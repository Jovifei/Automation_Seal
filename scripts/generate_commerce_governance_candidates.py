#!/usr/bin/env python3
"""Freeze the non-authoritative V3 and Controlled Baseline candidates.

The generator writes only under the Commerce review queue.  It refuses to
overwrite an existing candidate package and never touches a formal Decision,
Manifest, Approval, control-plane state, or external repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validate_commerce_gate_readiness import load_json, parse_sha_manifest, sha256_file


def _sha(path: Path) -> str:
    return sha256_file(path).lower()


def _write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite candidate: {path}")
    path.parent.mkdir(parents=True, exist_ok=False if not path.parent.exists() else True)
    path.write_bytes(data)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_new(path, (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def _copy_new(source: Path, destination: Path) -> None:
    _write_new(destination, source.read_bytes())


def _manifest_rows(root: Path) -> tuple[dict[str, str], list[str]]:
    manifest = parse_sha_manifest(root / "FRAMEWORK_MANIFEST.sha256")
    mismatches: list[str] = []
    for rel, expected in manifest.items():
        path = root / rel
        if not path.is_file() or _sha(path) != expected.lower():
            mismatches.append(rel)
    return manifest, sorted(mismatches)


def _target_set(root: Path, target_set_path: Path) -> dict[str, Any]:
    original = load_json(target_set_path) or {}
    rows: list[dict[str, Any]] = []
    for item in original.get("future_write_scope", []):
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            continue
        raw = str(item["path"])
        if ":" in raw[:3]:
            path = Path(raw)
        else:
            path = root / raw
        if path.is_file():
            rows.append(
                {
                    "path": raw.replace("\\", "/"),
                    "present": True,
                    "bytes": path.stat().st_size,
                    "sha256": _sha(path),
                    "action": item.get("action"),
                }
            )
        else:
            rows.append(
                {"path": raw.replace("\\", "/"), "present": False, "bytes": None, "sha256": None, "action": item.get("action")}
            )
    return {
        "schema": "JOVI_AUTOMATION_FINAL_CONTROL_TARGET_SET_V2",
        "status": "CANDIDATE_PENDING_INDEPENDENT_AUDIT",
        "source_target_set_sha256": _sha(target_set_path),
        "target_count": len(rows),
        "targets": rows,
        "forbidden": original.get("protected_no_write", []),
        "invariants": original.get("invariants", {}),
    }


def generate(root: Path, output_dir: Path) -> dict[str, Any]:
    root = root.resolve()
    output_dir = output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"candidate output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence = root / "workspace/review-queue/commerce-v1/audit-remediation-v2"
    target_set_path = evidence / "G1_AUDIT_REMEDIATION_TARGET_SET_V2.json"
    hook_path = evidence / "HOOK_POLICY_V1.json"
    hook = load_json(hook_path)
    if hook != {
        "schema_version": 1,
        "authority": "CANDIDATE_ONLY",
        "status": "DO_NOT_TRUST",
        "hook_runtime_dependency": False,
        "hook_restore_allowed": False,
        "hook_trust_allowed": False,
    }:
        raise ValueError("Hook Policy candidate is not the exact fail-closed object")
    now = datetime.now(timezone.utc).isoformat()
    run_id = "preflight-v4-" + uuid.uuid4().hex
    framework, mismatches = _manifest_rows(root)
    old_decision = root / "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json"
    pointer = load_json(evidence / "CURRENT_REMEDIATION_CYCLE_V2.json") or {}
    correction_name = pointer.get("correction", "G1_EVIDENCE_CORRECTION_V2.json")
    old_result = evidence / correction_name
    decision = {
        "schema": "JOVI_S1_RESTART_DECISION_V3_CANDIDATE",
        "issued_from_human": False,
        "status": "CANDIDATE_PENDING_HUMAN_CONFIRMATION",
        "created_at_utc": now,
        "hook_status": "DO_NOT_TRUST",
        "hook_runtime_dependency": False,
        "hook_restore_allowed": False,
        "hook_trust_allowed": False,
        "manifest_apply_scope": ["FRAMEWORK_MANIFEST.sha256"],
        "track_p_allowed": False,
        "track_i_allowed": False,
        "real_platform_actions_allowed": False,
        "bindings": {
            "old_decision_v1_sha256": _sha(old_decision),
            "hook_policy_sha256": _sha(hook_path),
            "governance_plan_sha256": "4c84c4ed51ac56bb6e98b4628eb1a121f03fe442170b7e066821474c8af0de37",
            "governance_target_set_sha256": _sha(target_set_path),
            "g1_evidence_correction_sha256": _sha(old_result),
            "candidate_manifest_sha256": _sha(root / "workspace/review-queue/commerce-v1/CANDIDATE_MANIFEST.json"),
        },
        "decision_note": "Candidate only; Jovi must issue the formal Decision V3 after independent G3 PASS.",
    }
    decision_path = output_dir / "JOVI_S1_RESTART_DECISION_V3_CANDIDATE.json"
    _write_json(decision_path, decision)
    _write_new(output_dir / (decision_path.name + ".sha256.sidecar"), (_sha(decision_path) + "  " + decision_path.name + "\n").encode("ascii"))

    baseline_rows: list[dict[str, Any]] = []
    for rel, formal_sha in sorted(framework.items()):
        path = root / rel
        if path.is_file():
            baseline_rows.append(
                {
                    "path": rel,
                    "formal_sha256": formal_sha,
                    "current_sha256": _sha(path),
                    "bytes": path.stat().st_size,
                    "disposition": "ACCEPT_CURRENT",
                    "source": "current_observed_tree",
                }
            )
        else:
            baseline_rows.append(
                {
                    "path": rel,
                    "formal_sha256": formal_sha,
                    "current_sha256": None,
                    "bytes": None,
                    "disposition": "REJECT",
                    "source": "missing_current_file",
                }
            )
    baseline = {
        "schema": "JOVI_AUTOMATION_CONTROLLED_BASELINE_V2_CANDIDATE",
        "status": "CANDIDATE_PENDING_HUMAN_CONFIRMATION",
        "created_at_utc": now,
        "manifest_apply_scope": ["FRAMEWORK_MANIFEST.sha256"],
        "formal_framework_manifest_sha256": _sha(root / "FRAMEWORK_MANIFEST.sha256"),
        "pre_apply_expected_manifest_mismatches": mismatches,
        "targets": baseline_rows,
        "hook_monitoring": {
            "path": ".codex/hooks.json",
            "status": "DO_NOT_TRUST",
            "runtime_dependency": False,
            "disposition": "ACCEPT_CURRENT",
        },
        "exclusions": ["MANIFEST.sha256", "reports/", "runtime/", "products/", "cache/", "build/"],
        "human_confirmation_required": True,
        "automatic_current_to_accepted_conversion": False,
    }
    baseline_path = output_dir / "CONTROLLED_BASELINE_V2_CANDIDATE.json"
    _write_json(baseline_path, baseline)
    _write_new(output_dir / "CONTROLLED_BASELINE_V2_CANDIDATE.sha256", (_sha(baseline_path) + "\n").encode("ascii"))

    candidate_manifest_lines = []
    for row in baseline_rows:
        if row["current_sha256"]:
            candidate_manifest_lines.append(f"{row['current_sha256']}  {row['path']}")
    _write_new(output_dir / "FRAMEWORK_MANIFEST_V2_CANDIDATE.sha256", ("\n".join(candidate_manifest_lines) + "\n").encode("utf-8"))
    final_targets = _target_set(root, target_set_path)
    final_targets["decision_candidate_sha256"] = _sha(decision_path)
    final_targets["controlled_baseline_candidate_sha256"] = _sha(baseline_path)
    _write_json(output_dir / "FINAL_CONTROL_TARGET_SET_V2.json", final_targets)

    preflight = {
        "schema": "JOVI_AUTOMATION_PRE_APPLY_PREFLIGHT_V4",
        "run_id": run_id,
        "run_at_utc": now,
        "reused_previous_result": False,
        "status": "FRESH_PRE_APPLY_CANDIDATE",
        "framework_manifest_mismatches": mismatches,
        "hook_status": "DO_NOT_TRUST",
        "formal_decision_created": False,
        "gate_a_p_created": False,
        "real_platform_actions": False,
    }
    _write_json(output_dir / "PREFLIGHT_V4.json", preflight)

    package = output_dir / "PRE_APPLY_AUDIT_INPUT_V4"
    package.mkdir()
    for source, dest in (
        (decision_path, package / "candidate/JOVI_S1_RESTART_DECISION_V3_CANDIDATE.json"),
        (baseline_path, package / "candidate/CONTROLLED_BASELINE_V2_CANDIDATE.json"),
        (output_dir / "FINAL_CONTROL_TARGET_SET_V2.json", package / "candidate/FINAL_CONTROL_TARGET_SET_V2.json"),
        (output_dir / "FRAMEWORK_MANIFEST_V2_CANDIDATE.sha256", package / "candidate/FRAMEWORK_MANIFEST_V2_CANDIDATE.sha256"),
        (output_dir / "PREFLIGHT_V4.json", package / "PREFLIGHT_V4.json"),
    ):
        _copy_new(source, dest)
    for name in (
        "HOOK_POLICY_V1.json",
        "G1_EVIDENCE_CORRECTION_V2.json",
        "G1_EVIDENCE_CORRECTION_V2_RERUN1.json",
        "GOVERNANCE_TEST_RESULTS_V2.json",
        "HUMAN_ONLY_TREE_BEFORE_V2.json",
        "HUMAN_ONLY_TREE_AFTER_V2.json",
        "HUMAN_ONLY_TREE_DIFF_V2.json",
        "CURRENT_REMEDIATION_CYCLE_V2.json",
        "HUMAN_ONLY_TREE_BEFORE_V2_RERUN1.json",
        "HUMAN_ONLY_TREE_AFTER_V2_RERUN1.json",
        "HUMAN_ONLY_TREE_DIFF_V2_RERUN1.json",
        "G3_PREAPPLY_AUDIT_FAIL_V1.json",
        "PROTECTED_TREE_BEFORE_V2.json",
    ):
        source = evidence / name
        if source.is_file():
            _copy_new(source, package / "evidence" / name)
    rows = []
    for file in sorted(package.rglob("*")):
        if file.is_file():
            rows.append({"path": file.relative_to(package).as_posix(), "sha256": _sha(file)})
    manifest_path = package / "REVIEW_PACKAGE_MANIFEST.json"
    _write_json(manifest_path, {"schema": "JOVI_AUTOMATION_REVIEW_PACKAGE_MANIFEST_V4", "files": rows})
    _write_new(package / "REVIEW_PACKAGE_MANIFEST.json.sha256.sidecar", (_sha(manifest_path) + "  REVIEW_PACKAGE_MANIFEST.json\n").encode("ascii"))

    return {
        "status": "G2_CANDIDATES_FROZEN",
        "output_dir": str(output_dir),
        "decision_candidate_sha256": _sha(decision_path),
        "controlled_baseline_candidate_sha256": _sha(baseline_path),
        "final_control_target_set_sha256": _sha(output_dir / "FINAL_CONTROL_TARGET_SET_V2.json"),
        "preflight_run_id": run_id,
        "framework_mismatch_count": len(mismatches),
        "review_package_manifest_sha256": _sha(manifest_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output or root / "workspace/review-queue/commerce-v1/governance-v2"
    result = generate(root, output)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
