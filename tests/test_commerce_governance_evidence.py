from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_commerce_predecision_readiness import hook_policy_errors


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "workspace/review-queue/commerce-v1/audit-remediation-v2"


class CommerceGovernanceEvidenceTests(unittest.TestCase):
    def test_hook_policy_candidate_is_explicit_and_closed(self) -> None:
        path = EVIDENCE / "HOOK_POLICY_V1.json"
        self.assertTrue(path.is_file())
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual([], hook_policy_errors(payload))

    def test_machine_report_is_authoritative_for_final_count(self) -> None:
        path = EVIDENCE / "GOVERNANCE_TEST_RESULTS_V2.json"
        self.assertTrue(path.is_file())
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(118, payload["passed"])
        self.assertEqual(118, payload["collected"])
        self.assertEqual("GOVERNANCE_TEST_RESULTS_V2.json", payload["authority"])

        todo = (ROOT / "tasks/todo.md").read_text(encoding="utf-8")
        self.assertRegex(todo, r"G1\.5.*116/116 PASS")
        self.assertRegex(todo, r"G1\.7.*118/118 PASS")
        self.assertNotRegex(todo, r"authoritative_final_result\s*=\s*116/116")

    def test_old_history_remains_not_verified(self) -> None:
        path = EVIDENCE / "G1_EVIDENCE_CORRECTION_V2.json"
        self.assertTrue(path.is_file())
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual("NOT_VERIFIED", payload["original_g1_history"])
        self.assertEqual("PASS_ZERO_DRIFT", payload["new_v2_remediation_cycle"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

