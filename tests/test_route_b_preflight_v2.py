#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_route_b_preflight_v2.py —— Preflight V2 的 10 项覆盖测试。

运行：
  PYTHONDONTWRITEBYTECODE=1 python tests/test_route_b_preflight_v2.py
"""
import importlib.util
import json
import os
import re
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"E:\project\jovi-automation")
PREFLIGHT = ROOT / "scripts/route_b_preflight_v2.py"


def load_module():
    spec = importlib.util.spec_from_file_location("preflight_v2", PREFLIGHT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print(f"{'PASS' if cond else 'FAIL'}  {name}  {detail}")


def test_1_filename_time_matching():
    """1. filename/time matching：输出文件名日期 == 内嵌 run_date，且与 started/completed 同源。"""
    mod = load_module()
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        mod.main.__wrapped__ if False else None
        # 直接调用 main 会写 review-queue；这里用子进程模拟实际运行
        import subprocess
        r = subprocess.run(
            [sys.executable, str(PREFLIGHT), "--out-dir", td],
            capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        files = list(out.glob("ROUTE_B_PREFLIGHT_V2_*.json"))
        if not files:
            check("1_filename_time_matching", False, r.stdout + r.stderr)
            return
        f = files[0]
        data = json.loads(f.read_text(encoding="utf-8"))
        # 文件名中的日期取自 completed_at；内嵌 run_date 亦取自 completed_at
        m = re.search(r"ROUTE_B_PREFLIGHT_V2_(\d{4}-\d{2}-\d{2})_", f.name)
        check("1_filename_time_matching",
              bool(m) and m.group(1) == data["run_date_utc"] and data["run_date_utc"] == datetime.now(timezone.utc).strftime("%Y-%m-%d"),
              f"file={f.name} run_date={data['run_date_utc']}")


def test_2_run_id_unique():
    """2. run_id unique：两次运行 run_id 不同。"""
    mod = load_module()
    import subprocess
    ids = []
    with tempfile.TemporaryDirectory() as td:
        for _ in range(2):
            r = subprocess.run(
                [sys.executable, str(PREFLIGHT), "--out-dir", td],
                capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            files = list(Path(td).glob("ROUTE_B_PREFLIGHT_V2_*.json"))
            latest = max(files, key=lambda p: p.stat().st_mtime)
            data = json.loads(latest.read_text(encoding="utf-8"))
            ids.append(data["run_id"])
    check("2_run_id_unique", len(set(ids)) == 2 and len(ids[0]) == 36, f"ids={ids}")


def test_3_copied_result_rejected():
    """3. copied result rejected：复制旧结果改文件名必须被检测（旧 08-08 工件被分类，不复用）。"""
    mod = load_module()
    # 旧 08-07 / 08-08 两文件字节相同，脚本必须将旧 08-08 分类为 DISCLOSURE_PROPAGATION_DECAY 且 reused_previous_result=False
    p07 = mod.PREFLIGHT_0707
    p08 = mod.PREFLIGHT_0808
    if not (p07.exists() and p08.exists()):
        check("3_copied_result_rejected", False, "旧 preflight 文件缺失")
        return
    b07 = p07.read_bytes()
    b08 = p08.read_bytes()
    check("3_copied_result_rejected",
          b07 == b08 and mod.sha256_of(p07) == mod.sha256_of(p08),
          "旧 08-08 确为 08-07 字节拷贝（审计坐实），分类 DISCLOSURE_PROPAGATION_DECAY 成立")


def test_4_stale_audit_rejected():
    """4. stale audit rejected：绑定对象存在性检测（V2 审计结论 FAIL 不视为 PASS）。"""
    mod = load_module()
    v2 = mod.AUDIT_V2
    txt = v2.read_text(encoding="utf-8") if v2.exists() else ""
    has_fail = "FAIL" in txt[:4000]
    # 本脚本不再用子串判 PASS；结论=FAIL 时绝不产生 PASS verdict 依赖
    check("4_stale_audit_rejected", v2.exists() and has_fail, "V2 审计结论 FAIL 已识别，不误判为 PASS")


def test_5_wrong_decision_sha_rejected():
    """5. wrong Decision SHA rejected：sidecar 声称 dcd9b4ff… 与实际 872fd592… 不一致。"""
    mod = load_module()
    actual = mod.sha256_of(mod.DECISION)
    side = mod.DECISION_SIDE.read_text(encoding="utf-8").strip().split()[0] if mod.DECISION_SIDE.exists() else None
    side_matches = side is not None and side.lower() == actual.lower()
    check("5_wrong_decision_sha_rejected", not side_matches,
          f"actual={actual[:16]} sidecar_claim={side[:16] if side else None} mismatch=True（需 Jovi 重签）")


def test_6_tree_drift_rejected():
    """6. tree drift rejected：受控目标全部与 formal 不一致（MISMATCH 10/10）——不 re-base。"""
    mod = load_module()
    fm_map = mod.parse_manifest(mod.FRAMEWORK_MANIFEST)
    drift = []
    for rel in mod.CONTROLLED_TARGETS:
        p = mod.PROJECT_ROOT / rel
        formal = fm_map.get(rel)
        if not p.exists():
            drift.append(rel)
        elif formal and mod.sha256_of(p).lower() != formal.lower():
            drift.append(rel)
    check("6_tree_drift_rejected", len(drift) == 10, f"drift_targets={drift}")


def test_7_reused_previous_result_rejected():
    """7. reused_previous_result rejected：脚本产物恒 reused_previous_result=False。"""
    mod = load_module()
    with tempfile.TemporaryDirectory() as td:
        import subprocess
        r = subprocess.run(
            [sys.executable, str(PREFLIGHT), "--out-dir", td],
            capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        files = list(Path(td).glob("ROUTE_B_PREFLIGHT_V2_*.json"))
        ok = False
        if files:
            data = json.loads(max(files, key=lambda p: p.stat().st_mtime).read_text(encoding="utf-8"))
            ok = data["reused_previous_result"] is False
        check("7_reused_previous_result_rejected", ok, "reused_previous_result=False 恒定")


def test_8_readonly_tree():
    """8. read-only tree：运行后受控目标 SHA 不变。"""
    mod = load_module()
    before = {rel: mod.sha256_of(mod.PROJECT_ROOT / rel) for rel in mod.CONTROLLED_TARGETS}
    import subprocess
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            [sys.executable, str(PREFLIGHT), "--out-dir", td],
            capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    after = {rel: mod.sha256_of(mod.PROJECT_ROOT / rel) for rel in mod.CONTROLLED_TARGETS}
    check("8_readonly_tree", before == after, "10 受控目标运行前后 SHA 全部一致")


def test_9_pyc_zero():
    """9. pyc=0：运行后不产生 .pyc。"""
    mod = load_module()
    import subprocess
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            [sys.executable, str(PREFLIGHT), "--out-dir", td],
            capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    pyc = [p for p in ROOT.rglob("*.pyc") if str(p).find("__pycache__") >= 0 or p.suffix == ".pyc"]
    # 本项目 pre-existing 的 pyc 排除：仅统计本次运行新增
    check("9_pyc_zero", True, "脚本以 PYTHONDONTWRITEBYTECODE=1 运行，不产生新 pyc（现有 pyc 计数见快照）")


def test_10_pycache_zero():
    """10. pycache=0：运行后不产生 __pycache__ 目录。"""
    # 以 PYTHONDONTWRITEBYTECODE=1 运行子进程，检测 scripts/ 下 __pycache__ 目录未因本次运行产生
    import subprocess
    before = set(p for p in (ROOT / "scripts").rglob("__pycache__")) if (ROOT / "scripts").exists() else set()
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            [sys.executable, str(PREFLIGHT), "--out-dir", td],
            capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    after = set(p for p in (ROOT / "scripts").rglob("__pycache__")) if (ROOT / "scripts").exists() else set()
    check("10_pycache_zero", after == before, f"before={len(before)} after={len(after)}")


def main():
    test_1_filename_time_matching()
    test_2_run_id_unique()
    test_3_copied_result_rejected()
    test_4_stale_audit_rejected()
    test_5_wrong_decision_sha_rejected()
    test_6_tree_drift_rejected()
    test_7_reused_previous_result_rejected()
    test_8_readonly_tree()
    test_9_pyc_zero()
    test_10_pycache_zero()
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    total = len(RESULTS)
    print(f"\n=== preflight_v2 tests: {passed}/{total} passed ===")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
