"""Regression contract for the isolated Security semantics entrypoint candidate."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "run-security-semantics.py"
SOURCE_PATH = ROOT / "tests" / "test_s2a1_control_plane.py"
BASELINE_PATH = (
    ROOT / "reports" / "remediation" / "QH1_REVISION_V3_ACCEPTED_CURRENT_SOURCE_BASELINE_V1.json"
)
SPEC = importlib.util.spec_from_file_location("security_semantics_entrypoint", RUNNER_PATH)
assert SPEC and SPEC.loader
ENTRYPOINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ENTRYPOINT)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


PROTECTED_SNAPSHOT_PATHS = (
    ".codex/hooks.json",
    "FRAMEWORK_MANIFEST.sha256",
    "MANIFEST.sha256",
    "CODEX_START_PROMPT.txt",
    "PROJECT_STATE.json",
    "STATUS.md",
    "scripts/authorize_action.py",
    "scripts/control_plane.py",
    "scripts/codex/pre_tool_guard.py",
    "scripts/codex/Invoke-PreToolGuard.ps1",
    "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json",
    "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json.sha256.sidecar",
)

AUTHORIZED_G1_FILES = {
    "scripts/authorize_action.py",
    "scripts/codex/pre_tool_guard.py",
    "scripts/control_plane.py",
    "scripts/generate_gate_a_plan.py",
    "tests/hooks/test_pre_tool_guard.py",
    "tests/test_s1_integrity.py",
    "tests/test_s2a1_control_plane.py",
    "tests/test_s2a2_enforcement.py",
}


def _protected_tree() -> dict[str, str]:
    return {
        relative: _sha256(ROOT / relative)
        for relative in PROTECTED_SNAPSHOT_PATHS
        if (ROOT / relative).is_file()
    }


class SecuritySemanticsEntrypointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_hash = _sha256(SOURCE_PATH)
        cls.initial_pyc = sorted(
            path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*.pyc")
        )
        cls.initial_pycache = sorted(
            path.relative_to(ROOT).as_posix() for path in ROOT.rglob("__pycache__")
        )
        cls.initial_tree = _protected_tree()

    def invoke(self) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PYTHONUTF8"] = "1"
        return subprocess.run(
            [sys.executable, "-B", str(RUNNER_PATH)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=ENTRYPOINT.TIMEOUT_SECONDS + 10,
            shell=False,
            env=environment,
            check=False,
        )

    def result(self) -> tuple[subprocess.CompletedProcess[str], dict]:
        completed = self.invoke()
        return completed, json.loads(completed.stdout)

    def test_01_entrypoint_file_exists_in_candidate(self) -> None:
        self.assertTrue(RUNNER_PATH.is_file())

    def test_02_expected_ids_exactly_20(self) -> None:
        self.assertEqual(20, len(ENTRYPOINT.EXPECTED_TEST_IDS))

    def test_03_expected_ids_are_test_01_to_test_20(self) -> None:
        self.assertTrue(
            all(
                value.startswith(f"test_{number:02d}_")
                for number, value in enumerate(ENTRYPOINT.EXPECTED_TEST_IDS, 1)
            )
        )

    def test_04_no_test_21_selected(self) -> None:
        self.assertNotIn(
            "test_21_legacy_entry_fails", ENTRYPOINT.EXPECTED_TEST_IDS
        )

    def test_05_no_wildcard_selection(self) -> None:
        self.assertTrue(all("*" not in value for value in ENTRYPOINT._node_ids(ENTRYPOINT.EXPECTED_TEST_IDS)))

    def test_06_no_directory_wide_test_run(self) -> None:
        self.assertTrue(
            all(
                value.startswith("tests.test_s2a1_control_plane.S2A1CoreTests.")
                for value in ENTRYPOINT._node_ids(ENTRYPOINT.EXPECTED_TEST_IDS)
            )
        )

    def test_07_success_returns_exit_zero(self) -> None:
        completed, _ = self.result()
        self.assertEqual(0, completed.returncode)

    def test_08_success_stdout_is_single_json(self) -> None:
        completed, payload = self.result()
        self.assertEqual(
            json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")),
            completed.stdout,
        )

    def test_09_success_stderr_is_empty(self) -> None:
        completed, _ = self.result()
        self.assertEqual("", completed.stderr)

    def test_10_success_reports_20_of_20(self) -> None:
        _, payload = self.result()
        self.assertEqual("20/20 PASS", payload["summary"])

    def test_11_missing_test_fails(self) -> None:
        self.assertFalse(ENTRYPOINT.validate_expected_ids(ENTRYPOINT.EXPECTED_TEST_IDS[:-1]))

    def test_12_extra_test_fails(self) -> None:
        self.assertFalse(
            ENTRYPOINT.validate_expected_ids(
                ENTRYPOINT.EXPECTED_TEST_IDS + ("test_21_legacy_entry_fails",)
            )
        )

    def test_13_duplicate_test_fails(self) -> None:
        self.assertFalse(
            ENTRYPOINT.validate_expected_ids(
                ENTRYPOINT.EXPECTED_TEST_IDS[:-1] + (ENTRYPOINT.EXPECTED_TEST_IDS[0],)
            )
        )

    def test_14_reordered_result_is_handled_deterministically(self) -> None:
        reversed_ids = tuple(reversed(ENTRYPOINT.EXPECTED_TEST_IDS))
        self.assertFalse(ENTRYPOINT.validate_expected_ids(reversed_ids))
        self.assertEqual(
            "expected_test_ids_not_exactly_frozen_20",
            ENTRYPOINT.run_entrypoint(reversed_ids)["diagnostic"],
        )

    def strict_result(self, **changes) -> dict:
        payload = {
            "expected_count": 20,
            "collected_count": 20,
            "expected_test_ids": list(ENTRYPOINT.EXPECTED_TEST_IDS),
            "collected_test_ids": list(ENTRYPOINT.EXPECTED_TEST_IDS),
            "passed": 20,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "xfailed": 0,
            "xpassed": 0,
            "not_run": 0,
            "child_exit_code": 0,
            "stderr_bytes": 0,
            "captured_stdout_bytes": 0,
            "captured_stderr_bytes": 0,
        }
        payload.update(changes)
        return payload

    def test_15_failed_test_fails_entrypoint(self) -> None:
        self.assertFalse(ENTRYPOINT.is_strict_pass(self.strict_result(passed=19, failed=1)))

    def test_16_skipped_test_fails_entrypoint(self) -> None:
        self.assertFalse(ENTRYPOINT.is_strict_pass(self.strict_result(passed=19, skipped=1)))

    def test_17_xfailed_test_fails_entrypoint(self) -> None:
        self.assertFalse(ENTRYPOINT.is_strict_pass(self.strict_result(passed=19, xfailed=1)))

    def test_18_not_run_test_fails_entrypoint(self) -> None:
        self.assertFalse(ENTRYPOINT.is_strict_pass(self.strict_result(passed=19, not_run=1)))

    def test_19_wrong_collected_count_fails(self) -> None:
        self.assertFalse(ENTRYPOINT.is_strict_pass(self.strict_result(collected_count=19)))

    def test_20_nonzero_child_exit_fails(self) -> None:
        result = ENTRYPOINT.evaluate_child_process(
            ENTRYPOINT.EXPECTED_TEST_IDS,
            SimpleNamespace(returncode=1, stdout="{}", stderr=""),
            1,
        )
        self.assertEqual("SECURITY_SEMANTICS_FAIL", result["status"])

    def test_21_unexpected_stderr_fails(self) -> None:
        child = {
            "collected_test_ids": list(ENTRYPOINT.EXPECTED_TEST_IDS),
            "passed": 20, "failed": 0, "errors": 0, "skipped": 0,
            "xfailed": 0, "xpassed": 0, "not_run": 0,
            "runner_output_sha256": "0" * 64,
            "captured_stdout_bytes": 0, "captured_stderr_bytes": 0,
        }
        raw = json.dumps(child, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        result = ENTRYPOINT.evaluate_child_process(
            ENTRYPOINT.EXPECTED_TEST_IDS,
            SimpleNamespace(returncode=0, stdout=raw, stderr="unexpected"),
            1,
        )
        self.assertEqual("SECURITY_SEMANTICS_FAIL", result["status"])

    def test_22_malformed_result_fails(self) -> None:
        result = ENTRYPOINT.evaluate_child_process(
            ENTRYPOINT.EXPECTED_TEST_IDS,
            SimpleNamespace(returncode=0, stdout="not-json", stderr=""),
            1,
        )
        self.assertEqual("SECURITY_SEMANTICS_FAIL", result["status"])

    def test_23_timeout_fails(self) -> None:
        def timeout_runner(*_args, **_kwargs):
            raise subprocess.TimeoutExpired("python", 1)
        self.assertEqual(
            "SECURITY_SEMANTICS_FAIL",
            ENTRYPOINT.run_entrypoint(runner=timeout_runner)["status"],
        )

    def test_24_no_pyc_created(self) -> None:
        self.assertEqual(
            self.initial_pyc,
            sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*.pyc")),
        )

    def test_25_no_pycache_created(self) -> None:
        self.assertEqual(
            self.initial_pycache,
            sorted(
                path.relative_to(ROOT).as_posix() for path in ROOT.rglob("__pycache__")
            ),
        )

    def test_26_accepted_20_baseline_files_unchanged(self) -> None:
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        for item in baseline["accepted_files"]:
            if item["relative_path"] in AUTHORIZED_G1_FILES:
                continue
            with self.subTest(path=item["relative_path"]):
                self.assertEqual(item["accepted_current_sha256"], _sha256(ROOT / item["relative_path"]))

    def test_27_source_test_file_unchanged(self) -> None:
        self.assertEqual(self.source_hash, _sha256(SOURCE_PATH))

    def test_28_project_tree_zero_drift(self) -> None:
        current = _protected_tree()
        self.assertEqual(self.initial_tree, current)

    def test_29_machine_json_schema_valid(self) -> None:
        _, payload = self.result()
        for key in (
            "schema_version", "entrypoint", "source_test_file", "expected_test_ids",
            "collected_test_ids", "expected_count", "collected_count", "passed",
            "failed", "errors", "skipped", "xfailed", "xpassed", "not_run",
            "exit_code", "status", "duration_ms", "stdout_sha256", "stderr_sha256",
        ):
            self.assertIn(key, payload)
        self.assertEqual("SECURITY_SEMANTICS_PASS", payload["status"])

    def test_30_direct_real_run_is_20_of_20(self) -> None:
        completed, payload = self.result()
        self.assertEqual(0, completed.returncode)
        self.assertEqual(20, payload["collected_count"])
        self.assertEqual(20, payload["passed"])

    def test_31_zero_drift_scope_excludes_mutable_outputs(self) -> None:
        self.assertFalse(any(path.startswith("reports/") for path in self.initial_tree))
        self.assertFalse(any(path.startswith("workspace/review-queue/") for path in self.initial_tree))


if __name__ == "__main__":
    unittest.main(verbosity=2)
