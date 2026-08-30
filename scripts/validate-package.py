#!/usr/bin/env python3
"""Local, read-only validation for the Jovi Automation final handoff package."""

from __future__ import annotations

import argparse
from authorize_action import authorization_errors
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

from package_integrity import load_scope, verify_snapshot

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(
    description="Validate the Jovi package structure and immutable safety framework."
)
parser.add_argument(
    "--verify-shipment",
    action="store_true",
    help="Also verify the full as-shipped MANIFEST.sha256. Use immediately after extraction and before runtime files change.",
)
parser.add_argument(
    "--shipment-mode",
    choices=("sealed", "mutable"),
    default="sealed",
    help="Shipment verification policy. Mutable mode still requires --verify-shipment and only permits declared runtime outputs.",
)
parser.add_argument(
    "--scope-config",
    type=Path,
    default=Path("config/package-integrity-scope.json"),
    help="Package integrity scope relative to the package root.",
)
ARGS = parser.parse_args()
authorization = authorization_errors(ROOT, "package-validation")
if authorization:
    print("[DENY] " + "; ".join(authorization), file=sys.stderr)
    raise SystemExit(2)
errors: list[str] = []
warnings: list[str] = []

REQUIRED = [
    "00_先读我.txt",
    "README_FIRST.md",
    "PROJECT_STATE.json",
    "CODEX_START_PROMPT.txt",
    "AGENTS.md",
    "CODEX_MASTER_TASK.md",
    "FAST_TRACK.md",
    "FIRST_RUN_TROUBLESHOOTING.md",
    "USER_ACTION_CHECKLIST.md",
    "NEXT_STEP_MAP.md",
    "MANIFEST_POLICY.md",
    "DECISIONS_REQUIRED.md",
    "context/04_CONVERSATION_CONTEXT.md",
    "context/05_COMPLETED_WORK.md",
    "context/06_RESEARCH_FREEZE_POLICY.md",
    "context/source_markdown/04_PRD_嵌入式知识产品_MVP.md",
    "docs/00_最终交付与操作总说明.md",
    "docs/08_交付包内容说明与执行索引.md",
    "sources/research_review_2026-07-12.md",
    "sources/technology_route_review_2026-07-12.md",
    "products/modbus-rtu-toolkit/README.md",
    "products/modbus-rtu-toolkit/modbus_toolkit/parser.py",
    "products/modbus-rtu-toolkit/tests/test_parser.py",
    "products/modbus-rtu-toolkit/SBOM.cdx.json",
    "prompts/00_first_readonly_audit.txt",
    "prompts/10_track_p_alpha.txt",
    "deploy/docker-compose.core.yml",
    "deploy/.env.example",
    "deploy/xianyu/xianyu_bundle.schema.json",
    ".codex/hooks.json",
    "scripts/00-run-readonly-audit.ps1",
    "scripts/preflight.ps1",
    "scripts/research/resolve_versions.py",
    "scripts/run-static-tests.py",
    "scripts/codex/pre_tool_guard.py",
    "scripts/codex/Invoke-PreToolGuard.ps1",
    "scripts/xianyu/xianyu_readonly_audit.py",
    "scripts/human-only/Approve-Gate.ps1",
    "tests/acceptance_matrix.csv",
]
for relative in REQUIRED:
    if not (ROOT / relative).exists():
        errors.append(f"missing required file: {relative}")

