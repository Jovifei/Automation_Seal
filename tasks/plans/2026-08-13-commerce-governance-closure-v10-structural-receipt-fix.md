# JOVI-AUTOMATION-COMMERCE-GOVERNANCE-CLOSURE-V10 Structural Receipt Fix

> **For agentic workers:** REQUIRED SUB-SKILL: use `executing-plans`; implement candidate changes with TDD; use fresh Luna `gpt-5.6-terra` with `xhigh` reasoning for independent audits only. Never use sol. Do not run human-only scripts.

**Goal:** Supersede the issued-but-automatically-rolled-back V9 Structural transaction with a V10 candidate whose real receipt schema is valid, whose isolated-root APPLY succeeds, and whose formal application remains limited to the same 13 structural bytes plus `FRAMEWORK_MANIFEST.sha256`.

**Architecture:** Keep formal V9 and its failed recovery journal immutable as historical evidence. Build V10 only in `workspace/review-queue/commerce-v1/governance-closure-v10/`, bind formal V9, its issuance source/audit, and the `ROLLED_BACK_AFTER_FAILURE` journal/backups. Correct the receipt builder so every published target row has `path`, `before_bytes`, `before_sha256`, `after_bytes`, and `after_sha256`; validate that exact shape through a real isolated-root APPLY, not a mocked receipt.

**Tech Stack:** Python 3.12 standard library, JSON/UTF-8 bytes, SHA-256 body sidecars, Windows PowerShell 5.1 parser, `unittest`.

## Global Constraints

- Formal V7 remains `a7bafcdf4c3f26848338f8abd1c5773edbe18c4b8b447613b6acfb4d8a194204`.
- Formal V9 remains immutable historical evidence: `af24e7ce181d5f5520be4570351e3cfe243b07562625d80928a79c684122c1bb`.
- The V9 journal at `workspace/review-queue/commerce-v1/governance-closure-v9-execution-receipts/structural/v9-apply-20260813-a/RECOVERY_JOURNAL_V9.json` must stay `ROLLED_BACK_AFTER_FAILURE`; its 14 backups and sidecar are never deleted, overwritten, recovered or rerun.
- All 14 V9 transaction targets must remain at their frozen V9 before bytes before V10 issuance and before V10 APPLY.
- V10 may write only candidate files until a fresh independent V10 pre-apply PASS and a new Jovi-issued Decision V10 exist.
- No formal tree edit, Hook/Manifest trust change, approval write, human-only execution, Gate, Commerce import, Git initialization, external Xianyu access, payment, delivery or platform action is in scope.
- Receipt and audit outputs are excluded from candidate-package self-coverage; all other candidate bodies and sidecars must be manifest-covered exactly once.

## Task 0 — Freeze V9 failure evidence

- [ ] Read formal V9 body/sidecar, V9 candidate source, V9 R2 audit, failed journal/sidecar, 14 backup files and absence of `STRUCTURAL_APPLY_RECEIPT_V9.json`.
- [ ] Recompute all 14 live target SHA/bytes and require the V9 before values; reject any after/mixed/unknown bytes.
- [ ] Create a V10 candidate-only copied input set containing the V9 formal Decision, V9 source candidate, V9 R2 audit, journal, journal sidecar and a machine-readable V9 failure evidence summary.
- [ ] The summary must bind journal SHA, journal sidecar-file SHA, 14 backup SHA/bytes, `ROLLED_BACK_AFTER_FAILURE`, the failed tool SHA and formal V9 SHA.

## Task 1 — TDD receipt-schema correction

**Candidate files:**

- Create `workspace/review-queue/commerce-v1/governance-closure-v10/tools/v10_runtime.py`.
- Create `workspace/review-queue/commerce-v1/governance-closure-v10/tools/apply_phase2b_structural_v10.py`.
- Create `workspace/review-queue/commerce-v1/governance-closure-v10/tests/test_v10_structural_receipt.py`.

- [ ] Write a failing test that invokes the actual V10 `--apply` in an isolated staged root with exactly 13 structural targets plus Framework and asserts a published receipt has 14 rows with all five required fields.
- [ ] Run the test before implementation. Expected failure against the copied V9 behavior: `invalid target byte count: CODEX_START_PROMPT.txt` or missing `before_bytes`.
- [ ] Implement a dedicated `receipt_target_rows(rows)` that returns full target rows:

