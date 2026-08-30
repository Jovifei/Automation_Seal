# Commerce Governance Closure V12 Self-Binding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `executing-plans` and `test-driven-development`. Use fresh Luna `gpt-5.6-terra` with `xhigh` reasoning for the independent audit. Never use sol. Never run human-only scripts.

**Goal:** Supersede the already-issued but pre-APPLY-blocked V11 Decision with a candidate whose formal Decision binds every V12 executable and shared runtime dependency before the executor is allowed to run.

**Architecture:** V12 is a candidate-only copy of the V11 R3 installed-contract package. It changes no structural target bytes; it repairs the Decision/issuer/runtime self-binding contract and adds a regression proving that the exact formal Decision used by `--check` contains the executor and runtime hashes. V11 remains immutable historical evidence and is never overwritten or retried.

**Tech Stack:** Bundled Python 3.12 standard library, UTF-8 JSON, SHA-256 body sidecars, Windows PowerShell 5.1 parser, `unittest`.

## Global Constraints

- V11 formal `c0dd781bdd8801680dcb6fe6afca41629a01b82f770ca637b34460b72ddd816f` is immutable history; its first `--check` stopped with `missing or malformed SHA-256: V11 executor self binding` and created no receipt directory.
- V11 candidate `70cff920259cc8c6ece5e1c201e17eb93749038d5f2316fc2eeb755f54e0745d`, package `e4868b30911731ef2c4f7b1673e7b67a653395888733747cc110ae8edf638a80`, and independent PASS `c34a3b46d7ce131f55cbc57ef24482f80438fb45d31776e8e209cb6e5e025741` are copied as historical inputs only.
- V12 candidate files may be written only under `workspace/review-queue/commerce-v1/governance-closure-v12/` until a fresh V12 audit and new Jovi Decision exist.
- No V12 real-root APPLY, Gate, import, Git initialization, Hook change, approval write, human-only script, external Xianyu access, product write, payment or platform action is allowed before the new Decision and bounded check.
- Physical structural scope remains exactly the V11 scope: 12 changed structural files plus `FRAMEWORK_MANIFEST.sha256` = 13 targets. The S2A1 20-case file remains a non-transaction Framework entry.
- A package manifest is generated once, after all staged tests pass; after that write only read-only verification is allowed. Exclude only V12 Decision body/sidecar, V12 package manifest body/sidecar, the future V12 audit body/sidecar, execution receipts, and `__pycache__`; preserve all V11 failure/history inputs.

## Authoritative V12 Contract

The V12 proposal must have:

```json
{
  "schema_version": 12,
  "status": "CANDIDATE_ONLY",
  "supersedes": "JOVI_S1_RESTART_DECISION_V11",
  "hook_status": "DO_NOT_TRUST",
  "hook_runtime_dependency": false,
  "hook_restore_allowed": false,
  "hook_trust_allowed": false,
  "track_p_allowed": false,
  "track_i_allowed": false,
  "real_platform_actions_allowed": false,
  "manifest_apply_scope": ["FRAMEWORK_MANIFEST.sha256"]
}
```

`bindings` must include 64-hex SHA values for the V11 formal Decision, V11 proposal, V11 package, V11 R3 PASS, V11 check-blocked evidence, V11 structural target/diff/Framework, V12 package, V12 review/report, the V12 executor, V12 runtime and every shared V12 tool dependency. Empty strings and unbound entrypoints are invalid. The V12 issuer must copy these exact bindings into the formal V12 Decision and add `issuance_bindings` for candidate, package, independent audit and V11 lineage.

## Task 0: Freeze V11 failure input

**Files:**

- Create: `workspace/review-queue/commerce-v1/governance-closure-v12/inputs/V11_CHECK_BLOCKED_EVIDENCE.json` and sidecar.
- Copy with bytes and sidecars: V11 formal Decision, V11 proposal/package/audit, V11 review/report, V11 target/diff/Framework, V11 R1 FAIL history, V10/V9 history.

- [ ] Recompute V11 formal body and sidecar, require `status=ISSUED`, `approver=Jovi`, all policy booleans false, and no V11 receipt child.
- [ ] Record the exact bounded check command, exit code `2`, error `missing or malformed SHA-256: V11 executor self binding`, receipt path absence, and current 13/13 before-state hashes. Do not claim an APPLY or rollback occurred.
- [ ] Verify V7, V9 and V10 formal bytes, V9/V10 journals, V10 failure audit and V10 rollback audit are unchanged.

## Task 1: TDD the formal self-binding repair

**Files:**

- Create: `workspace/review-queue/commerce-v1/governance-closure-v12/tests/test_v12_self_binding.py`.
- Create/modify only in V12 candidate: `tools/v12_runtime.py`, `tools/apply_phase2b_structural_v12.py`, `Issue-DecisionV12.ps1`.

- [ ] RED test: copy the issued V11 formal Decision and run the V12-compatible check path; assert it rejects the missing executor binding before creating a receipt.
- [ ] RED test: remove the V12 runtime binding or replace it with a non-64-hex value; assert fail-closed.
- [ ] GREEN implementation: require exact canonical formal path `workspace/decisions/JOVI_S1_RESTART_DECISION_V12.json`; require `structural_executor_v12_sha256`, `v12_runtime_v12_sha256`, package-manifest SHA and all shared dependency SHAs before target reads.
- [ ] GREEN test: create a test-only issued V12 Decision from the candidate proposal, run `--check`, assert `target_count=13`, `writes=0`, no receipt child and all self-bindings match.
- [ ] GREEN test: run actual isolated V12 `--apply`, validate 13 full temporal rows, `APPLIED` journal, Framework 40/40, protected snapshot equality, and all seven installed governance commands with `SECURITY_SEMANTICS_PASS` 20/20.
- [ ] Negative tests: V11/V10 receipt-root reuse, formal V11 path passed to V12, missing/changed shared runtime, stale target/diff/framework, and tampered package member.

