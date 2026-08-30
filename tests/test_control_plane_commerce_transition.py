from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V14TransitionFacadeTests(unittest.TestCase):
    def test_transition_facade_exposes_check_apply_rollback_and_recover_modes(self) -> None:
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/apply_commerce_control_plane_transition.py"), "--help"], text=True, capture_output=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)
        for token in ("--check", "--apply", "--rollback", "--recover"):
            self.assertIn(token, result.stdout)


if __name__ == "__main__":
    unittest.main()
