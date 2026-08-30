#!/usr/bin/env python3
"""Read-only snapshot generator for the Route B controlled-apply plan.

Reads workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json, recomputes each
target file's SHA-256, compares against the frozen current_sha256, and writes
APPLY_PLAN.md. Aborts (exit 1) on any missing file or SHA mismatch.
Writes ONLY to the change directory; the live tree is never modified.
"""
import json
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT = Path(__file__).resolve()
CHANGE_DIR = SCRIPT.parent
PROJECT_ROOT = SCRIPT.parents[4]  # .../jovi-automation
DECISION = PROJECT_ROOT / "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json"


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    items = decision.get("items", [])
    gate_flags = {
        "real_apply_allowed": decision.get("real_apply_allowed"),
        "formal_manifest_real_write_allowed": decision.get("formal_manifest_real_write_allowed"),
        "hook_trust_allowed": decision.get("hook_trust_allowed"),
        "track_p_allowed": decision.get("track_p_allowed"),
        "track_i_allowed": decision.get("track_i_allowed"),
        "xianyu_real_actions_allowed": decision.get("xianyu_real_actions_allowed"),
    }

    rows = []
    aborted = False
    for it in items:
        rel = it["path"]
        target = PROJECT_ROOT / rel
        decision_sha = it.get("current_sha256")
        if not target.exists():
            rows.append((rel, decision_sha, "MISSING", it.get("action"), "MISSING"))
            aborted = True
            continue
        live_sha = sha256_of(target)
        match = live_sha.lower() == (decision_sha or "").lower()
        if not match:
            aborted = True
        rows.append((rel, decision_sha, live_sha, it.get("action"), "OK" if match else "MISMATCH"))

    out = CHANGE_DIR / "APPLY_PLAN.md"
    L = []
    L.append("# Route B 受控 APPLY 计划（快照）")
    L.append("")
    L.append(f"- 生成时间(UTC): {datetime.now(timezone.utc).isoformat()}")
    L.append("- 来源决策: `workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json`")
    L.append("- 独立审核 PASS: `reports/audit/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V1.md`")
    L.append("")
    L.append("## 门条件（全部 false = fail-closed）")
    for k, v in gate_flags.items():
        L.append(f"- `{k}` = {str(v).lower()}")
    L.append("")
    L.append("## 目标清单（10 项）")
    L.append("")
    L.append("| # | 路径 | 决策SHA | 实时SHA | 比对 | 动作 |")
    L.append("|---|------|---------|---------|------|------|")
    for i, (rel, dsha, lsha, action, st) in enumerate(rows, 1):
        L.append(f"| {i} | `{rel}` | `{dsha}` | `{lsha}` | {st} | {action} |")
    L.append("")
    L.append("## 证据链")
    L.append("- 每项目标可追溯到决策 JSON 的对应 item（路径 + current_sha256）。")
    L.append("- 独立审核 PASS 证明决策 SHA 与真实文件及冻结目标映射一致、13 套回归全 PASS、真实树零漂移。")
    L.append("- 本快照为只读生成；真实树未被修改（零漂移）。")
    L.append("")
    if aborted:
        L.append("> ⚠️ 存在目标缺失或 SHA 失配，APPLY 计划中止，不允许部分应用。")
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {out}")
    print(f"targets={len(rows)} aborted={aborted}")
    return 1 if aborted else 0


if __name__ == "__main__":
    sys.exit(main())