# Machine-readable state.
try:
    state = json.loads((ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8-sig"))
    if state.get("package_version") != "3.0.0":
        errors.append("PROJECT_STATE package_version must be 3.0.0")
    if state.get("current_state") not in {
        "READY_FOR_CODEX_PHASE_0_A_X0",
        "AWAITING_GATE_A_TRACK_APPROVALS",
    }:
        warnings.append(f"unexpected current_state: {state.get('current_state')}")
    if state.get("decisions", {}).get("xianyu_integration") != "REUSE_AS_SEPARATE_ADAPTER":
        errors.append("Xianyu integration decision is missing or changed")
except Exception as exc:
    errors.append(f"PROJECT_STATE invalid: {exc}")

# JSON and YAML syntax.
for path in sorted(ROOT.rglob("*.json")):
    if any(part in {"reports", "backups", "dist", "__pycache__"} for part in path.parts):
        continue
    try:
        json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        errors.append(f"JSON invalid {path.relative_to(ROOT)}: {exc}")
try:
    import yaml
except Exception:
    yaml = None
    warnings.append("PyYAML unavailable; YAML semantic parsing skipped")
if yaml:
    for path in sorted(list(ROOT.rglob("*.yaml")) + list(ROOT.rglob("*.yml"))):
        if any(part in {"reports", "backups", "dist"} for part in path.parts):
            continue
        try:
            yaml.safe_load(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            errors.append(f"YAML invalid {path.relative_to(ROOT)}: {exc}")


# Skill mirrors.
def skills(base: Path) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    if not base.exists():
        return result
    for directory in sorted(p for p in base.iterdir() if p.is_dir()):
        file = directory / "SKILL.md"
        if not file.is_file():
            errors.append(f"missing SKILL.md: {file.relative_to(ROOT)}")
            continue
        raw = file.read_bytes()
        text = raw.decode("utf-8")
        match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if (
            not match
            or not re.search(r"^name:\s*\S+", match.group(1), re.MULTILINE)
            or not re.search(r"^description:", match.group(1), re.MULTILINE)
        ):
            errors.append(f"invalid Skill frontmatter: {file.relative_to(ROOT)}")
        result[directory.name] = raw
    return result


canonical = skills(ROOT / "skills")
if len(canonical) < 10:
    errors.append(f"expected at least 10 specialized skills, found {len(canonical)}")
for mirror in [ROOT / ".agents" / "skills", ROOT / "workspace" / "skills"]:
    mapped = skills(mirror)
    if set(mapped) != set(canonical):
        errors.append(f"skill mirror names mismatch: {mirror.relative_to(ROOT)}")
    for name in set(mapped) & set(canonical):
        if mapped[name] != canonical[name]:
            errors.append(f"skill mirror differs: {mirror.relative_to(ROOT)}/{name}")

# Formal docs and original product sources.
for index in range(9):
    matches = list((ROOT / "docs").glob(f"{index:02d}_*.md"))
    if len(matches) != 1:
        errors.append(f"expected exactly one docs/{index:02d}_*.md, found {len(matches)}")
        continue
    if not matches[0].with_suffix(".docx").is_file():
        errors.append(f"missing DOCX pair for {matches[0].name}")
for index in range(9):
    matches = list((ROOT / "context" / "source_markdown").glob(f"{index:02d}_*.md"))
    if len(matches) != 1:
        errors.append(f"expected original source markdown {index:02d}, found {len(matches)}")

# Compose safety.
compose = (ROOT / "deploy" / "docker-compose.core.yml").read_text(encoding="utf-8")
if re.search(r"image:\s*[^\n#]+:latest(?:\s|$)", compose, re.I):
    errors.append("core Compose contains a mutable latest tag")
for line in compose.splitlines():
    stripped = line.strip().strip("\"'")
    if re.fullmatch(r"-\s*\d{2,5}:\d{2,5}", stripped):
        errors.append(f"core Compose has non-loopback port mapping: {stripped}")
if "127.0.0.1:${N8N_PORT}:5678" not in compose:
    errors.append("n8n port is not explicitly loopback-only")
if "fetch('http://127.0.0.1:5678/healthz')" not in compose:
    errors.append("n8n healthcheck does not use the guaranteed Node runtime")
start_core = (ROOT / "scripts" / "start-core.ps1").read_text(encoding="utf-8-sig")
for phrase in [".env.runtime", "RepoDigest", "LOCKED_VERSIONS.json"]:
    if phrase not in start_core:
        errors.append(f"start-core missing immutable runtime control: {phrase}")

# Fixed decisions and no broad re-search.
start_prompt = (ROOT / "CODEX_START_PROMPT.txt").read_text(encoding="utf-8")
if "不要重新进行大范围" not in start_prompt:
    errors.append("start prompt does not freeze broad research")
if "00-run-readonly-audit.ps1" not in start_prompt:
    errors.append("start prompt lacks the one-command entry")
if "context/source_markdown/*.md" in start_prompt:
    warnings.append("start prompt appears to request indiscriminate historical context loading")

# Hook must not depend on Git and must block human-only and Xianyu mutations.
hook = (ROOT / "scripts" / "codex" / "pre_tool_guard.py").read_text(encoding="utf-8")
if "git rev-parse" in hook:
    errors.append("safety hook depends on an existing Git repository")
for phrase in ["human-only", "xianyu-auto-reply", "GATE_A", "approval_valid"]:
    if phrase not in hook:
        errors.append(f"safety hook missing expected control: {phrase}")

# No runtime caches or actual secrets.
for path in ROOT.rglob("*"):
    if any(part in {"__pycache__", ".pytest_cache", ".mypy_cache"} for part in path.parts):
        errors.append(f"runtime cache included: {path.relative_to(ROOT)}")
secret_pattern = re.compile(
    r"(?i)(sk-[a-z0-9]{20,}|ghp_[a-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
)
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() in {
        ".docx",
        ".xlsx",
        ".zip",
        ".png",
        ".jpg",
        ".jpeg",
    }:
        continue
    if path.stat().st_size > 2_000_000:
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    if secret_pattern.search(text):
        errors.append(f"possible embedded credential: {path.relative_to(ROOT)}")

# Scan text-bearing members inside Office and product ZIP packages without extracting them.
archive_text_suffixes = {".xml", ".rels", ".txt", ".md", ".py", ".json", ".yaml", ".yml", ".toml"}
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in {".docx", ".xlsx", ".zip"}:
        continue
    try:
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                errors.append(f"corrupt archive: {path.relative_to(ROOT)}")
                continue
            for info in archive.infolist():
                if (
                    info.file_size > 2_000_000
                    or Path(info.filename).suffix.lower() not in archive_text_suffixes
                ):
                    continue
                text = archive.read(info).decode("utf-8", errors="ignore")
                if secret_pattern.search(text):
                    errors.append(
                        f"possible embedded credential: {path.relative_to(ROOT)}::{info.filename}"
                    )
    except zipfile.BadZipFile:
        errors.append(f"invalid ZIP-compatible file: {path.relative_to(ROOT)}")

for forbidden in ["deploy/.env", "deploy/.env.runtime", "auth.json"]:
    if (ROOT / forbidden).exists():
        errors.append(f"runtime secret/state file included in shipment: {forbidden}")
for suffix in [".db", ".sqlite", ".sqlite3", ".pem", ".key"]:
    for path in ROOT.rglob(f"*{suffix}"):
        errors.append(f"forbidden runtime or key material included: {path.relative_to(ROOT)}")


# Manifest policy:
# - FRAMEWORK_MANIFEST.sha256 is immutable and is verified on every run.
# - MANIFEST.sha256 is the full as-shipped snapshot. Runtime evidence and state files
#   intentionally change after the first audit, so the full snapshot is verified only
#   with --verify-shipment (the unified first-run entry uses this flag before writes).
def verify_manifest(path: Path, label: str) -> None:
    if not path.is_file():
        warnings.append(
            f"{label} not present; archive-level SHA256 remains the outer integrity check"
        )
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            digest, relative = line.split("  ", 1)
        except ValueError:
            errors.append(f"invalid {label} line: {line[:80]}")
            continue
        file = ROOT / relative
        if not file.is_file():
            errors.append(f"{label} file missing: {relative}")
            continue
        actual = hashlib.sha256(file.read_bytes()).hexdigest()
        if actual != digest:
            errors.append(f"{label} mismatch: {relative}")


verify_manifest(ROOT / "FRAMEWORK_MANIFEST.sha256", "framework manifest")
if ARGS.verify_shipment:
    scope_path = ARGS.scope_config if ARGS.scope_config.is_absolute() else ROOT / ARGS.scope_config
    try:
        scope = load_scope(scope_path)
        manifest_path = ROOT / scope["shipment_manifest"]
        errors.extend(verify_snapshot(ROOT, manifest_path, scope, ARGS.shipment_mode))
    except Exception as exc:
        errors.append(f"shipment verification configuration invalid: {exc}")
elif (ROOT / "MANIFEST.sha256").is_file():
    warnings.append(
        "full shipment manifest skipped (use --verify-shipment only before runtime state changes)"
    )

if warnings:
    for warning in warnings:
        print(f"[WARN] {warning}")
if errors:
    for error in errors:
        print(f"[FAIL] {error}")
    print(f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s).")
    raise SystemExit(2)
print(
    f"[PASS] Package validation passed: {len(REQUIRED)} required entries, {len(canonical)} skills, 9 formal document pairs."
)
