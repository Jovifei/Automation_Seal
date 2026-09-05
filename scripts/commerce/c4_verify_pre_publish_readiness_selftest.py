#!/usr/bin/env python3
"""Self-test for c4_verify_pre_publish_readiness.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


READY = "C4_PRE_PUBLISH_QA_READY_FOR_HUMAN_DECISION"
FLAGS = [
    "production_integration_allowed",
    "real_payment",
    "real_customer",
    "xianyu",
    "auto_delivery",
    "n8n_production",
]
GATES = [
    "c3_runtime_git_reconciliation",
    "c3_runtime_evidence_integrity",
    "product_zero_write",
    "product_head_binding",
    "installer_binding",
    "portable_binding",
    "delivery_package_binding",
    "listing_claim_review",
    "customer_package_inventory",
    "xianyu_human_rule_check",
    "release_posture_human_choice",
    "delivery_transport_frozen",
    "privacy_minimization",
    "six_real_action_flags_false",
    "governance_pr_ci_status",
]


def run(verifier: Path, contract: Path, readiness: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(verifier), str(contract), str(readiness), *extra],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: selftest.py VERIFIER CONTRACT", file=sys.stderr)
        return 2

    verifier = Path(sys.argv[1]).resolve()
    contract = Path(sys.argv[2]).resolve()

    valid = {
        "schema_version": 1,
        "phase": "C4_PRE_PUBLISH_QA",
        "verdict": READY,
        "issued_from_human": False,
        "real_action_flags": {name: False for name in FLAGS},
        "gates": {name: {"status": "PASS", "evidence": [f"evidence/{name}.json"]} for name in GATES},
    }

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        valid_path = root / "valid.json"
        valid_path.write_text(json.dumps(valid, indent=2), encoding="utf-8")

        result = run(verifier, contract, valid_path, "--require-ready")
        assert result.returncode == 0, result.stderr
        assert READY in result.stdout

        pending = json.loads(json.dumps(valid))
        pending["verdict"] = "C4_PRE_PUBLISH_QA_PENDING"
        pending["gates"]["xianyu_human_rule_check"] = {"status": "PENDING", "evidence": []}
        pending_path = root / "pending.json"
        pending_path.write_text(json.dumps(pending, indent=2), encoding="utf-8")
        result = run(verifier, contract, pending_path)
        assert result.returncode == 0, result.stderr
        result = run(verifier, contract, pending_path, "--require-ready")
        assert result.returncode != 0

        bad_flag = json.loads(json.dumps(valid))
        bad_flag["real_action_flags"]["xianyu"] = True
        bad_flag_path = root / "bad_flag.json"
        bad_flag_path.write_text(json.dumps(bad_flag, indent=2), encoding="utf-8")
        result = run(verifier, contract, bad_flag_path)
        assert result.returncode != 0

        missing_evidence = json.loads(json.dumps(valid))
        missing_evidence["gates"]["listing_claim_review"]["evidence"] = []
        missing_evidence_path = root / "missing_evidence.json"
        missing_evidence_path.write_text(json.dumps(missing_evidence, indent=2), encoding="utf-8")
        result = run(verifier, contract, missing_evidence_path)
        assert result.returncode != 0

        forged_human = json.loads(json.dumps(valid))
        forged_human["issued_from_human"] = True
        forged_human_path = root / "forged_human.json"
        forged_human_path.write_text(json.dumps(forged_human, indent=2), encoding="utf-8")
        result = run(verifier, contract, forged_human_path)
        assert result.returncode != 0

    print("C4_PRE_PUBLISH_VERIFIER_SELFTEST_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
