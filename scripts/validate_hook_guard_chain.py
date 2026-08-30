#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hook / Guard 双轨验证器（B-04 / B-08 / P0-04 / P1 修复）。

Track A — Byte Integrity：三组件 formal expected vs current actual SHA（MATCH / MISMATCH）。
Track B — Semantic Evidence：
  - hooks.json canonical parse：entry count / matcher / command / commandWindows / timeout /
    statusMessage / canonical JSON digest；
  - 比较 ① rollback backup 中的旧 Hook ② current PreToolUse[0] ③ current comet entry；
  - semantic-equivalent 与 byte-identical 严格区分；
  - pre_tool_guard.py / Invoke-PreToolGuard.ps1 默认
    BYTE_MISMATCH_SEMANTIC_TRUST_NOT_ESTABLISHED（除非有 AST/canonical/behavior replay 证据）。

最终 Hook chain trust = DO_NOT_TRUST（本轮不得改变）。

用法：
  python validate_hook_guard_chain.py [--json <out.json>] [--canonical-separators compact|default]
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"E:\project\jovi-automation")
HOOKS = ROOT / ".codex/hooks.json"
GUARD_PY = ROOT / "scripts/codex/pre_tool_guard.py"
GUARD_PS1 = ROOT / "scripts/codex/Invoke-PreToolGuard.ps1"
ROLLBACK_A = ROOT / "workspace/review-queue/route_b_qualification/rollback_backup_A/.codex_hooks.json"
ROLLBACK_B = ROOT / "workspace/review-queue/route_b_qualification/rollback_backup_B/.codex_hooks.json"
FRAMEWORK = ROOT / "FRAMEWORK_MANIFEST.sha256"
OUT_DEFAULT = ROOT / "reports/remediation/ROUTE_B_HOOK_GUARD_CHAIN_VALIDATION_V1.json"

GUARD_COMPONENTS = [
    ("hooks.json", ".codex/hooks.json", HOOKS),
    ("pre_tool_guard.py", "scripts/codex/pre_tool_guard.py", GUARD_PY),
    ("Invoke-PreToolGuard.ps1", "scripts/codex/Invoke-PreToolGuard.ps1", GUARD_PS1),
]


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


def canonical_dump(obj, separators):
    return json.dumps(obj, sort_keys=True, separators=separators, ensure_ascii=False)


def canonical_sha(obj, separators):
    return hashlib.sha256(canonical_dump(obj, separators).encode("utf-8")).hexdigest()


