from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "workspace/review-queue/commerce-v1/governance-closeout-v14"


class V14S1IntegrityTests(unittest.TestCase):
    def test_framework_candidate_has_exactly_forty_entries(self) -> None:
        rows = [line for line in (PACKAGE / "inputs/FRAMEWORK_MANIFEST_V14_CANDIDATE.sha256").read_text(encoding="ascii").splitlines() if line]
        self.assertEqual(40, len(rows))
        self.assertEqual(40, len({line.split("  ", 1)[1] for line in rows}))

    def test_transaction_is_seven_structural_targets_plus_framework(self) -> None:
        target = json.loads((PACKAGE / "inputs/V14_STRUCTURAL_TARGET_SET.json").read_text(encoding="utf-8"))
        self.assertEqual(7, target["target_count"])
        self.assertEqual(8, target["transaction_target_count"])
        self.assertEqual("FRAMEWORK_MANIFEST.sha256", target["manifest_target"]["path"])
        self.assertIn("MANIFEST.sha256", target["forbidden_scope"])


if __name__ == "__main__":
    unittest.main()
