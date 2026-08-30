#!/usr/bin/env python3
"""Validate a Jovi Xianyu candidate bundle and its immutable package manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # The first read-only audit must work with the Python standard library.
    Draft202012Validator = None
    FormatChecker = None

ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_manifest(package_dir: Path, errors: list[str]) -> None:
    manifest_path = package_dir / "manifest.sha256.json"
    package_hash_path = package_dir / "package.sha256.txt"
    if not manifest_path.exists():
        errors.append("missing manifest.sha256.json")
        return
    if not package_hash_path.exists():
        errors.append("missing package.sha256.txt")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        errors.append(f"manifest unreadable: {exc}")
        return

    listed: set[str] = set()
    for index, item in enumerate(manifest.get("files", [])):
        if not isinstance(item, dict):
            errors.append(f"manifest.files[{index}] must be an object")
            continue
        relative = str(item.get("path", "")).replace("\\", "/")
        if not relative or relative.startswith("/") or ".." in Path(relative).parts:
            errors.append(f"manifest contains unsafe path: {relative!r}")
            continue
        if relative in listed:
            errors.append(f"manifest contains duplicate path: {relative}")
            continue
        listed.add(relative)
        target = (package_dir / relative).resolve()
        try:
            target.relative_to(package_dir.resolve())
        except ValueError:
            errors.append(f"manifest path escapes package: {relative}")
            continue
        if not target.is_file():
            errors.append(f"manifest file missing: {relative}")
            continue
        actual_hash = sha256(target)
        if actual_hash != str(item.get("sha256", "")).lower():
            errors.append(f"manifest hash mismatch: {relative}")
        if target.stat().st_size != item.get("size"):
            errors.append(f"manifest size mismatch: {relative}")

    allowed_unlisted = {"manifest.sha256.json", "package.sha256.txt", "bundle.sha256.txt"}
    actual = {
        path.relative_to(package_dir).as_posix()
        for path in package_dir.rglob("*")
        if path.is_file()
    }
    extras = actual - listed - allowed_unlisted
    if extras:
        errors.append("unlisted package files: " + ", ".join(sorted(extras)))

    expected_package_hash = (
        package_hash_path.read_text(encoding="ascii", errors="ignore").strip().lower()
    )
    if not re.fullmatch(r"[a-f0-9]{64}", expected_package_hash):
        errors.append("package.sha256.txt is invalid")
    elif sha256(manifest_path) != expected_package_hash:
        errors.append("package manifest SHA256 mismatch")


def fallback_schema_errors(bundle: object) -> list[str]:
    """Small standard-library fallback for the package's fixed bundle schema.

    The full jsonschema library remains supported, but it is not a prerequisite
    for the first read-only audit. This fallback checks every security-relevant
    invariant used by the current schema.
    """
    errors: list[str] = []
    if not isinstance(bundle, dict):
        return ["schema $: bundle must be an object"]
    required = {
        "schema_version",
        "bundle_id",
        "stage",
        "mode",
        "generated_at",
        "sku",
        "rights",
        "external_actions",
        "payload",
        "approval",
    }
    missing = sorted(required - set(bundle))
    if missing:
        errors.append("schema $: missing required fields: " + ", ".join(missing))
    allowed = required | {"source_input_sha256"}
    extras = sorted(set(bundle) - allowed)
    if extras:
        errors.append("schema $: unexpected fields: " + ", ".join(extras))
    if bundle.get("schema_version") != 1:
        errors.append("schema schema_version: 1 was expected")
    if not isinstance(bundle.get("bundle_id"), str) or not re.fullmatch(
        r"[A-Za-z0-9._-]+", str(bundle.get("bundle_id", ""))
    ):
        errors.append("schema bundle_id: safe string was expected")
    if bundle.get("stage") not in {
        "X2_DRY_RUN",
        "X3_FIXED_REPLY_CANDIDATE",
        "X4_SINGLE_SKU_CANDIDATE",
    }:
        errors.append("schema stage: unsupported stage")
    if bundle.get("mode") not in {"draft_only", "manual_import_only"}:
        errors.append("schema mode: unsupported mode")
    generated_at = bundle.get("generated_at")
    if not isinstance(generated_at, str) or "T" not in generated_at:
        errors.append("schema generated_at: ISO date-time string was expected")
    source_hash = bundle.get("source_input_sha256")
    if source_hash is not None and (
        not isinstance(source_hash, str) or not re.fullmatch(r"[a-f0-9]{64}", source_hash)
    ):
        errors.append("schema source_input_sha256: lowercase SHA256 was expected")

    sku = bundle.get("sku")
    if not isinstance(sku, dict):
        errors.append("schema sku: object was expected")
    else:
        for key in ("sku_id", "title", "version"):
            if not isinstance(sku.get(key), str):
                errors.append(f"schema sku.{key}: string was expected")

    rights = bundle.get("rights")
    if not isinstance(rights, dict):
        errors.append("schema rights: object was expected")
    else:
        if rights.get("status") not in {"ORIGINAL", "VERIFIED_LICENSE", "PENDING", "BLOCKED"}:
            errors.append("schema rights.status: unsupported status")
        evidence = rights.get("evidence_files", [])
        if not isinstance(evidence, list) or not all(isinstance(item, str) for item in evidence):
            errors.append("schema rights.evidence_files: string array was expected")

    actions = bundle.get("external_actions")
    expected_actions = {"publish", "send_message", "deliver", "change_price", "refund"}
    if not isinstance(actions, dict):
        errors.append("schema external_actions: object was expected")
    else:
        if set(actions) != expected_actions:
            errors.append("schema external_actions: exactly five fields were expected")
        for key in expected_actions:
            if actions.get(key) is not False:
                errors.append(f"schema external_actions.{key}: false was expected")

    payload = bundle.get("payload")
    if not isinstance(payload, dict):
        errors.append("schema payload: object was expected")
    else:
        if not isinstance(payload.get("listing_draft"), dict):
            errors.append("schema payload.listing_draft: object was expected")
        if not isinstance(payload.get("reply_rules"), list):
            errors.append("schema payload.reply_rules: array was expected")
        if not isinstance(payload.get("delivery_catalog"), list):
            errors.append("schema payload.delivery_catalog: array was expected")

    approval = bundle.get("approval")
    if not isinstance(approval, dict) or approval.get("status") != "PENDING":
        errors.append("schema approval.status: PENDING was expected")
    return errors


def validate_bundle(
    bundle_path: Path,
    schema_path: Path | None = None,
    *,
    skip_package_manifest: bool = False,
) -> list[str]:
    """Return all schema, semantic and package-integrity errors."""
    bundle_path = bundle_path.resolve()
    schema_path = (
        schema_path or ROOT / "deploy" / "xianyu" / "xianyu_bundle.schema.json"
    ).resolve()
    errors: list[str] = []
    try:
        bundle = json.loads(bundle_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return [f"bundle JSON unreadable: {exc}"]
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return [f"schema JSON unreadable: {exc}"]

    if Draft202012Validator is not None and FormatChecker is not None:
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for error in sorted(validator.iter_errors(bundle), key=lambda item: list(item.path)):
            where = ".".join(str(part) for part in error.path) or "$"
            errors.append(f"schema {where}: {error.message}")
    else:
        errors.extend(fallback_schema_errors(bundle))

    rights = bundle.get("rights", {})
    if rights.get("status") not in {"ORIGINAL", "VERIFIED_LICENSE"}:
        errors.append("rights status must be ORIGINAL or VERIFIED_LICENSE")

    actions = bundle.get("external_actions", {})
    expected_actions = {"publish", "send_message", "deliver", "change_price", "refund"}
    if set(actions) != expected_actions:
        errors.append("external_actions must contain exactly the five defined keys")
    for key in expected_actions:
        if actions.get(key) is not False:
            errors.append(f"external action {key} must be false")

    if bundle.get("approval", {}).get("status") != "PENDING":
        errors.append("bundle approval must remain PENDING; approval is a separate receipt")

    payload = bundle.get("payload", {})
    if bundle.get("stage") == "X2_DRY_RUN" and payload.get("delivery_catalog"):
        errors.append("X2 delivery catalog must be empty")

    listing = payload.get("listing_draft", {})
    if not str(listing.get("title", "")).strip():
        errors.append("listing title must not be empty")
    if not str(listing.get("description", "")).strip():
        errors.append("listing description must not be empty")

    for index, rule in enumerate(payload.get("reply_rules", [])):
        if not isinstance(rule, dict):
            errors.append(f"reply_rules[{index}] must be an object")
            continue
        if rule.get("mode") not in {"fixed_template", "draft"}:
            errors.append(f"reply_rules[{index}].mode must be fixed_template or draft")
        if rule.get("auto_send") is True:
            errors.append(f"reply_rules[{index}].auto_send must not be true")

    bundle_id = str(bundle.get("bundle_id", ""))
    if not re.fullmatch(r"[A-Za-z0-9._-]+", bundle_id):
        errors.append("bundle_id contains unsafe characters")

    if not skip_package_manifest:
        validate_manifest(bundle_path.parent, errors)
    # Preserve first occurrence order while removing duplicates.
    return list(dict.fromkeys(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--schema")
    parser.add_argument("--skip-package-manifest", action="store_true")
    args = parser.parse_args()
    errors = validate_bundle(
        Path(args.bundle),
        Path(args.schema) if args.schema else None,
        skip_package_manifest=args.skip_package_manifest,
    )
    if errors:
        for item in errors:
            print(f"[FAIL] {item}")
        return 2
    print("[PASS] bundle schema, semantics and package manifest valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
