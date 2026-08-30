#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--root", required=True)
parser.add_argument("--gate", required=True)
parser.add_argument("--track", required=True, choices=["P", "I", "X", "GENERAL"])
args = parser.parse_args()
root = Path(args.root).resolve()
plan = root / "reports" / "gates" / f"{args.gate}_PLAN.json"
receipt = root / "workspace" / "approvals" / f"{args.gate}.{args.track}.approval.json"
if not plan.exists() or not receipt.exists():
    print(f"missing plan or approval receipt for {args.gate}.{args.track}", file=sys.stderr)
    raise SystemExit(2)
current = hashlib.sha256(plan.read_bytes()).hexdigest()
try:
    plan_data = json.loads(plan.read_text(encoding="utf-8-sig"))
    receipt_data = json.loads(receipt.read_text(encoding="utf-8-sig"))
except Exception as exc:
    print(f"invalid plan or receipt JSON: {exc}", file=sys.stderr)
    raise SystemExit(3)
if plan_data.get("gate") != args.gate or args.track not in plan_data.get("tracks", {}):
    print("plan does not contain requested gate/track", file=sys.stderr)
    raise SystemExit(4)
if (
    receipt_data.get("gate") != args.gate
    or receipt_data.get("track") != args.track
    or str(receipt_data.get("plan_sha256", "")).lower() != current
):
    print("approval receipt does not match current plan and track", file=sys.stderr)
    raise SystemExit(5)
print(f"[PASS] {args.gate}.{args.track} approval verified: {current}")
