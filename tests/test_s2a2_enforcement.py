from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "workspace/review-queue/commerce-v1/governance-closeout-v14"


class V14S2A2EnforcementTests(unittest.TestCase):
    def test_candidate_never_authorizes_tracks_or_platform_actions(self) -> None:
        decision = json.loads((PACKAGE / "DECISION_V14_PROPOSED.json").read_text(encoding="utf-8"))
        self.assertFalse(decision["track_p_allowed"])
        self.assertFalse(decision["track_i_allowed"])
        self.assertFalse(decision["real_platform_actions_allowed"])
        self.assertEqual("DO_NOT_TRUST", decision["hook_status"])

    def test_forbidden_targets_are_explicit(self) -> None:
        target_set = json.loads((PACKAGE / "inputs/V14_STRUCTURAL_TARGET_SET.json").read_text(encoding="utf-8"))
        self.assertIn("MANIFEST.sha256", target_set["forbidden_scope"])
        self.assertIn("scripts/human-only/**", target_set["forbidden_scope"])


if __name__ == "__main__":
    unittest.main()
