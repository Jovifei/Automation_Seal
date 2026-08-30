#!/usr/bin/env python3
"""Fail-closed readiness checks before a human Decision V3.

This validator intentionally accepts the expected pre-APPLY Framework Manifest
mismatch.  It must not require a formal Decision, a Gate plan, or a Post-Apply
Audit; those are checked by :mod:`validate_commerce_gate_readiness` later.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

from validate_commerce_gate_readiness import (
    formal_decision_hook_policy_errors,
    hook_policy_errors,
    load_json,
    parse_sha_manifest,
    sha256_file,
    verify_candidate_manifest,
    verify_review_package_manifest,
)


EVIDENCE_ROOT = Path("workspace/review-queue/commerce-v1/audit-remediation-v2")
CURRENT_CYCLE_POINTER = "CURRENT_REMEDIATION_CYCLE_V2.json"
REQUIRED_G2_FILES = (
    "JOVI_S1_RESTART_DECISION_V3_CANDIDATE.json",
    "JOVI_S1_RESTART_DECISION_V3_CANDIDATE.json.sha256.sidecar",
    "CONTROLLED_BASELINE_V2_CANDIDATE.json",
    "CONTROLLED_BASELINE_V2_CANDIDATE.sha256",
    "FRAMEWORK_MANIFEST_V2_CANDIDATE.sha256",
    "FINAL_CONTROL_TARGET_SET_V2.json",
    "PREFLIGHT_V4.json",
    "PRE_APPLY_AUDIT_INPUT_V4/REVIEW_PACKAGE_MANIFEST.json",
)
MIRROR_PATHS = {
    "STATUS.md",
    "PROJECT_STATE.json",
    "CODEX_START_PROMPT.txt",
    "tasks/todo.md",
    "CHANGELOG.md",
}


def _safe_relative(root: Path, value: str) -> Path | None:
    candidate = Path(value.replace("\\", "/"))
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    return root / candidate


def _sidecar_matches(path: Path, sidecar: Path | None = None) -> bool:
    sidecar = sidecar or path.with_name(path.name + ".sha256.sidecar")
    if not path.is_file() or not sidecar.is_file():
        return False
    fields = sidecar.read_text(encoding="utf-8-sig").strip().split()
    return bool(fields) and fields[0].lower() == sha256_file(path).lower()


def _verify_evidence_files(root: Path, names: list[str]) -> list[str]:
    errors: list[str] = []
    evidence = root / EVIDENCE_ROOT
    for name in names:
        path = evidence / name
        if not path.is_file():
            errors.append(f"missing V2 evidence: {name}")
            continue
        if name.endswith(".json") and not _sidecar_matches(path):
            errors.append(f"V2 evidence sidecar mismatch: {name}")
    return errors


def verify_human_only_cycle(
    root: Path, before_path: Path, after_path: Path, diff_path: Path
) -> list[str]:
    """Verify a complete new before/after cycle and reject any byte drift."""
    errors: list[str] = []
    before = load_json(before_path)
    after = load_json(after_path)
    diff = load_json(diff_path)
    if before is None or after is None or diff is None:
        return ["human-only before/after/diff evidence is missing or invalid JSON"]
    if before.get("historical_g1_before") != "NOT_VERIFIED":
        errors.append("old G1 human-only history was not kept NOT_VERIFIED")
    if before.get("new_v2_cycle_before", before.get("new_v2_rerun_before")) != "VERIFIED":
        errors.append("new V2 human-only before snapshot is not VERIFIED")
    if after.get("original_g1_history") not in (None, "NOT_VERIFIED"):
        errors.append("new V2 after evidence rewrites old G1 history")
    if after.get("new_v2_remediation_cycle", after.get("new_v2_rerun_cycle")) != "PASS_ZERO_DRIFT":
        errors.append("new V2 human-only after evidence is not PASS_ZERO_DRIFT")
    if diff.get("status") != "PASS_ZERO_DRIFT":
        errors.append("human-only diff is not PASS_ZERO_DRIFT")

    before_rows = {row.get("path"): row for row in before.get("entries", []) if isinstance(row, dict)}
    after_rows = {row.get("path"): row for row in after.get("entries", []) if isinstance(row, dict)}
    if set(before_rows) != set(after_rows):
        errors.append("human-only file set drift: added or deleted file")
    for rel, old in before_rows.items():
        new = after_rows.get(rel)
        if new is None:
            continue
        for field in ("bytes", "sha256", "reparse"):
            if old.get(field) != new.get(field):
                errors.append(f"human-only drift for {rel}: {field}")
        safe = _safe_relative(root, str(rel))
        if safe is None or not safe.is_file():
            errors.append(f"human-only file missing or unsafe: {rel}")
            continue
        actual = sha256_file(safe).lower()
        if actual != str(new.get("sha256", "")).lower():
            errors.append(f"human-only current SHA drift for {rel}")
        if safe.is_symlink() or (safe.stat().st_file_attributes & getattr(os, "FILE_ATTRIBUTE_REPARSE_POINT", 0)):
            errors.append(f"human-only reparse/symlink detected: {rel}")
    for key in ("added", "deleted", "changed", "reparse_changed"):
        values = diff.get(key, [])
        if values:
            errors.append(f"human-only diff contains {key} entries")
    return errors


def _protected_snapshot_errors(root: Path) -> list[str]:
    snapshot = root / EVIDENCE_ROOT / "PROTECTED_TREE_BEFORE_V2.json"
    payload = load_json(snapshot)
    if payload is None:
        return ["PROTECTED_TREE_BEFORE_V2 is missing or invalid"]
    errors: list[str] = []
    for row in payload.get("entries", []):
        if not isinstance(row, dict) or not row.get("present"):
            continue
        rel = str(row.get("path", "")).replace("\\", "/")
        if rel in MIRROR_PATHS:
            continue
        path = _safe_relative(root, rel)
        if path is None or not path.is_file():
            errors.append(f"protected path missing: {rel}")
        elif sha256_file(path).lower() != str(row.get("sha256", "")).lower():
            errors.append(f"protected path drifted: {rel}")
    return errors


def _verify_ledger_count(root: Path) -> list[str]:
    evidence = root / EVIDENCE_ROOT
    report = load_json(evidence / "GOVERNANCE_TEST_RESULTS_V2.json")
    if report is None:
        return ["GOVERNANCE_TEST_RESULTS_V2 is missing or invalid"]
    errors: list[str] = []
    if report.get("authority") != "GOVERNANCE_TEST_RESULTS_V2.json":
        errors.append("machine governance result is not authoritative")
    if report.get("passed") != 118 or report.get("collected") != 118:
        errors.append("machine governance result is not 118/118")
    todo = (root / "tasks/todo.md").read_text(encoding="utf-8") if (root / "tasks/todo.md").is_file() else ""
    if not any("G1.5" in line and "116/116 PASS" in line for line in todo.splitlines()):
        errors.append("tasks/todo.md does not preserve G1.5 initial 116/116")
    if not any("G1.7" in line and "118/118 PASS" in line for line in todo.splitlines()):
        errors.append("tasks/todo.md does not record G1.7 final 118/118")
    return errors


def _framework_mismatch_errors(root: Path, baseline: dict[str, Any]) -> list[str]:
    framework = parse_sha_manifest(root / "FRAMEWORK_MANIFEST.sha256")
    actual_mismatches = sorted(
        rel
        for rel, expected in framework.items()
        if not (root / rel).is_file() or sha256_file(root / rel).lower() != expected.lower()
    )
    expected = sorted(str(item) for item in baseline.get("pre_apply_expected_manifest_mismatches", []))
    if actual_mismatches != expected:
        return [
            "pre-apply Framework Manifest mismatch set differs from candidate: "
            f"actual={actual_mismatches!r} expected={expected!r}"
        ]
    return []


def validate_predecision_readiness(root: Path, package_dir: Path) -> list[str]:
    root = root.resolve()
    package_dir = package_dir.resolve()
    errors: list[str] = []
    evidence = root / EVIDENCE_ROOT
    if not package_dir.is_dir():
        errors.append(f"governance-v2 package is missing: {package_dir}")
        return errors
    for rel in REQUIRED_G2_FILES:
        if not (package_dir / rel).is_file():
            errors.append(f"missing G2 candidate: {rel}")

    hook_path = evidence / "HOOK_POLICY_V1.json"
    hook = load_json(hook_path)
    if hook is None:
        errors.append("HOOK_POLICY_V1 candidate is missing or invalid")
    else:
        errors.extend(hook_policy_errors(hook, require_candidate_metadata=True))
        if not _sidecar_matches(hook_path):
            errors.append("HOOK_POLICY_V1 sidecar mismatch")

    pointer_path = evidence / CURRENT_CYCLE_POINTER
    pointer = load_json(pointer_path)
    if pointer is None:
        errors.append("current remediation cycle pointer is missing or invalid")
        cycle_files = {
            "before": "HUMAN_ONLY_TREE_BEFORE_V2.json",
            "after": "HUMAN_ONLY_TREE_AFTER_V2.json",
            "diff": "HUMAN_ONLY_TREE_DIFF_V2.json",
            "correction": "G1_EVIDENCE_CORRECTION_V2.json",
            "g3_finding": None,
        }
    else:
        if pointer.get("status") != "CURRENT_CANDIDATE_CYCLE":
            errors.append("current remediation cycle pointer is not current")
        cycle_files = {
            key: pointer.get(key)
            for key in ("before", "after", "diff", "correction", "g3_finding")
        }
        for key in ("before", "after", "diff", "correction"):
            if not isinstance(cycle_files.get(key), str):
                errors.append(f"current remediation cycle pointer missing {key}")
    evidence_names = [
        "GOVERNANCE_TEST_RESULTS_V2.json",
        CURRENT_CYCLE_POINTER,
        cycle_files["before"],
        cycle_files["after"],
        cycle_files["diff"],
        cycle_files["correction"],
    ]
    if cycle_files.get("g3_finding"):
        evidence_names.append(cycle_files["g3_finding"])
    errors.extend(_verify_evidence_files(root, [name for name in evidence_names if name]))
    errors.extend(
        verify_human_only_cycle(
            root,
            evidence / str(cycle_files["before"]),
            evidence / str(cycle_files["after"]),
            evidence / str(cycle_files["diff"]),
        )
    )
    errors.extend(_verify_ledger_count(root))
    errors.extend(_protected_snapshot_errors(root))

    matched, total, candidate_errors = verify_candidate_manifest(
        root, root / "workspace/review-queue/commerce-v1/CANDIDATE_MANIFEST.json"
    )
    errors.extend(candidate_errors)
    if (matched, total) != (20, 20):
        errors.append(f"Commerce candidate is not 20/20: {matched}/{total}")

    candidate = load_json(package_dir / "JOVI_S1_RESTART_DECISION_V3_CANDIDATE.json")
    if candidate is not None:
        if candidate.get("issued_from_human") is not False:
            errors.append("Decision V3 candidate must remain issued_from_human=false")
        errors.extend(formal_decision_hook_policy_errors(candidate))
        if not _sidecar_matches(package_dir / "JOVI_S1_RESTART_DECISION_V3_CANDIDATE.json"):
            errors.append("Decision V3 candidate sidecar mismatch")
    baseline_path = package_dir / "CONTROLLED_BASELINE_V2_CANDIDATE.json"
    baseline = load_json(baseline_path)
    if baseline is not None:
        if baseline.get("status") != "CANDIDATE_PENDING_HUMAN_CONFIRMATION":
            errors.append("Controlled Baseline candidate is not pending human confirmation")
        errors.extend(_framework_mismatch_errors(root, baseline))
        baseline_sidecar = package_dir / "CONTROLLED_BASELINE_V2_CANDIDATE.sha256"
        if not baseline_sidecar.is_file() or baseline_sidecar.read_text(encoding="utf-8").strip().split()[:1] != [sha256_file(baseline_path)]:
            errors.append("Controlled Baseline candidate sidecar mismatch")

    review_manifest = package_dir / "PRE_APPLY_AUDIT_INPUT_V4/REVIEW_PACKAGE_MANIFEST.json"
    if review_manifest.is_file():
        matched, total, package_errors = verify_review_package_manifest(root, review_manifest)
        errors.extend(package_errors)
        if total == 0 or matched != total:
            errors.append(f"V4 review package is not fully matched: {matched}/{total}")

    formal_forbidden = (
        root / "workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json",
        root / "reports/gates/GATE_A_PLAN.json",
        root / "workspace/approvals/GATE_A.P.approval.json",
    )
    errors.extend(f"formal object exists before Decision: {path}" for path in formal_forbidden if path.exists())
    state = load_json(root / "config/control-plane-state.json")
    if state is None or state.get("stage") != "S1" or state.get("phase_status") != "CLOSED":
        errors.append("pre-decision state must remain S1/CLOSED")
    if (root / ".git/HEAD").exists():
        errors.append("Git HEAD exists before Gate A.P")
    for rel in ("jovi_commerce", "docs/commerce", "schemas/commerce", "data/commerce"):
        if (root / rel).exists():
            errors.append(f"formal Commerce path exists before Gate A.P: {rel}")
    products = root / "products"
    if products.exists():
        # The legacy Modbus SKU directory predates this Commerce cycle and is
        # explicitly out of scope.  It may remain, but no new Commerce SKU or
        # product content may appear before Gate A.P.
        unexpected = [
            child.name
            for child in products.iterdir()
            if child.name != "modbus-rtu-toolkit"
        ]
        if unexpected:
            errors.append(
                "pre-existing products path contains an unexpected Commerce item: "
                + ", ".join(sorted(unexpected))
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    errors = validate_predecision_readiness(args.root, args.package)
    payload = {
        "schema_version": 1,
        "status": "PREDECISION_READY_FOR_INDEPENDENT_AUDIT" if not errors else "NOT_READY",
        "errors": errors,
        "hook": "DO_NOT_TRUST",
        "formal_decision_created": False,
        "gate_a_p_created": False,
        "real_platform_actions": False,
    }
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if args.output:
        args.output.resolve().write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
