#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MAX_COMMAND_TEXT = 1500
MAX_OPENAPI_BYTES = 4 * 1024 * 1024
SAFE_VERSION = re.compile(r"^v?\d+(?:\.\d+){1,3}(?:[-+][0-9A-Za-z.-]+)?$")


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 15) -> dict[str, Any]:
    try:
        process = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        return {
            "ok": process.returncode == 0,
            "returncode": process.returncode,
            "stdout": process.stdout.strip()[:MAX_COMMAND_TEXT],
            "stderr": process.stderr.strip()[:MAX_COMMAND_TEXT],
        }
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


def safe_version_file(path: Path) -> dict[str, Any]:
    result = {"exists": path.exists(), "size": None, "value": None, "accepted": False}
    if not path.is_file():
        return result
    result["size"] = path.stat().st_size
    if path.stat().st_size > 128:
        return result
    try:
        value = path.read_text(encoding="utf-8-sig").strip()
    except Exception:
        return result
    if SAFE_VERSION.fullmatch(value):
        result["value"] = value
        result["accepted"] = True
    return result


def git_status_summary(repo: Path) -> dict[str, Any]:
    raw = run(["git", "status", "--porcelain=v1", "-z"], repo)
    if not raw.get("ok"):
        return {"ok": False, "error": raw.get("stderr") or raw.get("error")}
    # Re-run in bytes mode to avoid retaining path strings in the report.
    try:
        process = subprocess.run(
            ["git", "status", "--porcelain=v1", "-z"],
            cwd=repo,
            capture_output=True,
            timeout=15,
        )
        entries = [item for item in process.stdout.split(b"\x00") if item]
        codes: dict[str, int] = {}
        for entry in entries:
            code = entry[:2].decode("ascii", errors="replace")
            codes[code] = codes.get(code, 0) + 1
        return {
            "ok": process.returncode == 0,
            "dirty": bool(entries),
            "entry_count": len(entries),
            "status_codes": codes,
            "paths_reported": False,
        }
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


def parse_bool_like(value: str) -> bool | None:
    normalized = value.strip().strip("\"'").lower()
    if normalized in {"true", "1", "yes", "on"}:
        return True
    if normalized in {"false", "0", "no", "off"}:
        return False
    return None


def safe_compose_findings(text: str) -> dict[str, Any]:
    """Return only structural and boolean risk findings, never environment values."""
    environment_keys = set()
    for match in re.finditer(r"^\s*-?\s*([A-Z][A-Z0-9_]+)\s*(?:=|:)", text, re.MULTILINE):
        environment_keys.add(match.group(1))

    enabled_flags: dict[str, bool | None] = {}
    for key in [
        "AUTO_REPLY_ENABLED",
        "AI_REPLY_ENABLED",
        "AUTO_DELIVERY_ENABLED",
        "ENABLE_VNC",
        "XY_SLIDER_REMOTE_ENABLED",
        "XY_SLIDER_DRISSION_FALLBACK",
        "USER_REGISTRATION_ENABLED",
    ]:
        match = re.search(rf"^\s*-?\s*{re.escape(key)}\s*(?:=|:)\s*([^\n#]+)", text, re.I | re.M)
        enabled_flags[key] = parse_bool_like(match.group(1)) if match else None

    known_default_markers = {
        "admin_password_known_default": bool(
            re.search(r"ADMIN_PASSWORD[^\n]*(admin123|change_me|default)", text, re.I)
        ),
        "jwt_secret_known_default": bool(
            re.search(r"JWT_SECRET[^\n]*(default-secret-key|change_me|default)", text, re.I)
        ),
    }
    port_mappings = []
    for match in re.finditer(
        r"^\s*-\s*[\"']?([^\"'\n#]+?\d{2,5}:\d{2,5})[\"']?\s*(?:#.*)?$", text, re.MULTILINE
    ):
        value = match.group(1).strip()
        # Ports are operational structure, not credential values.
        port_mappings.append(value)
    images = [
        m.group(1).strip() for m in re.finditer(r"^\s*image:\s*([^\s#]+)", text, re.MULTILINE)
    ]
    return {
        "content_collected": False,
        "environment_keys": sorted(environment_keys),
        "enabled_flags": enabled_flags,
        "known_default_markers": known_default_markers,
        "structural_risks": {
            "root_user": bool(re.search(r"^\s*user:\s*[\"']?0:0", text, re.I | re.M)),
            "whole_repo_rw_mount": bool(re.search(r"-\s*\.:/app:rw", text, re.I)),
            "mutable_latest_image": bool(
                re.search(r"^\s*image:\s*[^\n#]+:latest\s*$", text, re.I | re.M)
            ),
            "unqualified_host_port": any(
                not p.startswith(("127.0.0.1:", "[::1]:")) for p in port_mappings
            ),
            "vnc_ports_present": any(":5900" in p or ":6080" in p for p in port_mappings),
        },
        "images": images,
        "port_mappings": sorted(set(port_mappings)),
    }


