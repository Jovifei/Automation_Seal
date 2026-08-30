from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INCLUDE = [
    "README.md",
    "PRODUCT_SPEC.md",
    "LICENSE.txt",
    "THIRD_PARTY_NOTICES.md",
    "SBOM.cdx.json",
    "pyproject.toml",
    "modbus_toolkit",
    "tests",
    "examples",
]
FIXED_ZIP_TIME = (2026, 1, 1, 0, 0, 0)


def iter_included_files() -> list[Path]:
    files: list[Path] = []
    for relative in INCLUDE:
        path = ROOT / relative
        if path.is_dir():
            files.extend(
                file
                for file in sorted(path.rglob("*"))
                if file.is_file() and "__pycache__" not in file.parts and file.suffix != ".pyc"
            )
        elif path.is_file():
            files.append(path)
        else:
            raise FileNotFoundError(f"required product file missing: {relative}")
    return sorted(files, key=lambda file: file.relative_to(ROOT).as_posix())


def build_alpha(output_dir: Path) -> tuple[Path, str]:
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / "modbus-rtu-toolkit-alpha.zip"
    if archive_path.exists():
        archive_path.unlink()

    with zipfile.ZipFile(
        archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for file in iter_included_files():
            relative = file.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(relative, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, file.read_bytes())

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    archive_path.with_suffix(archive_path.suffix + ".sha256.txt").write_text(
        digest + "\n", encoding="ascii"
    )
    manifest = {
        "schema_version": 2,
        "product": "modbus-rtu-toolkit",
        "version": "0.1.0-alpha",
        "built_at": datetime.now(timezone.utc).isoformat(),
        "archive": archive_path.name,
        "sha256": digest,
        "deterministic_zip_timestamp": "2026-01-01T00:00:00Z",
        "source_files": [file.relative_to(ROOT).as_posix() for file in iter_included_files()],
    }
    (output_dir / "build-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return archive_path, digest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(ROOT / "dist"))
    args = parser.parse_args()
    archive_path, digest = build_alpha(Path(args.output_dir))
    print(f"{archive_path} {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