## Task 2: Freeze the V12 candidate

**Files:**

- Create: `workspace/review-queue/commerce-v1/governance-closure-v12/DECISION_V12_PROPOSED.json` and `Issue-DecisionV12.ps1`.
- Create: `V12_REVIEW_PACKAGE.md`, `V12_IMPLEMENTATION_REPORT.md`, `inputs/V12_STRUCTURAL_TARGET_SET.json`, `inputs/V12_EXACT_DIFF.json`, `inputs/FRAMEWORK_MANIFEST_V12_CANDIDATE.sha256`, `tests/**`, `tools/**`.
- Create last: `V12_PACKAGE_MANIFEST.json` and sidecar.

- [ ] Copy V11 target bytes unchanged and prove 13 targets, Framework 40/40 and exact diff computed from actual Framework bytes.
- [ ] Bind every V12 executable and shared dependency in the proposal before producing its sidecar.
- [ ] Make `Issue-DecisionV12.ps1` require separate candidate, package, V11-history, review and independent-audit SHA arguments plus exact confirmation `ISSUE DECISION V12 <candidate-prefix>`. It must refuse to overwrite V7/V9/V10/V11/V12 formal objects.
- [ ] Preserve `V11_CHECK_BLOCKED_EVIDENCE.json` as a bound historical input and state that no V11 receipt or target write occurred.
- [ ] Run bundled Python 3.12 tests, compile all candidate Python, parse all candidate PowerShell with Windows PowerShell 5.1, and rehash every body/sidecar and Decision binding.
- [ ] Generate the V12 package manifest once, then perform only read-only 100% member/sidecar verification. Status becomes `V12_SELF_BOUND_CANDIDATE_FROZEN`; no formal V12 exists.

## Task 3: Fresh independent V12 pre-apply audit

Use a fresh Luna `gpt-5.6-terra` `xhigh` agent that did not build V12. It may write only:

```text
workspace/review-queue/commerce-v1/governance-closure-v12/preapply-evidence/V12_INDEPENDENT_PREAPPLY_AUDIT.json
workspace/review-queue/commerce-v1/governance-closure-v12/preapply-evidence/V12_INDEPENDENT_PREAPPLY_AUDIT.json.sha256.sidecar
```

- [ ] Rehash the complete package, every body/sidecar, all V11 failure inputs, every Decision binding, 13 live before targets, Framework 40/40 and canonical mirror.
- [ ] Independently run V12 tests with the frozen manifest present, including actual test-local `--check`, `--apply`, seven installed contracts and 20/20 security semantics.
- [ ] Verify formal V11 is unchanged, formal V12 is absent, no V12 receipt child exists, and no human-only/real-root action ran.
- [ ] PASS only as `PASS_READY_FOR_JOVI_DECISION_V12`; any missing binding, ACL, stale byte or unrun dynamic test is fail-closed.

## Task 4: Jovi issuance and bounded V12 apply

- [ ] Derive the exact current `Issue-DecisionV12.ps1` parameters and hashes in the same turn immediately before sending Jovi the command.
- [ ] Jovi alone runs the issuer and confirms `ISSUE DECISION V12 <candidate-prefix>`.
- [ ] Rehash formal V12 body/sidecar and verify candidate/package/audit/V11 lineage and all false permissions.
- [ ] Run V12 `--check`; require `target_count=13`, `writes=0`, no receipt child and no target changes.
- [ ] Run V12 `--apply` exactly once under a new V12 receipt child. If any post-write validation fails, use only signed V12 rollback/recover, obtain an independent recovery audit, and create a new superseding candidate; never retry in place.

## Task 5: Independent V12 post-apply audit

Use a second fresh Luna `gpt-5.6-terra` `xhigh` agent, different from the pre-apply auditor. It writes only the approved Post-Apply report and sidecar under `reports/remediation/`.

- [ ] Verify all 13 after bytes, Framework 40/40, receipt/journal/backups/sidecars, formal V12 bindings, V11/V10/V9 history and protected non-target trees.
- [ ] Run all seven installed commands in the real root; require `SECURITY_SEMANTICS_PASS` 20/20.
- [ ] Verify Hook DNT, `MANIFEST.sha256`, human-only tree, approvals, control plane `S1/CLOSED`, no Gate/import/main X2/real platform action.
- [ ] Only an independent `PASS` may reopen the original V9 closeout/Gate work. A FAIL stops with rollback/new candidate.

## Self-review and completion gate

- The V11 self-binding failure is a mandatory historical input, not a silent repair.
- The exact formal Decision used by `--check` is tested, so candidate-local synthetic bindings cannot hide an issuer defect.
- No V12 target byte differs from the V11 R3 target set; only the authorization/tool binding graph changes.
- No human-only script, approval file, Hook, Manifest, product, Commerce runtime, Git repository, external repo or platform action is touched before the new Decision and successful bounded check.
