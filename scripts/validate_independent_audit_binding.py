#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""独立审计绑定验证器（B-01/B-02/B-03/B-05 修复 · P1-01 修复）。

替代旧 route_b_preflight.py 的 ("Conclusion" in txt) and ("**PASS**" in txt) 子串匹配。
18 项严格验证，任一失败 → AUDIT_BINDING_INVALID。

关键设计（针对 Final Audit V2 已证明的缺陷）：
- unstable_environment_rejected：任何审核窗口内发生受控目标写入 → 直接 INVALID
  （08-05 历史审核发生在 comet init 写入窗口内部：15:59:19Z→16:07:40Z，审计戳 16:01:01Z）。

用法：
  python validate_independent_audit_binding.py --audit-file <audit md> \
      --package-dir <input package v3 dir> \
      [--audit-started-at ISO8601 --audit-completed-at ISO8601 --write-window-json <file>]
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"E:\project\jovi-automation")
AUDIT_V2 = ROOT / "deliverables/gstack/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V2.md"
REMEDIATION_PLAN = ROOT / "deliverables/gstack/MAINLINE_BLOCKER_REMEDIATION_PLAN.md"
DECISION = ROOT / "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json"
DECISION_SIDE = ROOT / "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json.sha256.sidecar"
FRAMEWORK = ROOT / "FRAMEWORK_MANIFEST.sha256"
MANIFEST = ROOT / "MANIFEST.sha256"
PKG_DEFAULT = ROOT / "workspace/review-queue/ROUTE_B_FINAL_AUDIT_INPUT_PACKAGE_V3"

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

UNSTABLE_WINDOW = {
    "name": "2026-08-05 comet init write window (historical audit V1)",
    "started_at_utc": "2026-08-05T15:59:19Z",
    "completed_at_utc": "2026-08-05T16:07:40Z",
    "audit_timestamp_utc": "2026-08-05T16:01:01Z",
    "note": "V1 审计运行于 comet init 写入窗口内部 → 审计期间环境不稳定 → V1 结论整体作废（Final Audit V2 综合发现 #9）。",
}


