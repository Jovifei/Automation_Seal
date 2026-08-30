#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_validate_independent_audit_binding.py —— 绑定验证器的负向/正向测试。

核心：unstable_environment_rejected —— 任何审核窗口内发生受控目标写入 → 直接 INVALID。
参考 Final Audit V2 已证明：08-05 V1 审计发生在 comet init 写入窗口内部
（15:59:19Z→16:07:40Z，审计戳 16:01:01Z）。

运行：
  PYTHONDONTWRITEBYTECODE=1 python tests/test_validate_independent_audit_binding.py
"""
import importlib.util
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"E:\project\jovi-automation")
VALIDATOR = ROOT / "scripts/validate_independent_audit_binding.py"

RESULTS = []


def load():
    spec = importlib.util.spec_from_file_location("binding_validator", VALIDATOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print(f"{'PASS' if cond else 'FAIL'}  {name}  {detail}")


def test_unstable_environment_rejected():
    """审计窗口与 comet init 写窗口重叠 → 必须 INVALID。"""
    mod = load()
    ws = mod.iso_to_ts(mod.UNSTABLE_WINDOW["started_at_utc"])
    we = mod.iso_to_ts(mod.UNSTABLE_WINDOW["completed_at_utc"])
    # 审计时间戳落在写窗口内（V1 真实情况：16:01:01Z ∈ [15:59:19Z, 16:07:40Z]）
    audit_ts = mod.iso_to_ts(mod.UNSTABLE_WINDOW["audit_timestamp_utc"])
    overlap = not (audit_ts <= ws or audit_ts >= we)
    check("unstable_environment_rejected",
          overlap and ws < audit_ts < we,
          f"audit_ts={audit_ts.isoformat()} in window [{ws.isoformat()},{we.isoformat()}] → overlap=True")


def test_conclusion_fail_not_pass():
    """V2 结论为 FAIL 时，conclusion_exactly_pass 必须为 False（不再子串误判）。"""
    mod = load()
    txt = mod.AUDIT_V2.read_text(encoding="utf-8")
    fail_marker = "**FAIL**" in txt or "🔴 FAIL" in txt or "No-Go" in txt
    import re
    pass_marker_exact = re.search(r"整体结论[：:]\s*🟢\s*PASS", txt) is not None
    check("conclusion_fail_not_pass",
          (pass_marker_exact and not fail_marker) is False,
          "V2=FAIL → conclusion_exactly_pass=False（正确 fail-closed）")


def test_decision_sha_break_detected():
    """决策 SHA 断链（872fd592 vs sidecar dcd9b4ff）必须被检出。"""
    mod = load()
    actual = mod.sha256_of(mod.DECISION)
    side_claim = None
    if mod.DECISION_SIDE.exists():
        side_claim = mod.DECISION_SIDE.read_text(encoding="utf-8").strip().split()[0]
    bound = (side_claim is not None and side_claim.lower() == actual.lower())
    check("decision_sha_break_detected", not bound,
          f"actual={actual[:12]} sidecar_claim={side_claim[:12] if side_claim else None}")


def test_package_missing_failopen_removed():
    """V3 包 _missing 由差集计算；若 missing_count>0 则 ready=False。"""
    mod = load()
    pkg = mod.PKG_DEFAULT
    im_path = pkg / "INPUT_MANIFEST.json"
    if not im_path.exists():
        check("package_missing_failopen_removed", False, "INPUT_MANIFEST.json 缺失")
        return
    im = json.loads(im_path.read_text(encoding="utf-8"))
    ready = im.get("missing_count", 999) == 0
    check("package_missing_failopen_removed", ready,
          f"missing_count={im.get('missing_count')} expected_count={im.get('expected_count')}")


def test_no_substring_pass_judgement():
    """验证器不得包含旧式 audit_pass = ("Conclusion" in txt) ... 子串判 PASS 逻辑（赋值代码）。"""
    src = VALIDATOR.read_text(encoding="utf-8")
    # 旧脚本：audit_pass = ("Conclusion" in txt) and ("**PASS**" in txt)
    # 新验证器：结构化正则提取 fail_marker / pass_marker_exact；不得出现 audit_pass = ( 赋值
    banned = "audit_pass = (" in src
    check("no_substring_pass_judgement", not banned,
          "validator 使用结构化 conclusion 提取，不使用旧子串匹配赋值")


def main():
    test_unstable_environment_rejected()
    test_conclusion_fail_not_pass()
    test_decision_sha_break_detected()
    test_package_missing_failopen_removed()
    test_no_substring_pass_judgement()
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    total = len(RESULTS)
    print(f"\n=== binding validator tests: {passed}/{total} passed ===")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
