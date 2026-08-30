#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真实树保护对比（步骤十三）：before vs after 快照差异检测。

分类：
- 允许新增：新 scripts / 新 tests / reports/remediation 新报告 / workspace/review-queue 新 candidate /
  Audit Input Package V3（这些出现在 after 而不在 before 且属于允许写入范围 → OK）
- 严禁修改：10 受控目标 / hooks.json / pre_tool_guard.py / Invoke-PreToolGuard.ps1 /
  FRAMEWORK_MANIFEST / MANIFEST / 旧 Decision / rollback backup / approvals / human-only / Xianyu
  任何受保护对象 SHA 变化 → ROUTE_B_REMEDIATION_SCOPE_VIOLATION
"""
import json
from pathlib import Path

ROOT = Path(r"E:\project\jovi-automation")
BEFORE = ROOT / "reports/remediation/ROUTE_B_PROTECTED_TREE_SNAPSHOT_BEFORE_V1.json"
AFTER = ROOT / "reports/remediation/ROUTE_B_PROTECTED_TREE_SNAPSHOT_AFTER_V1.json"
OUT = ROOT / "reports/remediation/ROUTE_B_PROTECTED_TREE_DIFF_V1.json"

# 严禁修改的受保护路径（含目录前缀）
FORBIDDEN_PREFIXES = [
    ".codex/hooks.json",
    "scripts/codex/pre_tool_guard.py",
    "scripts/codex/Invoke-PreToolGuard.ps1",
    "FRAMEWORK_MANIFEST.sha256",
    "MANIFEST.sha256",
    "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json",
    "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json.sha256.sidecar",
    "workspace/review-queue/route_b_qualification/rollback_backup_A/",
    "workspace/review-queue/route_b_qualification/rollback_backup_B/",
    "workspace/approvals/",
    "scripts/human-only/",
    "scripts/xianyu/human-only/",
]
# 10 受控目标（单独列出，精确匹配）
CONTROLLED = [
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

# 允许新增的目录前缀
ALLOWED_NEW_PREFIXES = [
    "scripts/route_b_preflight_v2.py",
    "scripts/validate_hook_guard_chain.py",
    "scripts/validate_independent_audit_binding.py",
    "scripts/check_evidence_qualifier_propagation.py",
    "scripts/snapshot_protected_tree.py",
    "tests/test_route_b_preflight_v2.py",
    "tests/test_validate_independent_audit_binding.py",
    "reports/remediation/",
    "workspace/review-queue/ROUTE_B_REMEDIATION_TASK_MATRIX_V1.json",
    "workspace/review-queue/JOVI_S1_RESTART_DECISION_V2_CANDIDATE.json",
    "workspace/review-queue/JOVI_S1_RESTART_DECISION_V2_CANDIDATE.json.sha256.sidecar",
    "workspace/review-queue/STATUS_CURRENT_STATE_PATCH_V1.md",
    "workspace/review-queue/PROJECT_STATE_CURRENT_STATE_PATCH_V1.json",
    "workspace/review-queue/ROUTE_B_FINAL_AUDIT_INPUT_PACKAGE_V3/",
    "workspace/review-queue/coverage_selfcheck_report_v2.json",
    "workspace/review-queue/_gen_decision_v2_candidate.py",
    "workspace/review-queue/_build_audit_input_v3.py",
]


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def entry_map(snap):
    m = {}
    for e in snap["entries"]:
        m[e["path"]] = e
    return m


def main() -> int:
    before = load(BEFORE)
    after = load(AFTER)
    bm = entry_map(before)
    am = entry_map(after)

    changed = []
    added = []
    removed = []
    for path in sorted(set(bm) | set(am)):
        if path in bm and path in am:
            b, a = bm[path], am[path]
            if b.get("sha256") != a.get("sha256") or b.get("byte_length") != a.get("byte_length"):
                changed.append({
                    "path": path,
                    "before_sha": b.get("sha256"),
                    "after_sha": a.get("sha256"),
                    "before_bytes": b.get("byte_length"),
                    "after_bytes": a.get("byte_length"),
                })
        elif path in am:
            added.append(path)
        else:
            removed.append(path)

    # 分类
    violations = []
    for c in changed:
        path = c["path"]
        if path in CONTROLLED or any(path.startswith(f) for f in FORBIDDEN_PREFIXES):
            violations.append({"type": "FORBIDDEN_MODIFIED", **c})
        else:
            violations.append({"type": "NON_PROTECTED_MODIFIED", **c})

    for p in added:
        if not any(p.startswith(f) for f in ALLOWED_NEW_PREFIXES):
            violations.append({"type": "UNEXPECTED_ADDED", "path": p})
        else:
            pass  # 允许新增

    scope_verdict = "ROUTE_B_REMEDIATION_SCOPE_VIOLATION" if any(
        v["type"] in ("FORBIDDEN_MODIFIED", "UNEXPECTED_ADDED") for v in violations
    ) else "ROUTE_B_REMEDIATION_SCOPE_CLEAN"

    report = {
        "schema": "ROUTE_B_PROTECTED_TREE_DIFF_V1",
        "generated_at_utc": after.get("captured_at_utc"),
        "before_snapshot": str(BEFORE),
        "after_snapshot": str(AFTER),
        "changed_count": len(changed),
        "added_count": len(added),
        "removed_count": len(removed),
        "forbidden_modified": [v for v in violations if v["type"] == "FORBIDDEN_MODIFIED"],
        "unexpected_added": [v for v in violations if v["type"] == "UNEXPECTED_ADDED"],
        "non_protected_modified": [v for v in violations if v["type"] == "NON_PROTECTED_MODIFIED"],
        "allowed_added": [p for p in added if any(p.startswith(f) for f in ALLOWED_NEW_PREFIXES)],
        "scope_verdict": scope_verdict,
        "note": "受保护对象（10 受控目标 / Hook 三组件 / 双 Manifest / 旧 Decision / rollback / approvals / human-only）不得有任何修改。",
    }

    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"changed={len(changed)} added={len(added)} removed={len(removed)}")
    print(f"scope_verdict = {scope_verdict}")
    for v in violations:
        print(f"  [{v['type']}] {v.get('path', v.get('type'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
