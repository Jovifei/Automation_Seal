#!/usr/bin/env python3
"""Governance-side C2 deterministic delivery-package reference oracle."""
from __future__ import annotations
import argparse, hashlib, io, json, re, stat, sys, zipfile
from pathlib import Path, PurePosixPath

FORMAT = "C2_DETERMINISTIC_ZIP_V1"
FIXED_DT = (1980, 1, 1, 0, 0, 0)
DRIVE_RE = re.compile(r"^[A-Za-z]:")

class ContractError(ValueError):
    pass

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical_json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")

def validate_relative_path(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContractError("EMPTY_RELATIVE_PATH")
    if "\x00" in value:
        raise ContractError("NUL_IN_PATH")
    if "\\" in value:
        raise ContractError("BACKSLASH_PATH_FORBIDDEN")
    if value.startswith("/") or value.startswith("//") or DRIVE_RE.match(value):
        raise ContractError("ABSOLUTE_OR_DRIVE_PATH_FORBIDDEN")
    p = PurePosixPath(value)
    if any(part in ("", ".", "..") for part in p.parts):
        raise ContractError("DOT_OR_TRAVERSAL_SEGMENT_FORBIDDEN")
    return p.as_posix()

def _assert_regular_file(root: Path, rel: str) -> Path:
    target = root.joinpath(*PurePosixPath(rel).parts)
    try:
        resolved_root = root.resolve(strict=True)
        resolved_target = target.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ContractError(f"MISSING_ASSET:{rel}") from exc
    try:
        resolved_target.relative_to(resolved_root)
    except ValueError as exc:
        raise ContractError(f"PATH_ESCAPE:{rel}") from exc
    current = resolved_root
    for part in PurePosixPath(rel).parts:
        current = current / part
        if current.is_symlink():
            raise ContractError(f"SYMLINK_FORBIDDEN:{rel}")
    if not stat.S_ISREG(resolved_target.stat().st_mode):
        raise ContractError(f"NOT_REGULAR_FILE:{rel}")
    return resolved_target

def read_stable_asset(root: Path, rel: str) -> bytes:
    target = _assert_regular_file(root, rel)
    before = target.stat()
    data = target.read_bytes()
    after = target.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ContractError(f"ASSET_CHANGED_DURING_READ:{rel}")
    return data

def verify_product_manifest(root: Path, manifest: dict) -> list[dict]:
    if manifest.get("synthetic_only") is not True:
        raise ContractError("SYNTHETIC_ONLY_REQUIRED")
    if manifest.get("rights_status") != "original":
        raise ContractError("RIGHTS_NOT_ORIGINAL")
    if manifest.get("prohibited_content_confirmed_absent") is not True:
        raise ContractError("PROHIBITED_CONTENT_NOT_CONFIRMED_ABSENT")
    if not manifest.get("deliverables"):
        raise ContractError("EMPTY_DELIVERABLES")
    if not manifest.get("acceptance_criteria"):
        raise ContractError("EMPTY_ACCEPTANCE_CRITERIA")
    assets = manifest.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ContractError("EMPTY_ASSETS")
    verified, seen = [], set()
    for raw in assets:
        rel = validate_relative_path(raw.get("relative_path"))
        if rel in seen:
            raise ContractError(f"DUPLICATE_ASSET:{rel}")
        seen.add(rel)
        data = read_stable_asset(root, rel)
        actual = sha256_bytes(data)
        if actual != raw.get("sha256"):
            raise ContractError(f"ASSET_SHA_MISMATCH:{rel}")
        if len(data) != raw.get("size"):
            raise ContractError(f"ASSET_SIZE_MISMATCH:{rel}")
        if raw.get("rights_status") != "original":
            raise ContractError(f"ASSET_RIGHTS_NOT_ORIGINAL:{rel}")
        verified.append({
            "relative_path": rel,
            "sha256": actual,
            "size": len(data),
            "media_type": raw.get("media_type"),
            "rights_status": "original",
        })
    if sorted(manifest["deliverables"]) != sorted(seen):
        raise ContractError("DELIVERABLE_ASSET_SET_MISMATCH")
    return sorted(verified, key=lambda x: x["relative_path"])

def _zip_info(name: str) -> zipfile.ZipInfo:
    z = zipfile.ZipInfo(name, FIXED_DT)
    z.compress_type = zipfile.ZIP_STORED
    z.create_system = 3
    z.create_version = 20
    z.extract_version = 20
    z.external_attr = (0o100644 & 0xFFFF) << 16
    z.internal_attr = 0
    z.extra = b""
    z.comment = b""
    return z

def build_package(root: Path, manifest: dict) -> tuple[bytes, dict]:
    assets = verify_product_manifest(root, manifest)
    product_manifest_bytes = canonical_json_bytes(manifest)
    package_manifest = {
        "schema_version": 1,
        "package_format": FORMAT,
        "release_id": f"rel_{manifest['product_id']}_{manifest['version'].replace('.', '_')}",
        "product_id": manifest["product_id"],
        "version": manifest["version"],
        "product_manifest_sha256": sha256_bytes(product_manifest_bytes),
        "files": assets,
    }
    manifest_bytes = canonical_json_bytes(package_manifest)
    members = {"MANIFEST.json": manifest_bytes}
    for asset in assets:
        members[asset["relative_path"]] = read_stable_asset(root, asset["relative_path"])
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as zf:
        for name in sorted(members):
            zf.writestr(_zip_info(name), members[name])
    return out.getvalue(), package_manifest

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture_root", type=Path)
    ap.add_argument("output_zip", type=Path)
    ap.add_argument("--manifest", type=Path)
    ap.add_argument("--expect-zip-sha256")
    args = ap.parse_args()
    manifest_path = args.manifest or args.fixture_root / "product-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    package, package_manifest = build_package(args.fixture_root, manifest)
    actual = sha256_bytes(package)
    if args.expect_zip_sha256 and actual != args.expect_zip_sha256:
        print(f"ZIP_SHA_MISMATCH expected={args.expect_zip_sha256} actual={actual}", file=sys.stderr)
        return 2
    args.output_zip.parent.mkdir(parents=True, exist_ok=True)
    args.output_zip.write_bytes(package)
    print(json.dumps({
        "verdict": "C2_REFERENCE_PACKAGE_PASS",
        "format": FORMAT,
        "zip_sha256": actual,
        "zip_size": len(package),
        "manifest_sha256": sha256_bytes(canonical_json_bytes(package_manifest)),
        "file_count": len(package_manifest["files"]),
    }, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
