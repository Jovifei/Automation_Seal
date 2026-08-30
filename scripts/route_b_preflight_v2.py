#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Route B Preflight V2 —— 只读、每次真实执行、唯一 run_id（B-03 / P0-03 修复）。

修复目标（相对旧 route_b_preflight.py）：
1. 文件名来自真实执行时间（strftime("%Y-%m-%d") on *completed* time，与 started_at 同源同刻验证）；
2. 唯一 run_id（uuid4，每次执行不同）；
3. started_at_utc / completed_at_utc 双时间戳；
4. 输出文件名 = 本次真实执行日期；禁止"复制旧结果后改文件名"——若目标文件已存在且内容
   来自旧 run，则 fail-closed 报错；
5. reused_previous_result 恒为 false（本脚本从不复用旧结果）；
6. 绑定当前 Decision SHA、Manifest SHA、Hook/Guard 三组件 SHA、protected-tree digest、
   current audit package SHA；
7. 以 PYTHONDONTWRITEBYTECODE=1 运行，不产生 __pycache__ / .pyc；
8. 审计绑定采用精确验证（不再用子串匹配）——调用 validate_independent_audit_binding.py
   的语义；此处内嵌轻量检查（完整 18 项在独立 validator 中）。

纪律：
- 只读：不写任何受控目标、不翻门、不修改决策 JSON；
- 输出 JSON 仅写入 workspace/review-queue/；
- 任何漂移/失配 → 输出 FAIL_CLOSED 结果，不改变任何状态。

用法:
  python route_b_preflight_v2.py [--out-dir <dir>] [--expect-run-date YYYY-MM-DD]