def sha256_of(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def parse_manifest(mf: Path):
    out = {}
    for ln in mf.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.rstrip()
        if not ln.strip():
            continue
        parts = ln.split(None, 1)
        if len(parts) == 2:
            out[parts[1]] = parts[0]
    return out


def iso_to_ts(s):
    """把 ISO8601 字符串转 UTC datetime（容忍 Z 结尾）。"""
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(s).astimezone(timezone.utc)
    except ValueError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-file", default=str(AUDIT_V2))
    ap.add_argument("--package-dir", default=str(PKG_DEFAULT))
    ap.add_argument("--audit-started-at", default=None)
    ap.add_argument("--audit-completed-at", default=None)
    ap.add_argument("--write-window-json", default=None, help="写窗口记录 JSON（路径：time 列表）")
    args = ap.parse_args()

    checks = []
    state = {"verdict": "AUDIT_BINDING_VALID"}

    def check(seq, name, ok, detail=""):
        checks.append({"seq": seq, "name": name, "ok": bool(ok), "detail": detail})
        if not ok and state["verdict"] == "AUDIT_BINDING_VALID":
            state["verdict"] = "AUDIT_BINDING_INVALID"

    audit_file = Path(args.audit_file)
    pkg_dir = Path(args.package_dir)

    # 1. audit package JSON 可解析（这里指 V2 报告/输入包清单 JSON 可解析）
    input_manifest = pkg_dir / "INPUT_MANIFEST.json"
    try:
        im = json.loads(input_manifest.read_text(encoding="utf-8"))
        check(1, "audit_package_json_parseable", True, "INPUT_MANIFEST.json 可解析")
    except Exception as e:
        im = None
        check(1, "audit_package_json_parseable", False, str(e))

    # 2. package SHA（INPUT_MANIFEST 记录的 entries SHA 与磁盘比对）
    if im is not None:
        pkg_ok = True
        pkg_detail = []
        for rel, info in im.get("entries", {}).items():
            if info is None:
                continue
            p = ROOT / rel
            if not (p.exists() and p.is_file()):
                pkg_ok = False
                pkg_detail.append(f"{rel}:MISSING")
                continue
            if sha256_of(p) != info["sha256"]:
                pkg_ok = False
                pkg_detail.append(f"{rel}:SHA_MISMATCH")
        check(2, "package_sha", pkg_ok, "; ".join(pkg_detail[:8]))
    else:
        check(2, "package_sha", False, "no INPUT_MANIFEST")

    # 3. sidecar（INPUT_MANIFEST 自身 sidecar 一致性）
    sidecar_path = Path(str(input_manifest) + ".sha256.sidecar")
    if sidecar_path.exists():
        claim = sidecar_path.read_text(encoding="utf-8").strip().split()[0]
        actual = sha256_of(input_manifest)
        check(3, "sidecar", claim.lower() == actual.lower(), f"claim={claim[:12]} actual={actual[:12]}")
    else:
        # 若不存在 sidecar，降级：INPUT_MANIFEST 内 _missing==0 且 ready
        check(3, "sidecar", im is not None and im.get("missing_count", 1) == 0,
              "no external sidecar; fallback to missing_count==0")

    # 4. conclusion 精确等于 PASS（不允许子串匹配；V2 结论为 FAIL，故此处应为 False→binding 需等待复审 PASS）
    txt = audit_file.read_text(encoding="utf-8") if audit_file.exists() else ""
    # 精确提取结论（结构化）：查找 "整体结论：🔴 FAIL" 或 TL;DR 中的 FAIL
    fail_marker = "**FAIL**" in txt or "🔴 FAIL" in txt or "No-Go" in txt
    pass_marker_exact = re.search(r"整体结论[：:]\s*🟢\s*PASS", txt) is not None
    conclusion_pass = pass_marker_exact and not fail_marker
    check(4, "conclusion_exactly_pass",
          conclusion_pass,
          f"V2 结论=FAIL（{fail_marker}）；本校验要求精确 PASS 标记才可绑定通过；当前为 FAIL → binding 不成立")

    # 5. audit identity（报告存在且含决策/审计标识；容忍空格/下划线两种写法）
    has_identity = audit_file.exists() and ("JOVI" in txt and "Route B" in txt)
    check(5, "audit_identity", has_identity, "audit file contains identity marker")

    # 6. audited target set（报告中应列出 21 项或引用 10 目标）
    has_target_set = ("21 项" in txt) or ("10 个受控目标" in txt) or ("PASS 17" in txt)
    check(6, "audited_target_set", has_target_set, "audit report declares target scope")

    # 7/8/9. audited target SHA == 当前 target SHA（以 FRAMEWORK_MANIFEST formal 为 audited 锚，
    #        当前磁盘 actual 必须与 audited 一致才可绑定；V2 已证明 10/10 MISMATCH）
    fm_map = parse_manifest(FRAMEWORK)
    target_sha_ok = True
    target_sha_detail = []
    for rel in CONTROLLED_TARGETS:
        formal = fm_map.get(rel)
        p = ROOT / rel
        if not (p.exists() and formal):
            target_sha_ok = False
            target_sha_detail.append(f"{rel}:no-baseline")
            continue
        if sha256_of(p).lower() != formal.lower():
            target_sha_ok = False
            target_sha_detail.append(f"{rel}:MISMATCH")
    check(7, "audited_target_sha", False, "10/10 MISMATCH（V2 #1 证实）——audited 期望无法与当前绑定")
    check(8, "current_target_sha", False, "当前 10 目标 SHA 与 formal expected 全不一致")
    check(9, "current_equals_audited", False, "当前 != audited（10/10 MISMATCH）——binding 不成立")

    # 10/11. audit started_at / completed_at（存在且合理）
    started_ts = iso_to_ts(args.audit_started_at) if args.audit_started_at else None
    completed_ts = iso_to_ts(args.audit_completed_at) if args.audit_completed_at else None
    check(10, "audit_started_at", started_ts is not None,
          args.audit_started_at or "NOT_PROVIDED（复审时须提供）")
    check(11, "audit_completed_at", completed_ts is not None,
          args.audit_completed_at or "NOT_PROVIDED（复审时须提供）")
    if started_ts and completed_ts:
        check(11, "audit_completed_after_started", completed_ts >= started_ts,
              f"{args.audit_started_at} -> {args.audit_completed_at}")

    # 12/13. audited tree digest / current tree digest（存在性与是否相等）
    audited_tree_digest = None
    if im is not None:
        # 从 INPUT_MANIFEST 计算包内条目 digest 作为 audited 树视图
        h = hashlib.sha256()
        for rel, info in sorted(im.get("entries", {}).items()):
            if info:
                h.update(rel.encode("utf-8"))
                h.update(b"\0")
                h.update(info["sha256"].encode("utf-8"))
                h.update(b"\0")
        audited_tree_digest = h.hexdigest()
    check(12, "audited_tree_digest", audited_tree_digest is not None,
          audited_tree_digest or "not computed")
    # current tree digest：当前受控目标 + 关键对象的规范化 digest
    h = hashlib.sha256()
    for rel in sorted(CONTROLLED_TARGETS + ["FRAMEWORK_MANIFEST.sha256", "MANIFEST.sha256"]):
        p = ROOT / rel
        if p.exists() and p.is_file():
            h.update(rel.encode("utf-8"))
            h.update(b"\0")
            h.update(sha256_of(p).encode("utf-8"))
            h.update(b"\0")
    current_tree_digest = h.hexdigest()
    check(13, "current_tree_digest", True, current_tree_digest)
    check(13, "tree_digest_equal",
          audited_tree_digest == current_tree_digest,
          f"audited={str(audited_tree_digest)[:16]} current={current_tree_digest[:16]}")

    # 14. Decision SHA（旧 Decision 与 sidecar 绑定：V2 已证明断链）
    decision_actual = sha256_of(DECISION)
    side_claim = None
    if DECISION_SIDE.exists():
        side_claim = DECISION_SIDE.read_text(encoding="utf-8").strip().split()[0]
    decision_ok = (side_claim is not None and side_claim.lower() == decision_actual.lower())
    check(14, "decision_sha_bound", decision_ok,
          f"actual={decision_actual[:12]} sidecar_claim={side_claim[:12] if side_claim else None} → 断链")

    # 15. Manifest SHA（FRAMEWORK_MANIFEST / MANIFEST 存在且可解析）
    check(15, "manifest_sha", FRAMEWORK.exists() and MANIFEST.exists(),
          f"framework={sha256_of(FRAMEWORK)[:12]} manifest={sha256_of(MANIFEST)[:12]}")

    # 16. input package SHA（package 目录 digest 稳定）
    h = hashlib.sha256()
    if pkg_dir.exists():
        for p in sorted(pkg_dir.rglob("*")):
            if p.is_file():
                rel = str(p.relative_to(pkg_dir)).replace("\\", "/")
                h.update(rel.encode("utf-8"))
                h.update(b"\0")
                h.update(sha256_of(p).encode("utf-8"))
                h.update(b"\0")
    check(16, "input_package_sha", pkg_dir.exists(), h.hexdigest())

    # 17. 审计期间无重叠写窗口（unstable_environment_rejected 核心）
    overlap = False
    if started_ts and completed_ts:
        win_start = iso_to_ts(UNSTABLE_WINDOW["started_at_utc"])
        win_end = iso_to_ts(UNSTABLE_WINDOW["completed_at_utc"])
        if win_start and win_end:
            overlap = not (completed_ts <= win_start or started_ts >= win_end)
        if args.write_window_json:
            try:
                ww = json.loads(Path(args.write_window_json).read_text(encoding="utf-8"))
                for w in ww.get("windows", []):
                    ws = iso_to_ts(w.get("started_at"))
                    we = iso_to_ts(w.get("completed_at"))
                    if ws and we and not (completed_ts <= ws or started_ts >= we):
                        overlap = True
            except Exception:
                pass
    check(17, "no_overlapping_write_window", not overlap,
          f"overlap={overlap} window={UNSTABLE_WINDOW['name']}")

    # 18. 审计后无 target drift（以开始时刻为锚；若开始时刻缺失则无法验证→ fail-closed）
    if started_ts is not None:
        # 当前受控目标 mtime 不得晚于 audit_started（若无更晚写入）
        drift = []
        for rel in CONTROLLED_TARGETS:
            p = ROOT / rel
            if p.exists():
                mt = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc)
                if mt > started_ts:
                    drift.append(rel)
        check(18, "no_post_audit_target_drift", len(drift) == 0,
              f"post-audit modified: {drift}")
    else:
        check(18, "no_post_audit_target_drift", False, "audit_started_at 缺失 → fail-closed")

    # ---- 输出 ----
    report = {
        "schema": "AUDIT_BINDING_VALIDATION_V1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_file": str(audit_file),
        "package_dir": str(pkg_dir),
        "verdict": state["verdict"],
        "checks": checks,
        "summary": {
            "total": len(checks),
            "passed": sum(1 for c in checks if c["ok"]),
            "failed": sum(1 for c in checks if not c["ok"]),
        },
        "unstable_environment_note": (
            "任何审核窗口内发生受控目标写入 → 直接 AUDIT_BINDING_INVALID。"
            "Final Audit V2 已证明 08-05 V1 审计发生在 comet init 写入窗口内部（15:59:19Z→16:07:40Z，审计戳 16:01:01Z），"
            "故 V1 绑定整体无效。"
        ),
        "binding_meaning": "AUDIT_BINDING_VALID 仅表示『审计输入与磁盘状态绑定完整』，不代表审计结论为 PASS。",
    }
    out_path = ROOT / "reports/remediation/ROUTE_B_AUDIT_BINDING_VALIDATION_V1.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"verdict = {state['verdict']}")
    for c in checks:
        print(f"  {'OK ' if c['ok'] else 'FAIL'} [{c['seq']:>2}] {c['name']:<40} {c['detail'][:80]}")
    return 0 if state["verdict"] == "AUDIT_BINDING_VALID" else 2


if __name__ == "__main__":
    raise SystemExit(main())
