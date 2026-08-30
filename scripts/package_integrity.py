"""Strict manifest parsing and bidirectional shipment verification."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import unicodedata
from pathlib import Path, PurePosixPath, PureWindowsPath


MANIFEST_LINE = re.compile(r"^([0-9a-fA-F]{64})  (.+)$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_scope(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise ValueError("package integrity scope schema_version must be 1")
    protected = [PurePosixPath(normalize_relative(item)).parts for item in value["protected_roots"]]
    for raw in [*value["mutable_roots"], *value["mutable_files"]]:
        declared = PurePosixPath(normalize_relative(raw)).parts
        if any(
            declared[: len(item)] == item or item[: len(declared)] == declared for item in protected
        ):
            raise ValueError(f"mutable declaration overlaps protected root: {raw}")
    return value


def normalize_relative(raw: str) -> str:
    if not raw or "\x00" in raw:
        raise ValueError("path is empty or contains NUL")
    candidate = unicodedata.normalize("NFC", raw.replace("\\", "/"))
    if PurePosixPath(candidate).is_absolute() or PureWindowsPath(raw).is_absolute():
        raise ValueError(f"absolute path is forbidden: {raw}")
    if PureWindowsPath(raw).drive:
        raise ValueError(f"drive-qualified path is forbidden: {raw}")
    parts = PurePosixPath(candidate).parts
    if any(part == ".." for part in parts):
        raise ValueError(f"path traversal is forbidden: {raw}")
    normalized = PurePosixPath(*parts).as_posix()
    if normalized in {"", "."}:
        raise ValueError(f"invalid relative path: {raw}")
    return normalized


def parse_manifest(path: Path) -> tuple[dict[str, str], list[str]]:
    entries: dict[str, str] = {}
    folded: dict[str, str] = {}
    errors: list[str] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        match = MANIFEST_LINE.fullmatch(line)
        if not match:
            errors.append(f"invalid manifest line {number}")
            continue
        digest, raw = match.groups()
        try:
            relative = normalize_relative(raw)
        except ValueError as exc:
            errors.append(f"manifest line {number}: {exc}")
            continue
        key = relative.casefold()
        if relative in entries:
            errors.append(f"duplicate normalized manifest path: {relative}")
            continue
        if key in folded:
            errors.append(f"case-colliding manifest paths: {folded[key]} and {relative}")
            continue
        entries[relative] = digest.lower()
        folded[key] = relative
    return entries, errors


def is_reparse(path: Path) -> bool:
    if path.is_symlink():
        return True
    junction = getattr(path, "is_junction", None)
    if junction is not None and junction():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except OSError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def path_has_reparse(root: Path, relative: str) -> bool:
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.exists() or current.is_symlink():
            if is_reparse(current):
                return True
    return False


def enumerate_files(root: Path) -> tuple[set[str], list[str]]:
    files: set[str] = set()
    errors: list[str] = []
    stack = [root]
    while stack:
        directory = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name.casefold())
        except OSError as exc:
            errors.append(f"cannot enumerate {directory}: {exc}")
            continue
        for entry in entries:
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            if is_reparse(path):
                errors.append(f"reparse point forbidden: {relative}")
                continue
            if entry.is_dir(follow_symlinks=False):
                stack.append(path)
            elif entry.is_file(follow_symlinks=False):
                files.add(relative)
    return files, errors


def generate_manifest(root: Path, ignored_files: set[str] | None = None) -> str:
    ignored = ignored_files or set()
    files, errors = enumerate_files(root)
    if errors:
        raise ValueError("; ".join(errors))
    return "".join(
        f"{sha256(root / relative)}  {relative}\n" for relative in sorted(files - ignored)
    )


def _is_mutable(relative: str, scope: dict) -> bool:
    path = PurePosixPath(relative)
    if path.suffix.casefold() in {item.casefold() for item in scope["blocked_mutable_suffixes"]}:
        return False
    if relative in scope["mutable_files"]:
        return True
    return any(
        relative == root or relative.startswith(root + "/") for root in scope["mutable_roots"]
    )


def verify_snapshot(root: Path, manifest_path: Path, scope: dict, mode: str) -> list[str]:
    if mode not in {"sealed", "mutable"}:
        raise ValueError("shipment mode must be sealed or mutable")
    if not manifest_path.is_file():
        return [f"shipment manifest missing: {manifest_path}"]
    manifest, errors = parse_manifest(manifest_path)
    actual, enumeration_errors = enumerate_files(root)
    errors.extend(enumeration_errors)
    for relative, expected in manifest.items():
        file = root / PurePosixPath(relative)
        if path_has_reparse(root, relative):
            errors.append(f"reparse point in manifest path: {relative}")
        elif not file.is_file():
            errors.append(f"shipment manifest file missing: {relative}")
        elif sha256(file) != expected:
            errors.append(f"shipment manifest mismatch: {relative}")
    ignored = {normalize_relative(item) for item in scope["sealed_ignored_files"]}
    extras = sorted(actual - set(manifest) - ignored)
    if mode == "sealed":
        errors.extend(f"unlisted shipment file: {relative}" for relative in extras)
    else:
        errors.extend(
            f"unlisted file outside mutable roots: {relative}"
            for relative in extras
            if not _is_mutable(relative, scope)
        )
    return errors