```python
def receipt_target_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "path": row["path"],
            "before_bytes": row["before_bytes"],
            "before_sha256": row["before_sha256"],
            "after_bytes": row["after_bytes"],
            "after_sha256": row["after_sha256"],
        }
        for row in rows
    ]
```

- [ ] Make `validate_structural_receipt()` validate exactly that full shape and reject legacy `{path, bytes, sha256}` receipt rows.
- [ ] Run the isolated root test again. Expected result: V10 APPLY success, valid receipt+sidecar, journal status `APPLIED`, Framework 40/40 after match and protected snapshot equality.
- [ ] Add a negative test that tampers one receipt `before_bytes` value and proves validation fails.

## Task 2 — Recovery and failure-evidence boundaries

- [ ] Add tests proving V10 `--rollback` operates only on a V10 journal whose targets are all after bytes.
- [ ] Add tests proving V10 `--recover` only accepts a V10 journal with a before/after mixture and cannot accept V9’s historical journal path.
- [ ] Bind V9 failed journal and backup manifest into V10 Decision as historical inputs only; V10 runtime must reject their use as V10 receipt or recovery inputs.
- [ ] Run the targeted recovery tests and the complete candidate suite.

## Task 3 — Freeze V10 package and pre-apply interface

- [ ] Recreate the same exact 13 structural plus 1 Framework target set from live before bytes, independently recompute Framework 40 entries and exact diff.
- [ ] Generate V10 Decision candidate, review package, implementation report, PowerShell `Issue-DecisionV10.ps1`, candidate tests and all sidecars.
- [ ] Decision V10 must supersede `JOVI_S1_RESTART_DECISION_V9`, bind formal V9 plus its issuance bindings, V9 failure evidence, V10 target/diff/framework/package/review/tools, and retain Hook `DO_NOT_TRUST` with all authority booleans false and manifest scope only `FRAMEWORK_MANIFEST.sha256`.
- [ ] `Issue-DecisionV10.ps1` must require separate candidate/review/independent-audit SHA parameters, validate an independent V10 report with `PASS_READY_FOR_JOVI_DECISION_V10`, then atomically create only formal V10 body+sidecar after Jovi types `ISSUE DECISION V10 <candidate-prefix>`.
- [ ] Exclude V10 independent-audit output and V10 execution receipts from the V10 package manifest. Generate manifest last and independently rehash every covered entry and sidecar after generation.

## Task 4 — Candidate validation and independent V10 pre-apply audit

- [ ] Run all V10 tests using the bundled Python 3.12 runtime; record actual pass count.
- [ ] Run Python compilation and Windows PowerShell 5.1 parser checks for `Issue-DecisionV10.ps1`.
- [ ] Verify package exact membership, body/sidecar relationships, target count 14, Framework 40/40, current formal target before values, V9 journal preservation and formal V10 absence.
- [ ] Use a fresh Luna auditor that did not implement V10. It may write only `preapply-evidence/V10_INDEPENDENT_PREAPPLY_AUDIT.json` and its sidecar. It must inspect the real isolated APPLY regression result and issue only `PASS_READY_FOR_JOVI_DECISION_V10` or a fail-closed verdict.

## Task 5 — Jovi issuance and bounded V10 APPLY

- [ ] Only after Task 4 PASS, provide Jovi a mechanically derived complete V10 issuance command. Do not omit or hand-copy any mandatory SHA parameter.
- [ ] Re-read formal V10 body/sidecar, all issuance bindings and false authorities after Jovi’s command.
- [ ] Run V10 Structural `--check`, requiring `target_count=14`, `writes=0` and no receipt directory creation.
- [ ] Run V10 `--apply` once with a new V10 receipt directory. It must publish receipt+sidecar and journal+sidecar, preserve V9 failure evidence, validate 14 after rows and Framework 40/40, and leave MANIFEST, Hook, V7/V9/V10 Decisions, approvals and human-only trees unchanged.
- [ ] Any failure after a formal write requires V10’s bound rollback/recover outcome to be independently checked, followed by a new candidate revision and fresh Decision; never retry a signed candidate in place.

## Completion / Handoff

V10 is not complete when the candidate is green. It reaches the next V9-plan milestone only after formal V10 issuance and a successful V10 structural receipt. Then a new independent Post-Apply audit precedes closeout, Gate A.P and C/APPLY. Commerce import, main-root X2, real commerce pilot and remote setup remain `NOT_STARTED`.
