#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--gate", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--evidence", action="append", default=[])
parser.add_argument("--next-phase", required=True)
parser.add_argument("--track", choices=["P", "I", "X", "GENERAL"], default="GENERAL")
parser.add_argument("--action", action="append", default=[])
args = parser.parse_args()

out = Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)
data = {
    "schema_version": 2,
    "gate": args.gate,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "evidence": args.evidence,
    "tracks": {
        args.track: {
            "next_phase": args.next_phase,
            "actions": args.action,
            "status": "AWAITING_HUMAN_APPROVAL",
        }
    },
    "constraints": [
        "no external platform writes",
        "no secrets in reports",
        "human approval receipt bound to the exact plan SHA256 and track",
    ],
}
out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
digest = hashlib.sha256(out.read_bytes()).hexdigest()
out.with_suffix(".sha256.txt").write_text(digest + "\n", encoding="ascii")
print(f"{out}: {digest}")