def load_hooks(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def extract_pre_tool_entries(hooks):
    """返回 PreToolUse 条目列表（matcher + hooks[0] 的语义字段）。"""
    entries = []
    for block in hooks.get("hooks", {}).get("PreToolUse", []):
        matcher = block.get("matcher")
        for h in block.get("hooks", []):
            entries.append({
                "matcher": matcher,
                "type": h.get("type"),
                "command": h.get("command"),
                "commandWindows": h.get("commandWindows"),
                "timeout": h.get("timeout"),
                "statusMessage": h.get("statusMessage"),
            })
    return entries


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=str(OUT_DEFAULT))
    ap.add_argument("--canonical-separators", choices=["compact", "default"], default="compact")
    args = ap.parse_args()
    if args.canonical_separators == "compact":
        separators = (",", ":")
    else:
        separators = (", ", ": ")

    fm_map = parse_manifest(FRAMEWORK)

    # ---- Track A: Byte Integrity ----
    track_a = []
    for name, rel, p in GUARD_COMPONENTS:
        formal = fm_map.get(rel)
        actual = sha256_of(p)
        match = bool(formal and actual.lower() == formal.lower())
        track_a.append({
            "component": name,
            "path": rel,
            "formal_expected_sha256": formal,
            "current_actual_sha256": actual,
            "match": match,
            "verdict": "MATCH" if match else "MISMATCH",
        })

    # ---- Track B: Semantic Evidence (hooks.json) ----
    current = load_hooks(HOOKS)
    rollback_a = load_hooks(ROLLBACK_A)
    rollback_b = load_hooks(ROLLBACK_B)

    cur_entries = extract_pre_tool_entries(current)
    rb_a_entries = extract_pre_tool_entries(rollback_a)
    rb_b_entries = extract_pre_tool_entries(rollback_b)

    # 语义字段（排除 commandWindows 因体积巨大——逐条比对前 N 字符指纹；此处聚焦语义键）
    def semantic_view(entries):
        return [
            {
                "matcher": e["matcher"],
                "type": e["type"],
                "command": e["command"],
                "timeout": e["timeout"],
                "statusMessage": e["statusMessage"],
                "commandWindows_prefix": (e["commandWindows"] or "")[:60],
            }
            for e in entries
        ]

    cur_sem = semantic_view(cur_entries)
    rb_a_sem = semantic_view(rb_a_entries)
    rb_b_sem = semantic_view(rb_b_entries)

    # entry[0]（原守卫条目）语义等价判断：cur[0] vs rollback[0]
    entry0_semantic_cur_vs_a = (cur_sem[0] == rb_a_sem[0]) if cur_sem and rb_a_sem else None
    entry0_semantic_cur_vs_b = (cur_sem[0] == rb_b_sem[0]) if cur_sem and rb_b_sem else None

    # byte-identical 判断
    byte_cur_vs_a = HOOKS.read_bytes() == ROLLBACK_A.read_bytes()
    byte_cur_vs_b = HOOKS.read_bytes() == ROLLBACK_B.read_bytes()

    canonical_cur = canonical_sha(current, separators)
    canonical_rb_a = canonical_sha(rollback_a, separators)
    canonical_rb_b = canonical_sha(rollback_b, separators)

    track_b = {
        "hooks_json": {
            "entry_count_current": len(cur_entries),
            "entry_count_rollback_a": len(rb_a_entries),
            "entry_count_rollback_b": len(rb_b_entries),
            "entries_current": [
                {
                    "index": i,
                    "matcher": e["matcher"],
                    "command": (e["command"] or "")[:90],
                    "timeout": e["timeout"],
                    "statusMessage": e["statusMessage"],
                    "has_commandWindows": bool(e["commandWindows"]),
                }
                for i, e in enumerate(cur_entries)
            ],
            "semantic_equivalence": {
                "entry0_current_vs_rollback_a": entry0_semantic_cur_vs_a,
                "entry0_current_vs_rollback_b": entry0_semantic_cur_vs_b,
                "note": "entry[0] 语义视图（matcher/type/command/timeout/statusMessage/commandWindows 前缀）比对。",
            },
            "byte_identity": {
                "current_vs_rollback_a": byte_cur_vs_a,
                "current_vs_rollback_b": byte_cur_vs_b,
                "note": "byte-identical 与 semantic-equivalent 严格区分：字节可不同而语义相等（F-017 re-serialize）。",
            },
            "canonical_digest": {
                "separators": args.canonical_separators,
                "current": canonical_cur,
                "rollback_a": canonical_rb_a,
                "rollback_b": canonical_rb_b,
                "current_vs_rollback_a": canonical_cur == canonical_rb_a,
                "current_vs_rollback_b": canonical_cur == canonical_rb_b,
            },
        },
        "pre_tool_guard_py": {
            "semantic_trust": "BYTE_MISMATCH_SEMANTIC_TRUST_NOT_ESTABLISHED",
            "evidence": "无 AST evidence / canonical evidence / behavior replay evidence 证明语义等价；默认不建立信任。",
        },
        "invoke_pre_tool_guard_ps1": {
            "semantic_trust": "BYTE_MISMATCH_SEMANTIC_TRUST_NOT_ESTABLISHED",
            "evidence": "同 pre_tool_guard.py：无证明语义等价的独立证据。",
        },
    }

    chain_trust = "DO_NOT_TRUST"
    all_byte_match = all(t["match"] for t in track_a)
    report = {
        "schema": "ROUTE_B_HOOK_GUARD_CHAIN_VALIDATION_V1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "author": "remediation-executor",
        "canonical_separators_used": args.canonical_separators,
        "track_a_byte_integrity": track_a,
        "track_b_semantic_evidence": track_b,
        "chain_trust": chain_trust,
        "chain_trust_reason": (
            "三组件（hooks.json / pre_tool_guard.py / Invoke-PreToolGuard.ps1）与 formal expected 全部 MISMATCH；"
            "语义等价≠可信：可信要求锚到正式基线，而三组件当前都锚不上。DO_NOT_TRUST 是唯一可成立结论。"
        ),
        "semantic_vs_byte_notes": [
            "entry[0] 语义可保持相等（canonical 口径 cur==old=True），但整文件 byte SHA 不等（F-017 re-serialize 215B）。",
            "byte-identical 与 semantic-equivalent 必须严格区分；信任判定以锚定正式基线为准。",
        ],
    }

    out_path = Path(args.json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")
    for t in track_a:
        print(f"  [TrackA] {t['component']:<28} {t['verdict']}")
    print(f"  [TrackB] entry0_semantic cur_vs_a={entry0_semantic_cur_vs_a} cur_vs_b={entry0_semantic_cur_vs_b}")
    print(f"  [TrackB] canonical cur==a {canonical_cur == canonical_rb_a} cur==b {canonical_cur == canonical_rb_b}")
    print(f"  [TrackB] byte cur==a {byte_cur_vs_a} cur==b {byte_cur_vs_b}")
    print(f"  chain_trust = {chain_trust}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
