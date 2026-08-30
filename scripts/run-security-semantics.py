#!/usr/bin/env python3
"""Run exactly the named Security semantics 20/20 regression contract."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINT = "scripts/run-security-semantics.py"
SOURCE_TEST_FILE = "tests/test_s2a1_control_plane.py"
SOURCE_TEST_CLASS = "S2A1CoreTests"
TIMEOUT_SECONDS = 30
EXPECTED_TEST_IDS = (
    "test_01_registry_has_required_controls",
    "test_02_registry_missing_control_fails",
    "test_03_registry_self_classification_required",
    "test_04_absolute_control_path_fails",
    "test_05_traversal_control_path_fails",
    "test_06_case_collision_fails",
    "test_07_state_schema_is_valid",
    "test_08_unknown_state_fails",
    "test_09_illegal_state_tuple_fails",
    "test_10_initial_predecessor_fails",
    "test_11_revision_replay_fails",
    "test_12_revision_rollback_fails",
    "test_13_closed_to_prepare_fails",
    "test_14_blocked_to_ready_fails",
    "test_15_prepare_to_apply_without_approval_fails",
    "test_16_permission_expansion_requires_distinct_binding",
    "test_17_project_state_is_mirror",
    "test_18_status_only_tamper_fails",
    "test_19_project_only_tamper_fails",
    "test_20_prompt_only_tamper_fails",
)
CHILD_PROGRAM = r"""
import contextlib
import importlib.util
import io
import json
import sys
import unittest
from pathlib import Path

