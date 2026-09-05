#!/usr/bin/env python3
"""Validate a C4 pre-publish readiness record against the governance contract.

This verifier is intentionally dependency-free. It validates structure and the
critical fail-closed invariants for the agent terminal state. It does not
recompute local product/runtime evidence; local execution must do that before
writing the readiness record.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


READY = "C4_PRE_PUBLISH_QA_READY_FOR_HUMAN_DECISION"
ALLOWED_NON_READY = {"C4_PRE_PUBLISH_QA_PENDING", "C4_PRE_PUBLISH_QA_BLOCKED"}


class VerificationError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VerificationError(f"cannot parse JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise VerificationError(f"top-level JSON must be object: {path}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def verify(contract: dict[str, Any], readiness: dict[str, Any], require_ready: bool) -> None:
    require(contract.get("success_stop") == READY, "contract success_stop mismatch")

    required_gates = contract.get("required_gates")
    require(isinstance(required_gates, list) and required_gates, "contract required_gates missing")
    require(all(isinstance(x, str) and x for x in required_gates), "invalid required gate name")

    flag_names = contract.get("real_action_flags")
    require(isinstance(flag_names, list) and flag_names, "contract real_action_flags missing")

    require(readiness.get("phase") == "C4_PRE_PUBLISH_QA", "readiness phase mismatch")
    verdict = readiness.get("verdict")
    require(verdict == READY or verdict in ALLOWED_NON_READY, f"unsupported verdict: {verdict!r}")

    issued = readiness.get("issued_from_human")
    require(issued is False, "C4 readiness must keep issued_from_human=false")

    flags = readiness.get("real_action_flags")
    require(isinstance(flags, dict), "real_action_flags must be an object")
    for name in flag_names:
        require(name in flags, f"missing real-action flag: {name}")
        require(flags[name] is False, f"real-action flag must remain false: {name}")

    gates = readiness.get("gates")
    require(isinstance(gates, dict), "gates must be an object")

    allowed_gate_states = set(contract.get("allowed_gate_states", []))
    require(allowed_gate_states >= {"PASS", "PENDING", "BLOCKED"}, "contract gate states incomplete")

    for name in required_gates:
        require(name in gates, f"missing required gate: {name}")
        gate = gates[name]
        require(isinstance(gate, dict), f"gate must be object: {name}")
        status = gate.get("status")
        require(status in allowed_gate_states, f"invalid gate status {name}: {status!r}")
        evidence = gate.get("evidence")
        require(isinstance(evidence, list), f"gate evidence must be list: {name}")
        if status == "PASS":
            require(bool(evidence), f"PASS gate must cite evidence: {name}")
            require(all(isinstance(x, str) and x.strip() for x in evidence), f"invalid evidence path: {name}")

    if verdict == READY:
        non_pass = [name for name in required_gates if gates[name].get("status") != "PASS"]
        require(not non_pass, f"READY verdict has non-PASS gates: {', '.join(non_pass)}")

    if require_ready:
        require(verdict == READY, f"not ready: verdict={verdict}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    parser.add_argument("readiness", type=Path)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()

    try:
        contract = load_json(args.contract)
        readiness = load_json(args.readiness)
        verify(contract, readiness, args.require_ready)
    except VerificationError as exc:
        print(f"C4_PRE_PUBLISH_READINESS_FAIL {exc}", file=sys.stderr)
        return 1

    print(f"C4_PRE_PUBLISH_READINESS_VALID verdict={readiness['verdict']}")
    if readiness["verdict"] == READY:
        print(READY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
