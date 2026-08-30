#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JOVI-S1-ROUTE-B-FINAL-AUDIT-V2-P0-P1-REMEDIATION-V1 · 步骤一：保护快照（read-only）。

对受保护对象建立完整保护快照：
  - path / byte length / sha256 / mtime(UTC, iso) / reparse / is_dir
  - 对受控目标目录扫描 pyc / __pycache__ 残留
只读取，不写入任何真实树目标字节。输出写入 reports/remediation/。
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"E:\project\jovi-automation")
OUT_DIR = ROOT / "reports/remediation"
OUT_PATH = OUT_DIR / "ROUTE_B_PROTECTED_TREE_SNAPSHOT_BEFORE_V1.json"

# 10 个 S1 受控目标（来自 FRAMEWORK_MANIFEST.sha256 与决策文件 items）
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

# 其余受保护对象
OTHER_PATHS = [
    "FRAMEWORK_MANIFEST.sha256",
    "MANIFEST.sha256",
    "STATUS.md",
    "PROJECT_STATE.json",
    "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json",
    "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json.sha256.sidecar",
    ".agents/skills/comet/scripts/comet-hook-router.mjs",
    "workspace/review-queue/ROUTE_B_PREFLIGHT_2026-08-07.json",
    "workspace/review-queue/ROUTE_B_PREFLIGHT_2026-08-08.json",
    "workspace/review-queue/route_b_preflight.py",
    "workspace/review-queue/coverage_selfcheck.py",
    "workspace/approvals/README.md",
    "reports/remediation/S1_CONTROLLED_ENTRY_RECOVERY_TARGET_MAP_V1.json",
    "deliverables/gstack/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V2.md",
    "deliverables/gstack/MAINLINE_BLOCKER_REMEDIATION_PLAN.md",
]

# rollback backup A/B 全量（目录）
ROLLBACK_DIRS = [
    "workspace/review-queue/route_b_qualification/rollback_backup_A",
    "workspace/review-queue/route_b_qualification/rollback_backup_B",
]

# Final Audit V2 三方最新 R3/R4/QA 增补产物
AUDIT_V2_RAW = [
    "deliverables/gstack/_audit_v2_raw/security.md",
    "deliverables/gstack/_audit_v2_raw/security_findings.json",
    "deliverables/gstack/_audit_v2_raw/qa.md",
    "deliverables/gstack/_audit_v2_raw/qa_evidence.json",
    "deliverables/gstack/_audit_v2_raw/investigation.md",
    "deliverables/gstack/_audit_v2_raw/investigation_evidence.json",
]


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def mtime_utc(p: Path) -> str:
    try:
        ts = os.path.getmtime(p)
        return datetime.fromtimestamp(ts, timezone.utc).isoformat()
    except OSError:
        return None


def is_reparse(p: Path) -> bool:
    try:
        st = p.stat()
        return bool(getattr(st, "st_reparse_tag", 0) or getattr(st, "st_file_attributes", 0) & 0x400)
    except OSError:
        return None


def snapshot_file(rel: str) -> dict:
    p = ROOT / rel
    if not p.exists():
        return {"path": rel, "present": False}
    if p.is_dir():
        return {"path": rel, "present": True, "is_dir": True, "mtime_utc": mtime_utc(p)}
    return {
        "path": rel,
        "present": True,
        "is_dir": False,
        "byte_length": p.stat().st_size,
        "sha256": sha256_of(p),
        "mtime_utc": mtime_utc(p),
        "reparse": is_reparse(p),
    }


def snapshot_tree(root: Path) -> list:
    rows = []
    for p in sorted(root.rglob("*")):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        rows.append(snapshot_file(rel))
    return rows


def main() -> int:
    entries = []
    seen = set()

    def add(rel: str):
        if rel in seen:
            return
        seen.add(rel)
        entries.append(snapshot_file(rel))

    for t in CONTROLLED_TARGETS:
        add(t)
    for p in OTHER_PATHS:
        add(p)
    for d in ROLLBACK_DIRS:
        rows = snapshot_tree(ROOT / d)
        for r in rows:
            if r["path"] not in seen:
                seen.add(r["path"])
                entries.append(r)
    for p in AUDIT_V2_RAW:
        add(p)

    # pyc / pycache 扫描：受控脚本所在目录
    pyc_findings = []
    for scan_dir in ["scripts", "scripts/codex", "scripts/xianyu", "workspace/review-queue"]:
        d = ROOT / scan_dir
        if not d.exists():
            continue
        for p in sorted(d.rglob("*")):
            if p.is_file() and (p.suffix == ".pyc" or "__pycache__" in str(p)):
                rel = str(p.relative_to(ROOT)).replace("\\", "/")
                pyc_findings.append({
                    "path": rel,
                    "byte_length": p.stat().st_size,
                    "sha256": sha256_of(p),
                    "mtime_utc": mtime_utc(p),
                })

    snapshot = {
        "schema": "ROUTE_B_PROTECTED_TREE_SNAPSHOT_V1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "remediation input freeze (before any remediation write)",
        "controlled_targets": CONTROLLED_TARGETS,
        "entries": entries,
        "pyc_pycache_findings": pyc_findings,
        "summary": {
            "entries_total": len(entries),
            "present": sum(1 for e in entries if e.get("present")),
            "missing": [e["path"] for e in entries if not e.get("present")],
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")
    print(f"entries={len(entries)} present={snapshot['summary']['present']} "
          f"missing={snapshot['summary']['missing']}")
    for e in entries:
        if e.get("is_dir"):
            print(f"  [DIR ] {e['path']}")
        elif e.get("present"):
            print(f"  {e['sha256'][:12]} {e['byte_length']:>7} {e['path']}")
        else:
            print(f"  [MISS] {e['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
