#!/usr/bin/env python3
"""Create an immutable Xianyu manual-import candidate package from synthetic/approved input."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    source = json.loads(input_path.read_text(encoding="utf-8-sig"))
    output = Path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    rights_dir = output / "rights_evidence"
    rights_dir.mkdir(parents=True, exist_ok=True)

    reply_rules = []
    for raw_rule in source.get("reply_rules", []):
        rule = dict(raw_rule)
        rule.setdefault("mode", "draft")
        rule["auto_send"] = False
        rule.setdefault("requires_human_escalation", False)
        reply_rules.append(rule)

    generated_at = datetime.now(timezone.utc).isoformat()
    bundle = {
        "schema_version": 1,
        "bundle_id": source["bundle_id"],
        "stage": "X2_DRY_RUN",
        "mode": "draft_only",
        "generated_at": generated_at,
        "source_input_sha256": sha256(input_path),
        "sku": {
            "sku_id": source["sku_id"],
            "title": source["title"],
            "version": source["version"],
        },
        "rights": {
            "status": source.get("rights_status", "PENDING"),
            "evidence_files": ["rights_evidence/README.md"],
        },
        "external_actions": {
            "publish": False,
            "send_message": False,
            "deliver": False,
            "change_price": False,
            "refund": False,
        },
        "payload": {
            "listing_draft": {
                "title": source["listing_title"],
                "description": source["listing_description"],
                "buyer_notice": source.get("buyer_notice", []),
            },
            "reply_rules": reply_rules,
            "delivery_catalog": [],
        },
        "approval": {"status": "PENDING"},
    }

    write_json(output / "bundle.json", bundle)
    (output / "listing_draft.md").write_text(
        f"# {source['listing_title']}\n\n{source['listing_description']}\n",
        encoding="utf-8",
    )
    write_json(output / "reply_rules.json", reply_rules)
    write_json(output / "delivery_catalog.json", [])
    (rights_dir / "README.md").write_text(
        "# Rights evidence\n\n"
        "This synthetic package declares ORIGINAL only for contract testing. "
        "A real package must replace this file with verifiable ownership or license evidence.\n",
        encoding="utf-8",
    )
    (output / "test_report.md").write_text(
        "# Synthetic package test report\n\n"
        f"- Generated: {generated_at}\n"
        "- Dataset: synthetic only\n"
        "- External platform actions: all disabled\n"
        "- Delivery catalog: empty\n"
        "- Publication status: prohibited\n",
        encoding="utf-8",
    )

    package_files = [
        "bundle.json",
        "listing_draft.md",
        "reply_rules.json",
        "delivery_catalog.json",
        "rights_evidence/README.md",
        "test_report.md",
    ]
    manifest = {
        "schema_version": 1,
        "bundle_id": source["bundle_id"],
        "generated_at": generated_at,
        "files": [
            {
                "path": relative,
                "size": (output / relative).stat().st_size,
                "sha256": sha256(output / relative),
            }
            for relative in sorted(package_files)
        ],
    }
    manifest_path = output / "manifest.sha256.json"
    write_json(manifest_path, manifest)
    (output / "package.sha256.txt").write_text(sha256(manifest_path) + "\n", encoding="ascii")
    (output / "bundle.sha256.txt").write_text(
        sha256(output / "bundle.json") + "\n", encoding="ascii"
    )

    print(output / "bundle.json")
    print(f"package manifest SHA256: {sha256(manifest_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
