# JOVI-AUTOMATION-COMMERCE-GOVERNANCE-CLOSURE-V9 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans`; candidate implementation tasks use TDD and every completion claim uses verification-before-completion. Fresh independent audits use Luna `gpt-5.6-terra` with `xhigh` reasoning. Do not use sol.

**Goal:** Close the governance chain from issued V7 to a V9-bound Structural APPLY, Post-Apply Audit, S1 closeout, Gate A.P and C/APPLY while keeping Commerce import, Git baseline, real platform actions and the pilot unauthorized.

**Architecture:** Build a candidate-only V9 package under `workspace/review-queue/commerce-v1/governance-closure-v9/`. V9 supersedes formal V7 and consumes the audited-but-unissued V8 candidate/PASS as history. After a fresh independent V9 pre-apply PASS, Jovi alone issues Decision V9; Luna performs the bound structural write, a different Luna performs the only Post-Apply Audit, and the remaining Gate/C-APPLY human gates occur in order.

**Tech Stack:** Python 3.12 standard library, JSON/UTF-8 bytes, SHA-256 sidecars, PowerShell 5.1-compatible scripts, `unittest`, existing governed control-plane tools.

## Global Constraints

- Formal V7 remains unchanged: `a7bafcdf4c3f26848338f8abd1c5773edbe18c4b8b447613b6acfb4d8a194204`.
- V8 inputs are candidate/history only: candidate `5121a89a95bbdf4fedd3f95716fa24f3cb5b92363b4b383337385e553f64bf63`; audit `c60738ed1aa8534607d85e5e8211d822b3109a81c1b475399bc9c84df3e673ca`.
- Hook remains `DO_NOT_TRUST`; runtime/restore/trust and Track P/I/platform booleans remain explicit `false`.
- No V8/V9 human-only action, Gate approval, Manifest APPLY, Commerce import, Git initialization, product write, real payment, delivery, refund, platform action or external Xianyu access is performed by Luna.
- Existing canonical mirror is immutable: verify its 52/52 tree by elevated read-only inspection; never change ACL, replace, delete or re-materialize it.
- Candidate package excludes its own manifest/sidecar, the current independent review output/sidecar, execution receipts and `__pycache__` from self-coverage.
- Any SHA, byte, path, sidecar, state or phase drift fails closed and invalidates the candidate.

## Task 0 — Preflight and frozen inputs

- Save this plan and its sidecar before creating the candidate.
- Verify V7 body/sidecar, absence of formal V8/V9, V8 package 122/122, V8 audit body/sidecar, current 13 V8 target before bytes, Hook/Manifest/Decision/Approval/human-only/control-plane snapshots, old mirror 52/52, and external repository commits/clean/remote-empty.
- Confirm the root `.git` state is not treated as a valid HEAD unless `git rev-parse --verify HEAD` succeeds; no initialization or repair is allowed before C/APPLY.
- Stop as `BLOCKED_V9_PREFLIGHT_DRIFT` on any mismatch.

## Task 1 — TDD V9 downstream-chain candidate

Create candidate files under `governance-closure-v9/tools/`, `tests/`, `proposed-structural/` and `proposed-closeout/`. Write RED tests first, then the smallest GREEN implementation. Tests must fail closed for missing independent V9 audit, V8-PASS masquerading as V9, missing receipt bindings, hard-coded exact-diff counts, V3 decision/path references, missing Post-Apply sidecars, post-transition rejection of an existing approval, unbound closeout/transition/import tools, non-Jovi approval, unsafe targets and Windows path collisions.

Implement real non-stub tools:

- `validate_post_apply_audit_v9.py`
- `apply_s1_closeout_v9.py`
- `verify_phase2b_governance_chain_v9.py`
- `prepare_import_scope_v9.py`
- `generate_gate_a_plan_bound_v9.py`
- `verify_gate_a_p_bound_v9.py`
- `apply_control_plane_transition_v9.py`

Every tool self-binds its SHA, requires body/sidecar inputs, validates formal Decision V9, phase, target before bytes and forbidden paths before any write. `pre-gate` requires no approval; `post-transition` verifies the existing approval/plan/transition receipt.

Structural executor interface is exactly:

```text
--root --decision --independent-preapply-audit --target-set --exact-diff
--framework-candidate --package-manifest --receipt-dir
--check | --apply | --rollback | --recover
```

Its receipt binds Decision/source proposal, V9 audit, V8 history, tool self-SHA, package/target/diff/framework SHA, all 14 before/after rows, protected snapshots, backup, run ID and UTC. A recovery journal is written before the first formal byte.

## Task 2 — Freeze the V9 candidate package

