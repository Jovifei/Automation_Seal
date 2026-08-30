#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True)
ap.add_argument("--audit", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()
repo = Path(args.repo).resolve()
audit = json.loads(Path(args.audit).read_text(encoding="utf-8-sig"))
out = Path(args.out)
out.mkdir(parents=True, exist_ok=True)
changes = [
    {"id": "XY-001", "action": "bind admin port to 127.0.0.1", "required": True},
    {"id": "XY-002", "action": "remove or loopback-bind VNC/noVNC ports", "required": True},
    {"id": "XY-003", "action": "replace default admin/JWT/encryption secrets", "required": True},
    {"id": "XY-004", "action": "disable public registration", "required": True},
    {"id": "XY-005", "action": "disable auto reply, AI reply and auto delivery", "required": True},
    {"id": "XY-006", "action": "disable remote slider and fallback automation", "required": True},
    {"id": "XY-007", "action": "disable automatic hot update", "required": True},
    {"id": "XY-008", "action": "pin local commit and image tag/digest", "required": True},
    {
        "id": "XY-009",
        "action": "remove whole-repo rw mount after image-content test",
        "required": False,
    },
    {
        "id": "XY-010",
        "action": "evaluate non-root container after filesystem permission test",
        "required": False,
    },
    {
        "id": "XY-011",
        "action": "backup SQLite, browser_data and configs before change",
        "required": True,
    },
]
plan = {
    "schema_version": 1,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "stage": "X1_PROPOSAL_ONLY",
    "local_repo": str(repo),
    "audit_path": str(Path(args.audit)),
    "changes": changes,
    "apply_policy": "create parallel files only; never overwrite original compose; no restart",
    "license_status": "PENDING_LICENSE_CLARIFICATION",
    "status": "AWAITING_HUMAN_APPROVAL",
}
plan_path = out / "hardening-plan.json"
plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
h = hashlib.sha256(plan_path.read_bytes()).hexdigest()
(out / "hardening-plan.sha256.txt").write_text(h + "\n", encoding="ascii")
proposal = """# Generated proposal - do not copy blindly\n# Target Codex must build docker-compose.jovi-hardened.yml from the local compose.\n# Required environment defaults:\nAUTO_REPLY_ENABLED=false\nAI_REPLY_ENABLED=false\nAUTO_DELIVERY_ENABLED=false\nUSER_REGISTRATION_ENABLED=false\nENABLE_VNC=false\nXY_SLIDER_REMOTE_ENABLED=false\nXY_SLIDER_DRISSION_FALLBACK=false\n# Required secrets supplied manually:\nADMIN_PASSWORD=<USER_SETS_LOCALLY>\nJWT_SECRET_KEY=<USER_SETS_LOCALLY>\nSECRET_ENCRYPTION_KEY=<USER_SETS_LOCALLY>\n"""
(out / "hardening-env.proposal.txt").write_text(proposal, encoding="utf-8")
print(plan_path)
