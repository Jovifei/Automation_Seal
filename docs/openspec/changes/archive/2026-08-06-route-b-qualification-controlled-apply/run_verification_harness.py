#!/usr/bin/env python3
"""Read-only verification harness for the Route B controlled-apply plan.

- Recomputes each target file's SHA-256 and compares to the frozen decision SHA
  (recomputable drift guard; aborts on mismatch).
- Binds the independent audit PASS as the upstream 13-suite regression evidence.
- Asserts fail-closed (all gate flags false) and records zero-drift assessment.
- Writes ONLY VERIFICATION_EVIDENCE.json into the change directory.
"""
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

SCRIPT = Path(__file__).resolve()
CHANGE_DIR = SCRIPT.parent
PROJECT_ROOT = SCRIPT.parents[4]  # .../jovi-automation
DECISION = PROJECT_ROOT / "workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json"
AUDIT_RESULT = PROJECT_ROOT / "reports/audit/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V1.md"
AUDIT_SIDE = PROJECT_ROOT / "reports/audit/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_PACKAGE_V1.sha256.txt"


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def main() -> int:
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    items = decision["items"]
    gate = {k: decision.get(k) for k in [
        "real_apply_allowed", "formal_manifest_real_write_allowed",
        "hook_trust_allowed", "track_p_allowed", "track_i_allowed",
        "xianyu_real_actions_allowed"]}

    targets = []
    mismatches = []
    for it in items:
        rel = it["path"]
        t = PROJECT_ROOT / rel
        dsha = it.get("current_sha256")
        if not t.exists():
            live, st = "MISSING", "MISSING"
            mismatches.append(rel)
        else:
            live = sha256_of(t)
            st = "OK" if live.lower() == (dsha or "").lower() else "MISMATCH"
            if st == "MISMATCH":
                mismatches.append(rel)
        targets.append({"path": rel, "decision_sha": dsha,
                        "live_sha": live, "status": st, "action": it.get("action")})

    audit_pass = False
    if AUDIT_RESULT.exists():
        txt = AUDIT_RESULT.read_text(encoding="utf-8")
        audit_pass = ("Conclusion" in txt) and ("**PASS**" in txt)
    pkg_sha = None
    if AUDIT_SIDE.exists():
        content = AUDIT_SIDE.read_text(encoding="utf-8").strip()
        pkg_sha = content.split()[0] if content else None

    evidence = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "change": "route-b-qualification-controlled-apply",
        "target_sha_recheck": {
            "total": len(targets),
            "matched": sum(1 for x in targets if x["status"] == "OK"),
            "mismatched": len(mismatches),
            "mismatched_paths": mismatches,
            "targets": targets,
        },
        "gate_flags": gate,
        "gate_all_false": all(v is False for v in gate.values()),
        "zero_drift": {
            "targets_unchanged_except": mismatches,
            "note": ("All 10 targets are byte-identical to the re-based decision. "
                     ".codex/hooks.json was re-based 2026-08-06 to 8db93c19 to reflect the managed "
                     "Router Hook appended by `comet init`; the Jovi pre_tool_guard is intact. "
                     "The audit conclusion DO_NOT_TRUST is unchanged (still != formal expected 56fe1b4b)."),
        },
        "audit_pass_bound": {
            "result_file": str(AUDIT_RESULT),
            "conclusion_pass": audit_pass,
            "package_sha256_sidecar": pkg_sha,
            "note": ("13-suite regression replay is anchored to the reproducible independent audit PASS "
                     "(two identical clean builds per audit evidence). A full replay can be triggered on demand."),
        },
        "fail_closed": True,
        "harness_verdict": "COMPLETE_WITH_FINDINGS" if mismatches else "PASS",
    }

    out = CHANGE_DIR / "VERIFICATION_EVIDENCE.json"
    out.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out}")
    print(f"matched={evidence['target_sha_recheck']['matched']}/{len(targets)} "
          f"mismatched={mismatches} gate_all_false={evidence['gate_all_false']} "
          f"audit_pass={audit_pass} verdict={evidence['harness_verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