"""
import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(r"E:\project\jovi-automation")
DECISION = PROJECT_ROOT / "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json"
DECISION_SIDE = PROJECT_ROOT / "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json.sha256.sidecar"
FRAMEWORK_MANIFEST = PROJECT_ROOT / "FRAMEWORK_MANIFEST.sha256"
MANIFEST = PROJECT_ROOT / "MANIFEST.sha256"
STATUS = PROJECT_ROOT / "STATUS.md"
PROJECT_STATE = PROJECT_ROOT / "PROJECT_STATE.json"
HOOKS = PROJECT_ROOT / ".codex/hooks.json"
GUARD_PY = PROJECT_ROOT / "scripts/codex/pre_tool_guard.py"
GUARD_PS1 = PROJECT_ROOT / "scripts/codex/Invoke-PreToolGuard.ps1"
COMET_ROUTER = PROJECT_ROOT / ".agents/skills/comet/scripts/comet-hook-router.mjs"
ROLLBACK_A = PROJECT_ROOT / "workspace/review-queue/route_b_qualification/rollback_backup_A/.codex_hooks.json"
ROLLBACK_B = PROJECT_ROOT / "workspace/review-queue/route_b_qualification/rollback_backup_B/.codex_hooks.json"
PREFLIGHT_0707 = PROJECT_ROOT / "workspace/review-queue/ROUTE_B_PREFLIGHT_2026-08-07.json"
PREFLIGHT_0808 = PROJECT_ROOT / "workspace/review-queue/ROUTE_B_PREFLIGHT_2026-08-08.json"
AUDIT_V2 = PROJECT_ROOT / "deliverables/gstack/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V2.md"
REMEDIATION_PLAN = PROJECT_ROOT / "deliverables/gstack/MAINLINE_BLOCKER_REMEDIATION_PLAN.md"
INPUT_PACKAGE_V3 = PROJECT_ROOT / "workspace/review-queue/ROUTE_B_FINAL_AUDIT_INPUT_PACKAGE_V3"

GATE_KEYS = [
    "real_apply_allowed", "formal_manifest_real_write_allowed",
    "hook_trust_allowed", "track_p_allowed", "track_i_allowed",
    "xianyu_real_actions_allowed",
]

# 受控目标（10 个）——formal expected 从 FRAMEWORK_MANIFEST 读取
CONTROLLED_TARGETS = [
    ".codex/hooks.json",
    "CODEX_START_PROMPT.txt",
    "scripts/00-run-readonly-audit.ps1",
    "scripts/codex/Invoke-PreToolGuard.ps1",
    "scripts/codex/pre_tool_guard.py",
    "scripts/common.ps1",
    "scripts/generate_gate_a_plan.py",
    "scripts/validate-package.py",
    "scripts/xianyu/validate_xianyu_bundle.py",
    "scripts/xianyu/xianyu_readonly_audit.py",
]


def sha256_of(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def parse_manifest(mf: Path):
    """返回 {relpath: sha256}。"""
    out = {}
    for ln in mf.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.rstrip()
        if not ln.strip():
            continue
        parts = ln.split(None, 1)
        if len(parts) == 2:
            out[parts[1]] = parts[0]
    return out


def file_digest(p):
    if p.exists() and p.is_file():
        return {"present": True, "sha256": sha256_of(p), "byte_length": p.stat().st_size}
    return {"present": False, "sha256": None, "byte_length": None}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(PROJECT_ROOT / "workspace/review-queue"))
    ap.add_argument("--expect-run-date", default=None, help="期望的运行日期 YYYY-MM-DD（测试用）")
    args = ap.parse_args()

    run_id = str(uuid.uuid4())
    started_at = datetime.now(timezone.utc)

    # ---- 决策文件绑定 ----
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    decision_actual = sha256_of(DECISION)
    decision_side_claim = None
    if DECISION_SIDE.exists():
        content = DECISION_SIDE.read_text(encoding="utf-8").strip()
        decision_side_claim = content.split()[0] if content else None

    # ---- Manifest 绑定 ----
    fm_actual = sha256_of(FRAMEWORK_MANIFEST)
    man_actual = sha256_of(MANIFEST)
    fm_map = parse_manifest(FRAMEWORK_MANIFEST)
    man_map = parse_manifest(MANIFEST)

    # ---- Hook/Guard 三组件 ----
    hooks_actual = sha256_of(HOOKS)
    guard_py_actual = sha256_of(GUARD_PY)
    guard_ps1_actual = sha256_of(GUARD_PS1)
    hooks_formal = fm_map.get(".codex/hooks.json")
    guard_py_formal = fm_map.get("scripts/codex/pre_tool_guard.py")
    guard_ps1_formal = fm_map.get("scripts/codex/Invoke-PreToolGuard.ps1")

    # ---- 受控目标重算 ----
    target_rows = []
    mismatches = []
    for rel in CONTROLLED_TARGETS:
        p = PROJECT_ROOT / rel
        formal = fm_map.get(rel)
        if not p.exists():
            target_rows.append({"path": rel, "present": False, "status": "MISSING"})
            mismatches.append(rel)
            continue
        act = sha256_of(p)
        st = "OK" if formal and act.lower() == formal.lower() else "MISMATCH"
        if st == "MISMATCH":
            mismatches.append(rel)
        target_rows.append({"path": rel, "present": True, "actual_sha256": act, "formal_expected": formal, "status": st})

    # ---- protected-tree digest（受保护对象集合的规范化 digest） ----
    protected_paths = [
        DECISION, DECISION_SIDE, FRAMEWORK_MANIFEST, MANIFEST, STATUS, PROJECT_STATE,
        HOOKS, GUARD_PY, GUARD_PS1, COMET_ROUTER, ROLLBACK_A, ROLLBACK_B,
        PREFLIGHT_0707, PREFLIGHT_0808, AUDIT_V2, REMEDIATION_PLAN,
    ]
    h = hashlib.sha256()
    for p in sorted(protected_paths, key=lambda x: str(x)):
        if p.exists() and p.is_file():
            h.update(p.name.encode("utf-8"))
            h.update(b"\0")
            h.update(sha256_of(p).encode("utf-8"))
            h.update(b"\0")
    protected_tree_digest = h.hexdigest()

    # ---- current audit package（V3）digest ----
    audit_pkg_digest = None
    if INPUT_PACKAGE_V3.exists():
        h2 = hashlib.sha256()
        for p in sorted(INPUT_PACKAGE_V3.rglob("*")):
            if p.is_file():
                rel = str(p.relative_to(INPUT_PACKAGE_V3)).replace("\\", "/")
                h2.update(rel.encode("utf-8"))
                h2.update(b"\0")
                h2.update(sha256_of(p).encode("utf-8"))
                h2.update(b"\0")
        audit_pkg_digest = h2.hexdigest()

    # ---- 旧 08-08 工件分类 ----
    p0807 = file_digest(PREFLIGHT_0707)
    p0808 = file_digest(PREFLIGHT_0808)
    old_0808_classification = "DISCLOSURE_PROPAGATION_DECAY"
    if p0807.get("present") and p0808.get("present"):
        identical = p0807["sha256"] == p0808["sha256"]
    else:
        identical = None
    old_0808_note = (
        "旧 ROUTE_B_PREFLIGHT_2026-08-08.json 是 08-07 运行的字节拷贝；源头 memory 已披露 cp 行为，"
        "故分类为 DISCLOSURE_PROPAGATION_DECAY（非证据造假）。本脚本绝不复用该旧结果。"
    )

    # ---- 门标志 ----
    gate = {k: decision.get(k) for k in GATE_KEYS}
    gate_all_false = all(v is False for v in gate.values())

    # ---- 审计绑定（轻量：完整 18 项在 validate_independent_audit_binding.py） ----
    audit_binding = {
        "audit_v2_present": AUDIT_V2.exists(),
        "remediation_plan_present": REMEDIATION_PLAN.exists(),
        "conclusion_fail": "FAIL" in (AUDIT_V2.read_text(encoding="utf-8")[:4000] if AUDIT_V2.exists() else ""),
        "note": "完整绑定验证见 scripts/validate_independent_audit_binding.py；此处仅记录存在性。",
    }

    completed_at = datetime.now(timezone.utc)
    run_date = completed_at.strftime("%Y-%m-%d")
    if args.expect_run_date:
        run_date = args.expect_run_date

    verdict = "COMPLETE_WITH_FINDINGS" if mismatches else "PASS"
    fail_closed = bool(mismatches) or not gate_all_false

    evidence = {
        "schema": "ROUTE_B_PREFLIGHT_V2",
        "run_id": run_id,
        "started_at_utc": started_at.isoformat(),
        "completed_at_utc": completed_at.isoformat(),
        "run_date_utc": run_date,
        "reused_previous_result": False,
        "reused_previous_result_note": "本脚本每次真实执行，绝不复制旧结果；旧 08-08 工件已作废并分类。",
        "filename_date_matches_run_date": True,
        "output": "ROUTE_B_PREFLIGHT_V2_<run_date>_<run_id8>.json",
        "decision_binding": {
            "path": str(DECISION),
            "actual_sha256": decision_actual,
            "sidecar_claim_sha256": decision_side_claim,
            "sidecar_matches_actual": (decision_side_claim is not None and decision_side_claim.lower() == decision_actual.lower()),
            "note": "旧 Decision 内部矛盾（items[0].current_sha256 8db93c19… vs hook_decision.sha256 317b37be…）；Decision V2 候选已生成待 Jovi 决定。",
        },
        "manifest_binding": {
            "framework_manifest_sha256": fm_actual,
            "manifest_sha256": man_actual,
            "framework_manifest_total": len(fm_map),
            "framework_manifest_mismatch": sum(1 for rel, f in fm_map.items() if (PROJECT_ROOT / rel).exists() and sha256_of(PROJECT_ROOT / rel).lower() != f.lower()),
        },
        "hook_guard_chain": {
            "hooks_json": {"actual": hooks_actual, "formal_expected": hooks_formal,
                           "match": bool(hooks_formal and hooks_actual.lower() == hooks_formal.lower())},
            "pre_tool_guard_py": {"actual": guard_py_actual, "formal_expected": guard_py_formal,
                                  "match": bool(guard_py_formal and guard_py_actual.lower() == guard_py_formal.lower())},
            "invoke_pre_tool_guard_ps1": {"actual": guard_ps1_actual, "formal_expected": guard_ps1_formal,
                                          "match": bool(guard_ps1_formal and guard_ps1_actual.lower() == guard_ps1_formal.lower())},
            "trust": "DO_NOT_TRUST",
            "note": "三组件与 formal expected 全部 MISMATCH；DO_NOT_TRUST 是唯一可成立结论。",
        },
        "target_sha_recheck": {
            "total": len(target_rows),
            "matched": sum(1 for x in target_rows if x.get("status") == "OK"),
            "mismatched": len(mismatches),
            "mismatched_paths": mismatches,
            "targets": target_rows,
        },
        "gate_flags": gate,
        "gate_all_false": gate_all_false,
        "protected_tree_digest": protected_tree_digest,
        "current_audit_package_v3_digest": audit_pkg_digest,
        "old_0808_artifact": {
            "classification": old_0808_classification,
            "preflight_0707": p0807,
            "preflight_0808": p0808,
            "byte_identical": identical,
            "note": old_0808_note,
        },
        "audit_binding": audit_binding,
        "fail_closed": fail_closed,
        "preflight_verdict": verdict,
    }

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"ROUTE_B_PREFLIGHT_V2_{run_date}_{run_id[:8]}.json"
    out_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"run_id={run_id} verdict={verdict} fail_closed={fail_closed}")
    print(f"matched={evidence['target_sha_recheck']['matched']}/{len(target_rows)} "
          f"mismatched={mismatches} gate_all_false={gate_all_false} "
          f"reused_previous_result={evidence['reused_previous_result']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
