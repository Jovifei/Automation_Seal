#!/usr/bin/env python3
from __future__ import annotations

import argparse
from authorize_action import authorization_errors
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--root", required=True)
parser.add_argument("--stage", required=True)
parser.add_argument("--summary", required=True)
parser.add_argument("--next", required=True)
args = parser.parse_args()
root = Path(args.root).resolve()
authorization = authorization_errors(root, "status-write")
if authorization:
    print("[DENY] " + "; ".join(authorization), file=sys.stderr)
    raise SystemExit(2)
state_path = root / "PROJECT_STATE.json"
state = json.loads(state_path.read_text(encoding="utf-8-sig"))
state["current_state"] = args.stage
state["last_updated_at"] = datetime.now(timezone.utc).isoformat()
state["last_summary"] = args.summary
state["next_action"] = args.next
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
status = f"""# STATUS

- 包版本：V3.0 Final Handoff。
- 当前阶段：`{args.stage}`。
- 最近更新：{state["last_updated_at"]}。
- 最近结果：{args.summary}
- 下一步：{args.next}
- 永久边界：无自动发布、回复、发货、改价、退款或平台验证处理。
- 证据目录：`reports/`。
"""
(root / "STATUS.md").write_text(status, encoding="utf-8")