root = Path(sys.argv[1])
expected = json.loads(sys.argv[2])
source = root / "tests" / "test_s2a1_control_plane.py"
payload = {
    "schema_version": 1,
    "source_test_file": "tests/test_s2a1_control_plane.py",
    "collected_test_ids": [],
    "passed": 0,
    "failed": 0,
    "errors": 0,
    "skipped": 0,
    "xfailed": 0,
    "xpassed": 0,
    "not_run": len(expected),
    "runner_output_sha256": None,
    "captured_stdout_bytes": 0,
    "captured_stderr_bytes": 0,
}
try:
    spec = importlib.util.spec_from_file_location("security_semantics_source", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("source_test_module_load_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    case_type = getattr(module, "S2A1CoreTests")
    suite = unittest.TestSuite()
    for test_id in expected:
        method = getattr(case_type, test_id, None)
        if method is None or not callable(method):
            raise RuntimeError("missing_expected_test:" + test_id)
        payload["collected_test_ids"].append(test_id)
        suite.addTest(case_type(test_id))
    runner_stream = io.StringIO()
    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()
    with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
        result = unittest.TextTestRunner(stream=runner_stream, verbosity=0).run(suite)
    runner_output = runner_stream.getvalue()
    payload.update(
        {
            "passed": result.testsRun - len(result.failures) - len(result.errors)
            - len(result.skipped) - len(result.expectedFailures) - len(result.unexpectedSuccesses),
            "failed": len(result.failures),
            "errors": len(result.errors),
            "skipped": len(result.skipped),
            "xfailed": len(result.expectedFailures),
            "xpassed": len(result.unexpectedSuccesses),
            "not_run": len(expected) - result.testsRun,
            "runner_output_sha256": __import__("hashlib").sha256(
                runner_output.encode("utf-8")
            ).hexdigest(),
            "captured_stdout_bytes": len(captured_stdout.getvalue().encode("utf-8")),
            "captured_stderr_bytes": len(captured_stderr.getvalue().encode("utf-8")),
        }
    )
except Exception as exc:
    payload["diagnostic"] = type(exc).__name__ + ":" + str(exc)
sys.stdout.write(json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
"""


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _node_ids(expected_ids: Iterable[str]) -> tuple[str, ...]:
    return tuple(
        "tests.test_s2a1_control_plane."
        + SOURCE_TEST_CLASS
        + "."
        + test_id
        for test_id in expected_ids
    )


def validate_expected_ids(expected_ids: Iterable[str]) -> bool:
    values = tuple(expected_ids)
    return (
        values == EXPECTED_TEST_IDS
        and len(values) == 20
        and len(set(values)) == 20
        and all(value.startswith(f"test_{index:02d}_") for index, value in enumerate(values, 1))
    )


def is_strict_pass(result: dict[str, Any]) -> bool:
    return (
        result.get("expected_count") == 20
        and result.get("collected_count") == 20
        and tuple(result.get("expected_test_ids", ())) == EXPECTED_TEST_IDS
        and tuple(result.get("collected_test_ids", ())) == EXPECTED_TEST_IDS
        and result.get("passed") == 20
        and result.get("failed") == 0
        and result.get("errors") == 0
        and result.get("skipped") == 0
        and result.get("xfailed") == 0
        and result.get("xpassed") == 0
        and result.get("not_run") == 0
        and result.get("child_exit_code") == 0
        and result.get("stderr_bytes") == 0
        and result.get("captured_stdout_bytes") == 0
        and result.get("captured_stderr_bytes") == 0
    )


def _base_result(expected_ids: tuple[str, ...]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "entrypoint": ENTRYPOINT,
        "source_test_file": SOURCE_TEST_FILE,
        "expected_test_ids": list(expected_ids),
        "collected_test_ids": [],
        "selected_node_ids": list(_node_ids(expected_ids)),
        "expected_count": len(expected_ids),
        "collected_count": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "skipped": 0,
        "xfailed": 0,
        "xpassed": 0,
        "not_run": len(expected_ids),
        "child_exit_code": None,
        "stderr_bytes": 0,
        "stdout_sha256": None,
        "stderr_sha256": None,
        "runner_output_sha256": None,
        "captured_stdout_bytes": 0,
        "captured_stderr_bytes": 0,
        "duration_ms": 0,
        "status": "SECURITY_SEMANTICS_FAIL",
        "summary": "SECURITY_SEMANTICS_FAIL",
        "exit_code": 1,
    }


def evaluate_child_process(
    expected_ids: Iterable[str], completed: Any, duration_ms: int
) -> dict[str, Any]:
    expected = tuple(expected_ids)
    result = _base_result(expected)
    stdout = getattr(completed, "stdout", "")
    stderr = getattr(completed, "stderr", "")
    result["duration_ms"] = duration_ms
    result["child_exit_code"] = getattr(completed, "returncode", None)
    result["stderr_bytes"] = len(stderr.encode("utf-8"))
    result["stdout_sha256"] = _sha256_bytes(stdout.encode("utf-8"))
    result["stderr_sha256"] = _sha256_bytes(stderr.encode("utf-8"))
    if not validate_expected_ids(expected):
        result["diagnostic"] = "expected_test_ids_not_exactly_frozen_20"
        return result
    if not isinstance(stdout, str) or not isinstance(stderr, str):
        result["diagnostic"] = "child_stream_type_invalid"
        return result
    try:
        child = json.loads(stdout)
        if not isinstance(child, dict) or json.dumps(
            child, ensure_ascii=True, sort_keys=True, separators=(",", ":")
        ) != stdout:
            raise ValueError("child_stdout_is_not_single_canonical_json")
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        result["diagnostic"] = "child_result_invalid:" + type(exc).__name__
        return result
    for key in (
        "collected_test_ids",
        "passed",
        "failed",
        "errors",
        "skipped",
        "xfailed",
        "xpassed",
        "not_run",
        "runner_output_sha256",
        "captured_stdout_bytes",
        "captured_stderr_bytes",
    ):
        if key not in child:
            result["diagnostic"] = "child_result_missing:" + key
            return result
    result.update(
        {
            "collected_test_ids": child["collected_test_ids"],
            "collected_count": len(child["collected_test_ids"]),
            "passed": child["passed"],
            "failed": child["failed"],
            "errors": child["errors"],
            "skipped": child["skipped"],
            "xfailed": child["xfailed"],
            "xpassed": child["xpassed"],
            "not_run": child["not_run"],
            "runner_output_sha256": child["runner_output_sha256"],
            "captured_stdout_bytes": child["captured_stdout_bytes"],
            "captured_stderr_bytes": child["captured_stderr_bytes"],
        }
    )
    if is_strict_pass(result):
        result.update(
            {
                "status": "SECURITY_SEMANTICS_PASS",
                "summary": "20/20 PASS",
                "exit_code": 0,
            }
        )
    else:
        result["diagnostic"] = "strict_contract_not_satisfied"
    return result


def run_entrypoint(
    expected_ids: Iterable[str] = EXPECTED_TEST_IDS,
    runner: Callable[..., Any] = subprocess.run,
) -> dict[str, Any]:
    expected = tuple(expected_ids)
    if not validate_expected_ids(expected):
        result = _base_result(expected)
        result["diagnostic"] = "expected_test_ids_not_exactly_frozen_20"
        return result
    environment = dict(__import__("os").environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONUTF8"] = "1"
    started = time.monotonic()
    try:
        completed = runner(
            [
                sys.executable,
                "-B",
                "-c",
                CHILD_PROGRAM,
                str(ROOT),
                json.dumps(list(expected), ensure_ascii=True, separators=(",", ":")),
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=TIMEOUT_SECONDS,
            shell=False,
            env=environment,
            check=False,
        )
    except subprocess.TimeoutExpired:
        result = _base_result(expected)
        result["duration_ms"] = int((time.monotonic() - started) * 1000)
        result["diagnostic"] = "child_timeout"
        return result
    return evaluate_child_process(
        expected, completed, int((time.monotonic() - started) * 1000)
    )


def main() -> int:
    result = run_entrypoint()
    sys.stdout.write(
        json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    )
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
