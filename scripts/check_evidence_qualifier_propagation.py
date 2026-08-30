#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""证据限定语传播检查器（P1-03 / B-03 修复 · qualifier propagation）。

检查限定语（copied / reused / derived / stale / not rerun / not verified / superseded）
在 source evidence → intermediate report → summary → audit package 全链的传播。

核心验证场景（Final Audit V2 已证明）：
  08-07 preflight（source）→ 08-08 copy（intermediate）→ 后续摘要（summary）
  若 source 表达 "copy"（如 memory L12「已 cp 一份 08-08」）而 summary 表达 "08-08 rerun"
  （如 tasks[x] 中的"复跑""实测"）→ 必须 QUALIFIER_PROPAGATION_FAIL。

用法：
  python check_evidence_qualifier_propagation.py [--json <out.json>]
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"E:\project\jovi-automation")
MEMORY = ROOT / ".workbuddy/memory/2026-08-08.md"
PREFLIGHT_0707 = ROOT / "workspace/review-queue/ROUTE_B_PREFLIGHT_2026-08-07.json"
PREFLIGHT_0808 = ROOT / "workspace/review-queue/ROUTE_B_PREFLIGHT_2026-08-08.json"
STATUS = ROOT / "STATUS.md"
AUDIT_V2 = ROOT / "deliverables/gstack/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V2.md"
OUT_DEFAULT = ROOT / "reports/remediation/ROUTE_B_QUALIFIER_PROPAGATION_CHECK_V1.json"

# 限定语关键词（中文 + 英文）
QUALIFIERS = {
    "copied": ["copy", "cp 一份", "复制", "字节拷贝", "byte copy", "identical"],
    "reused": ["reuse", "复用", "沿用"],
    "derived": ["derived", "派生", "基于"],
    "stale": ["stale", "过期", "失效", "superseded", "已被取代"],
    "not_rerun": ["未重跑", "未复跑", "not rerun", "未真正执行", "当天未真正执行", "未真执行"],
    "not_verified": ["not verified", "未验证", "NOT_VERIFIED"],
}

# 反限定词：无保留地断言"真跑"（若同时出现则传播衰减）
UNQUALIFIED_PASS_CLAIMS = [
    "复跑", "实测", "rerun", "真复跑", "重新执行",
]

SUMMARY_SOURCES = [
    ("memory", MEMORY, "source evidence（源头披露）"),
    ("status", STATUS, "intermediate report（项目状态文档）"),
    ("audit_v2", AUDIT_V2, "summary（审计总报告）"),
]

CHAIN = [
    {"step": "source", "path": str(PREFLIGHT_0707), "role": "08-07 原始运行产物"},
    {"step": "intermediate", "path": str(PREFLIGHT_0808), "role": "08-08 拷贝工件（DISCLOSURE_PROPAGATION_DECAY）"},
]


def scan(text: str):
    found = {}
    for qname, kws in QUALIFIERS.items():
        hits = []
        for kw in kws:
            if kw in text:
                hits.append(kw)
        if hits:
            found[qname] = hits
    return found


def main() -> int:
    memory_txt = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    status_txt = STATUS.read_text(encoding="utf-8") if STATUS.exists() else ""
    audit_txt = AUDIT_V2.read_text(encoding="utf-8") if AUDIT_V2.exists() else ""

    # 源头（memory）是否披露 copy：memory 2026-08-08 L12 应含 "已 cp 一份 08-08"
    source_disclosed_copy = ("cp" in memory_txt and "08-08" in memory_txt) or ("复制" in memory_txt)
    # 下游是否出现无保留"复跑/实测"
    unqualified_in_status = [w for w in UNQUALIFIED_PASS_CLAIMS if w in status_txt]
    unqualified_in_audit = [w for w in UNQUALIFIED_PASS_CLAIMS if w in audit_txt]

    # 具体断言：08-08 preflight 的"复跑"表述是否带限定
    # memory L12 原文带括号限定 → source 诚实；STATUS L21 中 "pre-flight 复跑 ... 仍 PASS" 无限定
    status_has_unqualified_0808_rerun = False
    if "复跑" in status_txt:
        # 找 "复跑" 上下文是否带限定词（括号/UTC/cp/copy）
        for m in re.finditer(r".{80}复跑.{80}", status_txt):
            ctx = m.group(0)
            qualified = any(kw in ctx for kw in ["cp", "copy", "UTC", "实际写", "复制", "字节拷贝"])
            if not qualified:
                status_has_unqualified_0808_rerun = True

    # 审计总报告是否明确"披露传播衰减"
    audit_has_decay_label = ("披露传播衰减" in audit_txt) or ("DISCLOSURE_PROPAGATION_DECAY" in audit_txt)

    findings = []
    if source_disclosed_copy and status_has_unqualified_0808_rerun:
        findings.append({
            "severity": "HIGH",
            "code": "QUALIFIER_PROPAGATION_FAIL",
            "message": "source 披露了 copy（memory L12），但 STATUS.md 摘要层以无限定'复跑'表述 08-08 preflight → 限定语在传播中丢失",
            "evidence": {
                "source_disclosed_copy": source_disclosed_copy,
                "status_unqualified_rerun": status_has_unqualified_0808_rerun,
                "unqualified_terms_in_status": unqualified_in_status,
            },
        })
    else:
        findings.append({
            "severity": "INFO",
            "code": "NO_ACTIVE_PROPAGATION_FAIL_IN_CURRENT_DOCS",
            "message": "当前文档未发现 active 的无限定'复跑'断言（STATUS 已由 remediation 前序记录勘误）",
            "evidence": {
                "source_disclosed_copy": source_disclosed_copy,
                "status_has_unqualified_rerun": status_has_unqualified_0808_rerun,
                "audit_has_decay_label": audit_has_decay_label,
            },
        })

    report = {
        "schema": "ROUTE_B_QUALIFIER_PROPAGATION_CHECK_V1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "author": "remediation-executor",
        "chain": CHAIN,
        "scan_sources": [
            {"name": n, "path": str(p), "role": r} for n, p, r in SUMMARY_SOURCES
        ],
        "source_qualifiers": scan(memory_txt),
        "status_qualifiers": scan(status_txt),
        "audit_qualifiers": scan(audit_txt),
        "findings": findings,
        "rule": "若 source 表达 copy 而 summary 表达 rerun → QUALIFIER_PROPAGATION_FAIL",
        "qualifier_preservation_rule": "上游带括号限定的事实陈述，下游引用时必须连同限定语一并携带，或标注'限定语已省略，见原始出处'",
    }

    out_path = Path(OUT_DEFAULT)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"source_disclosed_copy={source_disclosed_copy}")
    print(f"status_unqualified_0808_rerun={status_has_unqualified_0808_rerun}")
    print(f"unqualified_in_status={unqualified_in_status}")
    print(f"audit_has_decay_label={audit_has_decay_label}")
    for f in findings:
        print(f"  [{f['severity']}] {f['code']}: {f['message'][:80]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