def directory_metadata(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "type": "missing", "entry_count": 0, "names_reported": False}
    if not path.is_dir():
        return {"exists": True, "type": "other", "entry_count": None, "names_reported": False}
    try:
        count = sum(1 for _ in path.iterdir())
    except Exception:
        count = None
    return {"exists": True, "type": "directory", "entry_count": count, "names_reported": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    report: dict[str, Any] = {
        "schema_version": 3,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_path": str(repo),
        "mode": "X0_READ_ONLY_REDACTED",
        "exists": repo.exists(),
        "git": {},
        "safe_versions": {},
        "file_inventory": {},
        "compose": {},
        "runtime": {},
        "health": {},
        "openapi": {},
        "sensitive_directories": {},
        "database_metadata": {
            "content_opened": False,
            "hashes_computed": False,
            "names_reported": False,
            "count": 0,
            "total_size": 0,
        },
        "warnings": [],
    }

    if not repo.exists():
        report["warnings"].append("Local Xianyu path does not exist; X1+ remain blocked.")
    else:
        if (repo / ".git").exists():
            report["git"]["head"] = run(["git", "rev-parse", "HEAD"], repo)
            report["git"]["branch"] = run(["git", "branch", "--show-current"], repo)
            report["git"]["status_summary"] = git_status_summary(repo)
            report["git"]["remote_names_only"] = run(["git", "remote"], repo)

        for relative in ["version.txt", "static/version.txt"]:
            report["safe_versions"][relative] = safe_version_file(repo / relative)

        # README and LICENSE are public-like project documentation. Sensitive configuration
        # is inventoried by size only; values and hashes are not collected.
        for relative in [
            "README.md",
            "LICENSE",
            "SECURITY.md",
            "global_config.yml",
            "docker-compose.yml",
            "docker-compose-cn.yml",
        ]:
            path = repo / relative
            if path.is_file():
                report["file_inventory"][relative] = {
                    "exists": True,
                    "size": path.stat().st_size,
                    "hash_computed": False,
                    "content_in_report": False,
                }
                if relative.startswith("docker-compose"):
                    try:
                        text = path.read_text(encoding="utf-8-sig", errors="replace")
                        report["compose"][relative] = safe_compose_findings(text)
                    except Exception as exc:
                        report["compose"][relative] = {"error": f"{type(exc).__name__}: {exc}"}

        for directory in ["data", "browser_data", "logs", "backups", "update_backup"]:
            report["sensitive_directories"][directory] = directory_metadata(repo / directory)

        data_dir = repo / "data"
        if data_dir.is_dir():
            try:
                db_files = [
                    p
                    for p in data_dir.iterdir()
                    if p.is_file() and p.suffix.lower() in {".db", ".sqlite", ".sqlite3"}
                ]
                report["database_metadata"]["count"] = len(db_files)
                report["database_metadata"]["total_size"] = sum(p.stat().st_size for p in db_files)
            except Exception as exc:
                report["database_metadata"]["error"] = f"{type(exc).__name__}: {exc}"

        docker_state = run(
            [
                "docker",
                "ps",
                "--filter",
                "name=xianyu",
                "--format",
                "{{.Names}}|{{.Status}}|{{.Ports}}",
            ]
        )
        report["runtime"]["docker_ps_filtered"] = docker_state
        mapped_ports = []
        if docker_state.get("ok"):
            for match in re.finditer(
                r"(?:127\.0\.0\.1|0\.0\.0\.0|\[::\])?:(\d+)->8090/tcp",
                docker_state.get("stdout", ""),
            ):
                mapped_ports.append(int(match.group(1)))
        mapped_ports = sorted(set(mapped_ports))
        report["runtime"]["detected_host_ports"] = mapped_ports

        for port in mapped_ports:
            try:
                with urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/health", timeout=3
                ) as response:
                    response.read(4097)
                    report["health"][str(port)] = {"ok": True, "status": response.status}
            except Exception as exc:
                report["health"][str(port)] = {"ok": False, "error": type(exc).__name__}
            try:
                with urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/openapi.json", timeout=3
                ) as response:
                    raw = response.read(MAX_OPENAPI_BYTES + 1)
                if len(raw) > MAX_OPENAPI_BYTES:
                    raise ValueError("OpenAPI response exceeds 4 MiB audit limit")
                data = json.loads(raw.decode("utf-8"))
                paths = []
                for api_path, methods in (data.get("paths") or {}).items():
                    paths.append(
                        {
                            "path": api_path,
                            "methods": sorted(
                                key.upper()
                                for key in methods
                                if key.lower() in {"get", "post", "put", "patch", "delete"}
                            ),
                        }
                    )
                report["openapi"][str(port)] = {
                    "ok": True,
                    "title": (data.get("info") or {}).get("title"),
                    "version": (data.get("info") or {}).get("version"),
                    "paths": paths,
                    "request_bodies_collected": False,
                    "responses_collected": False,
                }
            except Exception as exc:
                report["openapi"][str(port)] = {"ok": False, "error": type(exc).__name__}

    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Xianyu X0 read-only audit",
        "",
        f"- Generated: {report['generated_at']}",
        f"- Repo: `{repo}`",
        f"- Exists: {report['exists']}",
        "- Sensitive values collected: no",
        "- Git paths reported: no",
        "- SQLite opened or hashed: no",
        "",
    ]
    for filename, findings in report.get("compose", {}).items():
        lines += [f"## {filename}", "", "| Finding | Value |", "|---|---|"]
        for key, value in (findings.get("structural_risks") or {}).items():
            lines.append(f"| {key} | {value} |")
        for key, value in (findings.get("enabled_flags") or {}).items():
            lines.append(f"| {key} | {value} |")
        lines.append("")
    lines += [
        "## Restrictions observed",
        "",
        "- No file was modified.",
        "- SQLite files were not opened or hashed.",
        "- Cookie, buyer message, card inventory, browser profile and secret values were not collected.",
        "- Git changed paths were not written to reports.",
        "- No container was started, stopped or restarted.",
        "- No platform write endpoint or verification endpoint was called.",
    ]
    (output / "audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output / "audit.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
