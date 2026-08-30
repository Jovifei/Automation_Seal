from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V14GateReadinessFacadeTests(unittest.TestCase):
    def test_validator_facade_exposes_the_v14_cli_without_writes(self) -> None:
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/validate_commerce_gate_readiness.py"), "--help"], text=True, capture_output=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("--phase", result.stdout)

    def test_generator_facade_exposes_bound_input_contract_without_writes(self) -> None:
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/generate_gate_a_plan.py"), "--help"], text=True, capture_output=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("--closeout", result.stdout)


if __name__ == "__main__":
    unittest.main()
