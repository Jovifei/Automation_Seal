from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_commerce_predecision_readiness import (
    hook_policy_errors,
    validate_predecision_readiness,
    verify_human_only_cycle,
)


ROOT = Path(__file__).resolve().parents[1]


class CommercePredecisionReadinessTests(unittest.TestCase):
    def test_hook_policy_requires_all_explicit_false_fields(self) -> None:
        payload = {
            "schema_version": 1,
            "authority": "CANDIDATE_ONLY",
            "status": "DO_NOT_TRUST",
            "hook_runtime_dependency": False,
            "hook_trust_allowed": False,
        }
        errors = hook_policy_errors(payload, require_candidate_metadata=True)
        self.assertTrue(any("hook_restore_allowed" in item for item in errors))

    def test_hook_policy_rejects_unknown_and_true_fields(self) -> None:
        payload = {
            "schema_version": 1,
            "authority": "CANDIDATE_ONLY",
            "status": "DO_NOT_TRUST",
            "hook_runtime_dependency": False,
            "hook_restore_allowed": True,
            "hook_trust_allowed": False,
            "unexpected": False,
        }
        errors = hook_policy_errors(payload, require_candidate_metadata=True)
        self.assertTrue(any("unknown" in item for item in errors))
        self.assertTrue(any("hook_restore_allowed" in item for item in errors))

    def test_human_only_cycle_rejects_byte_drift(self) -> None:
        with tempfile.TemporaryDirectory(prefix="jovi-human-only-") as temp:
            root = Path(temp)
            before = root / "before.json"
            after = root / "after.json"
            diff = root / "diff.json"
            before.write_text(
                json.dumps(
                    {
                        "historical_g1_before": "NOT_VERIFIED",
                        "new_v2_cycle_before": "VERIFIED",
                        "entries": [
                            {"path": "scripts/human-only/a.ps1", "bytes": 1, "sha256": "a" * 64, "reparse": False}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            after.write_text(
                json.dumps(
                    {
                        "entries": [
                            {"path": "scripts/human-only/a.ps1", "bytes": 2, "sha256": "b" * 64, "reparse": False}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            diff.write_text(json.dumps({"status": "PASS_ZERO_DRIFT", "changed": []}), encoding="utf-8")
            errors = verify_human_only_cycle(root, before, after, diff)
            self.assertTrue(any("drift" in item.lower() for item in errors))

    def test_current_tree_is_predecision_ready_after_g2_package(self) -> None:
        errors = validate_predecision_readiness(
            ROOT, ROOT / "workspace/review-queue/commerce-v1/governance-v2"
        )
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)
