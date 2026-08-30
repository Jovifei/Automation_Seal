"""Read-only static-test support and independent build verification."""

from __future__ import annotations

import hashlib
import os
import shutil
import stat
import subprocess
import tempfile
import zipfile
from pathlib import Path


def _contained(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _existing_path_has_reparse(path: Path) -> bool:
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        if not (current.exists() or current.is_symlink()):
            continue
        if current.is_symlink() or (getattr(current, "is_junction", lambda: False)()):
            return True
        attributes = getattr(current.lstat(), "st_file_attributes", 0)
        if attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            return True
    return False


def resolve_report_dir(
    root: Path, output_dir: Path | None, approved_root: Path | None
) -> Path | None:
    if output_dir is None:
        if approved_root is not None:
            raise ValueError("--approved-output-root requires --output-dir")
        return None
    root = root.resolve()
    output = output_dir if output_dir.is_absolute() else root / output_dir
    output = output.resolve()
    approved = approved_root or (root / "reports")
    approved = approved if approved.is_absolute() else root / approved
    approved = approved.resolve()
    if not _contained(output, approved):
        raise ValueError(f"report output escapes approved root: {output}")
    if _existing_path_has_reparse(output) or _existing_path_has_reparse(approved):
        raise ValueError("report output path contains a reparse point")
    return output


def remove_runtime_caches(root: Path) -> None:
    for pyc in root.rglob("*.pyc"):
        try:
            pyc.unlink()
        except FileNotFoundError:
            pass
    for cache_dir in sorted(root.rglob("__pycache__"), reverse=True):
        try:
            cache_dir.rmdir()
        except OSError:
            pass


def snapshot_tree(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(
        item for item in root.rglob("*") if item.is_file() and ".git" not in item.parts
    ):
        result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def detect_capabilities(which=shutil.which) -> dict:
    windows_path = which("powershell.exe") or which("powershell")
    core_path = which("pwsh.exe") or which("pwsh")
    return {
        "windows_powershell": {"available": bool(windows_path), "path": windows_path},
        "powershell_core": {"available": bool(core_path), "path": core_path},
    }


def capability_limitations(capabilities: dict) -> list[str]:
    limitations: list[str] = []
    if capabilities["windows_powershell"]["available"]:
        limitations.append(
            "Windows PowerShell parser checks executed with the detected local runtime."
        )
    elif capabilities["powershell_core"]["available"]:
        limitations.append(
            "Windows PowerShell is unavailable; PowerShell Core parser checks used the detected local runtime."
        )
    else:
        limitations.append(
            "No PowerShell runtime was detected; PowerShell checks are lexical and structural only."
        )
    limitations.extend(
        [
            "Docker, WSL, GPU, Codex hook trust, current upstream releases and the real external adapter were not tested.",
            "No real account, message, order, delivery, price, refund or verification action was tested.",
        ]
    )
    return limitations


def _archive_facts(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        return {
            "bad_member": archive.testzip(),
            "names": sorted(archive.namelist()),
            "fixed_times": all(
                info.date_time == (2026, 1, 1, 0, 0, 0) for info in archive.infolist()
            ),
        }


def run_clean_build_pair(product: Path, python: str, env: dict[str, str]) -> dict:
    roots: list[Path] = []
    result: dict = {}
    first = tempfile.TemporaryDirectory(prefix="jovi-s1-build-a-")
    second = tempfile.TemporaryDirectory(prefix="jovi-s1-build-b-")
    try:
        roots = [Path(first.name), Path(second.name)]
        result["roots_distinct"] = roots[0].resolve() != roots[1].resolve()
        result["clean_starts"] = [not any(root.iterdir()) for root in roots]
        outputs = [root / "dist" for root in roots]
        runs = [
            subprocess.run(
                [python, "scripts/build_alpha.py", "--output-dir", str(output)],
                cwd=product,
                env=env,
                text=True,
                capture_output=True,
                timeout=60,
                check=False,
            )
            for output in outputs
        ]
        archives = [output / "modbus-rtu-toolkit-alpha.zip" for output in outputs]
        result["returncodes"] = [run.returncode for run in runs]
        result["details"] = [(run.stdout.strip() or run.stderr.strip()) for run in runs]
        result["archives_exist"] = [archive.is_file() for archive in archives]
        result["hashes"] = [
            hashlib.sha256(archive.read_bytes()).hexdigest() if archive.is_file() else None
            for archive in archives
        ]
        result["sha_files"] = [
            archive.with_suffix(archive.suffix + ".sha256.txt").read_text().strip()
            if archive.with_suffix(archive.suffix + ".sha256.txt").is_file()
            else None
            for archive in archives
        ]
        result["archive_facts"] = [
            _archive_facts(archive) if archive.is_file() else None for archive in archives
        ]
        result["shared_output"] = bool(set(outputs[0].rglob("*")) & set(outputs[1].rglob("*")))
    finally:
        first.cleanup()
        second.cleanup()
    result["cleaned"] = all(not root.exists() for root in roots)
    return result