- Use 13 structural targets (the V8 12 plus `scripts/generate_gate_a_plan.py`) and one `FRAMEWORK_MANIFEST.sha256` target: 14 transactions exactly.
- Recompute Framework 40/40 and exact diff from current bytes; never hard-code counts.
- Freeze closeout target bytes for exactly `config/control-plane-state.json`, `PROJECT_STATE.json`, `STATUS.md`; Prompt remains unchanged; closeout after-state is S1/CLOSED with blockers empty and Hook DNT accepted.
- Generate `DECISION_V9_PROPOSED.json`, `Issue-DecisionV9.ps1`, review package, implementation report, target/diff/receipt schemas and all sidecars. Decision includes both `ExpectedReviewPackageSha256` and `ExpectedIndependentAuditSha256`; issuance writes the independent audit SHA into `issuance_bindings`.
- Generate the package manifest last; verify every declared member and sidecar after generation and freeze the directory.

## Task 3 — Fresh independent V9 pre-apply audit

Dispatch a new Luna `gpt-5.6-terra/xhigh` agent not involved in implementation. It writes only `V9_INDEPENDENT_PREAPPLY_AUDIT.json` and its sidecar. It verifies package, Decision bindings, 14 before targets, Framework 40/40, V7 unchanged, V8/V9 formal absence, old mirror 52/52, real tools, negative tests and zero formal/human/external actions. Only `PASS_READY_FOR_JOVI_DECISION_V9` is acceptable. Any FAIL requires a new freeze and a new independent agent.

## Task 4 — Jovi-only Decision V9

Do not run the script. Provide Jovi the exact command only after Task 3 PASS. `Issue-DecisionV9.ps1` verifies candidate, V7, V8, D2, review package, independent audit, package manifest, all self-bindings and false policies before prompting `ISSUE DECISION V9 <candidate-sha-prefix>`. After Jovi runs it, read-only verify formal V9/sidecar, independent audit binding, lineage, Hook policy, scope and all tool bindings.

## Task 5 — V9 Structural + Framework APPLY

After formal V9 exists, run `--check` (14 targets, zero writes), then `--apply`. Verify all 13 structural after bytes, Framework 40/40, receipt/journal/backup/sidecars and unchanged MANIFEST, Hook, V7/V9 Decision, Approval, human-only tree, S1/CLOSED state and canonical mirror. Use only bound rollback/recover on failure. Success is `PHASE2B_STRUCTURAL_REMEDIATION_APPLIED_V9` plus `FRAMEWORK_MANIFEST_V9_APPLIED`.

## Task 6 — One independent Post-Apply Audit

Dispatch a different fresh Luna `gpt-5.6-terra/xhigh`. It writes only `reports/remediation/COMMERCE_V1_POST_APPLY_AUDIT.json` and its sidecar. It asserts `verdict=PASS`, `independent=true`, V9/V9-audit/receipt bindings, 14 after targets, Framework 40/40, MANIFEST unchanged, Hook DNT, human-only zero drift, S1/CLOSED, no Gate/Approval/runtime and all real actions false. Formal-byte findings require bound rollback and a new candidate; never reuse a stale PASS.

## Task 7 — V9-bound S1 closeout

Run the V9 closeout `--check`; then `--apply` only if all V9, audit, receipt, target, patch and self-SHA checks pass. It may write exactly `config/control-plane-state.json`, `PROJECT_STATE.json` and `STATUS.md`, and must emit `S1_CLOSEOUT_RECEIPT_V9.json` plus sidecar. Prompt SHA must remain unchanged. Validate control-plane mirrors, Framework and Hook policy.

## Task 8 — Import scope, readiness, Gate A.P

After closeout, generate import scope from Git objects with V9 tooling; permit only `jovi_commerce/**`, `docs/commerce/**`, `schemas/commerce/**`, `tests/commerce/**`, synthetic fixtures, `pyproject.toml`, `.gitignore`, `.gitattributes`; exclude products, Hook, Manifest, Decision, Approval, human-only, runtime data, external Xianyu and real data. Run post-closeout chain and pre-gate readiness. Generate exactly one V9-bound Gate Plan. Jovi alone runs `Approve-Gate.ps1`; V9 verifier requires approver exactly `Jovi`, Gate A/P, Plan SHA and all V9/import bindings. Luna never writes Approval or its sidecar.

## Task 9 — C/APPLY and acceptance

Run V9 transition dry-run (zero writes), then the Jovi-authorized apply writing only the three state mirrors. Emit a transition receipt/sidecar bound to V9, Gate Plan, Approval, strict verification, closeout, Post-Apply and import scope. Run control-plane validation, post-transition readiness, post-transition chain, Framework, Hook/Manifest/human-only protections and Prompt SHA checks. Confirm no valid Git HEAD/remote was created and Commerce import/X2/pilot remain unstarted. Emit `GOVERNANCE_C_APPLY_ACCEPTANCE_V9.json` and sidecar.

## Verification and evidence

After every candidate task run the candidate unittest suite, PowerShell 5.1 parser, relevant governance tests, security semantics, `git diff --check` where a valid Git worktree exists, and explicit sidecar/manifest recomputation. Counts come only from machine reports. Update `tasks/todo.md`; update `STATUS.md` only through the bound transition where required; update frozen Obsidian `00/02/03/06` only after C/APPLY. The final state is governance-only; the next plan is `COMMERCE-IMPORT-PHASE2C` for Git baseline, Git-object import, main-root X2, Import Audit and merge-candidate freeze.
