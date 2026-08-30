# Commerce Governance Closure V11 Installed-Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `executing-plans` and `test-driven-development`. Use fresh Luna `gpt-5.6-terra` with `xhigh` reasoning for independent audits only. Never use sol. Never run human-only scripts.

**Goal:** Replace the invalidated V10 structural candidate with a V11 candidate that proves the complete *installed* Framework contract in an isolated root before a future human Decision or live write is considered.

**Architecture:** V10 corrected the receipt schema but its isolated test only proved transactional publication. It did not execute the unchanged security-semantics runner against the replacement S2A1 test file. V11 keeps the V10 receipt repair, treats V10’s signed apply/fail/rollback sequence as immutable history, and narrows the physical transaction to the 12 bytes that actually change plus `FRAMEWORK_MANIFEST.sha256`. `tests/test_s2a1_control_plane.py` remains at its existing 20-case byte image, while becoming a verified non-transaction Framework entry. The V11 isolated-root test must execute the actual V11 `--apply` and then execute every installed governance contract before reporting GREEN.

**Tech Stack:** Bundled Python 3.12 standard library, JSON UTF-8 bytes, SHA-256 body sidecars, Windows PowerShell 5.1 parser, `unittest`.

## Global Constraints

- Formal V7 (`a7bafcdf4c3f26848338f8abd1c5773edbe18c4b8b447613b6acfb4d8a194204`), V9 (`af24e7ce181d5f5520be4570351e3cfe243b07562625d80928a79c684122c1bb`) and V10 (`553778744601445a29988fb31e471f68856f15f1c31089e9fde9e3186ec16e5d`) remain immutable historical decisions.
- The V9 journal remains `ROLLED_BACK_AFTER_FAILURE`; the V10 journal remains `ROLLED_BACK`; neither receipt root, its backups, receipt, report or sidecars may be deleted, overwritten, recovered, or reused for V11.
- V10 Post-Apply FAIL report SHA `96bb6de09aa80d676591373d4755305c1ab76f3128dfde6a477cd82b3ee5a25e` and V10 rollback audit SHA `5e49017a898989f0bfd15bb88d7c3eb32760a466c0103d33d22bb0a64657f682` are mandatory V11 historical inputs.
- Candidate-only files may be written only under `workspace/review-queue/commerce-v1/governance-closure-v11/` until a fresh independent V11 pre-apply PASS and a new Jovi Decision V11 exist.
- V11 transaction scope is exactly 12 structural targets plus `FRAMEWORK_MANIFEST.sha256` = 13 physical writes. `tests/test_s2a1_control_plane.py` is an active Framework entry but is deliberately not a physical transaction target because its current raw byte SHA is the required V11 after SHA.
- No hook trust change, `MANIFEST.sha256` write, approval write, human-only execution, Gate, Commerce import, Git initialization, external Xianyu access, payment, delivery, product write or real platform action is allowed.
- Candidate package coverage is exact: exclude only Decision V11 body/sidecar, package manifest body/sidecar, future independent audit body/sidecar, future execution receipts and `__pycache__`; all other candidate bodies and sidecars are covered exactly once.

## Authoritative Inputs

- Current restored root must contain 12 V11 structural before bytes plus Framework before bytes exactly matching a newly generated V11 target set.
- Current raw SHA for `tests/test_s2a1_control_plane.py` is `e47b0fa80c5cda9e69461df3cc62a0d4ca9db26b8104da2cacac3c03042c9761`; V11 Framework candidate must bind that value, not V10’s incompatible `aa05e553...` byte image.
- `scripts/run-security-semantics.py` SHA `bc106082a5735a87aaa3b74735debb93810ea2feb4e4221d075e39c690720cf6` must remain compatible with the active S2A1 test image and must execute `S2A1CoreTests` 20/20 in the V11 isolated after-state.

---

### Task 0: Freeze the failed V10 sequence and the restored root

**Files:**
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/inputs/V10_FAILURE_AND_ROLLBACK_EVIDENCE.json`
- Copy: formal V10, V10 source candidate/package/pre-audit, V10 structural receipt/journal/backups manifest, V10 Post-Apply FAIL report, V10 rollback audit, prior V9 history and all required sidecars.
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/inputs/V11_RESTORED_BEFORE_SNAPSHOT.json`

- [ ] Rehash formal V10, V10 receipt/journal, V10 FAIL report and V10 rollback audit; require their sidecars and their stated statuses.
- [ ] Rehash the V10 rollback root after completion. Require all prior physical targets to equal V10 before bytes and require the V10 journal to be `ROLLED_BACK`.
- [ ] Record the exact historical cause: the applied V10 S2A1 image defined `V9S2A1Tests`/two tests while the active Framework runner required `S2A1CoreTests`/twenty tests.
- [ ] Require the V9 journal and its 14 backups to remain unchanged and require no V9 structural receipt.

### Task 1: TDD the complete installed-contract gate

**Files:**
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/tests/test_v11_installed_contract.py`
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/tests/test_v11_structural_receipt.py`
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/tools/v11_runtime.py`
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/tools/apply_phase2b_structural_v11.py`

**Interfaces:**
- `stage_v11_root(tmp: Path) -> StagedV11Root` copies the restored root, copies the V11 candidate package, creates a test-only issued V11 Decision and pre-audit, and never touches the real root.
- `run_v11_apply(stage: StagedV11Root) -> subprocess.CompletedProcess[str]` executes the real V11 tool.
- `run_installed_contract(stage_root: Path) -> list[CompletedProcess[str]]` runs all listed root commands after actual isolated APPLY.

- [ ] Write a failing test that stages the old V10 after-images and asserts `scripts/run-security-semantics.py` returns exit 0 and `20/20 PASS`; confirm RED with `SECURITY_SEMANTICS_FAIL` and collection `0/20`.
- [ ] Write a failing test that requires V11’s Framework candidate to bind the existing S2A1 raw bytes and rejects a target set that asks V11 to write that path.
- [ ] Implement the minimum correction: use the existing 20-case S2A1 byte image as the V11 Framework entry, remove it from V11 structural target rows, and retain V10’s full receipt-row builder/validator.
- [ ] In the same staged root after real V11 `--apply`, run these commands and require every exit code to be zero:

```text
python -B scripts/run-security-semantics.py
python -B -m unittest tests.test_commerce_gate_readiness -v
python -B -m unittest tests.test_control_plane_commerce_transition -v
python -B tests/test_s1_integrity.py
python -B tests/test_s2a1_control_plane.py
python -B tests/test_s2a2_enforcement.py
python -B tests/hooks/test_pre_tool_guard.py
```

- [ ] Assert the isolated V11 receipt has exactly 13 rows, each exactly `{path,before_bytes,before_sha256,after_bytes,after_sha256}`, journal=`APPLIED`, Framework=40/40 candidate and protected snapshot equality.
- [ ] Add negatives for legacy receipt rows, tampered temporal fields, V9/V10 receipt-root reuse, no-op S2A1 path in the transaction set, and a staged runner/S2A1 contract mismatch.

### Task 2: Build the V11 structural package

**Files:**
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/inputs/V11_STRUCTURAL_TARGET_SET.json`
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/inputs/FRAMEWORK_MANIFEST_V11_CANDIDATE.sha256`
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/inputs/V11_EXACT_DIFF.json`
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/proposed-structural/**` for exactly 12 changed paths.
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/DECISION_V11_PROPOSED.json`
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/Issue-DecisionV11.ps1`
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/V11_REVIEW_PACKAGE.md`
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/V11_IMPLEMENTATION_REPORT.md`

- [ ] Generate target rows from raw current before bytes. Reject duplicate, drive-qualified, UNC, ADS, reserved-device, casefold/NFC-colliding, Hook, `MANIFEST.sha256`, approval, human-only, product and external paths.
- [ ] Build Framework candidate with 40 exact entries. Its S2A1 entry must equal the restored current raw SHA, and Framework must describe all 40 after bytes with no stale V10 `aa05e553...` entry.
- [ ] Compute exact diff from the current Framework bytes and candidate bytes rather than hardcoding counts.
- [ ] V11 Decision must supersede formal V10 and bind V10 formal/source/pre-audit/receipt/journal/Post-Apply FAIL/rollback audit, V11 target/diff/framework/package/review/tools/tests and all shared runtime dependencies.
- [ ] `Issue-DecisionV11.ps1` must require separate candidate, package, V10 history, review and independent-audit SHA arguments; verify `PASS_READY_FOR_JOVI_DECISION_V11`, `independent=true`, candidate/package bindings; refuse to overwrite V7/V9/V10/V11 formal objects; after exact Jovi confirmation atomically write only formal V11 body/sidecar.
- [ ] V11 executor must require the canonical formal V11 path, exact package-member rehashing, exact 13 target before values, actual Framework 40 verification, no preexisting V11 receipt child and a new V11-only receipt root.

### Task 3: Freeze and self-verify the candidate

**Files:**
- Create: `workspace/review-queue/commerce-v1/governance-closure-v11/V11_PACKAGE_MANIFEST.json`
- Create: matching `.sha256.sidecar` files for every body.

- [ ] Generate all body sidecars before the package manifest.
- [ ] Generate the package manifest last, with exact allowed exclusions only.
- [ ] Without modifying the candidate, rehash every package member and every body/sidecar relationship, Decision binding, target row and Framework entry.
- [ ] Run bundled Python 3.12 candidate tests, Python compilation and Windows PowerShell 5.1 parser. Record observed counts, not hand-written counts.
- [ ] Status may become only `V11_INSTALLED_CONTRACT_CANDIDATE_FROZEN`; no formal V11 must exist yet.

### Task 4: Fresh independent V11 pre-apply audit

**Files:**
- Write-only audit output: `workspace/review-queue/commerce-v1/governance-closure-v11/preapply-evidence/V11_INDEPENDENT_PREAPPLY_AUDIT.json` and sidecar.

- [ ] Use a fresh Luna auditor that did not implement V11.
- [ ] Require package exact coverage, Decision bindings, V10 historical evidence preservation, current 13 V11 before bytes, Framework candidate 40/40 semantics, and no formal V11.
- [ ] Re-run the real isolated V11 apply and the full installed contract. Do not accept unit-only receipt validation.
- [ ] Rehash the real root and canonical mirror read-only. If ACL access prevents a required byte check, report `FAIL_NOT_READY_FOR_JOVI_DECISION_V11`; do not infer PASS from V10 evidence.
- [ ] Audit must report only `PASS_READY_FOR_JOVI_DECISION_V11` or a fail-closed verdict. It must not run Issue/APPLY/rollback/recover/human-only/Gate/import/transition/external actions.

### Task 5: Jovi Decision V11 and bounded apply

- [ ] Only after Task 4 PASS, derive all mandatory PowerShell parameters from the then-current script signature and rehash every supplied body in the same turn.
- [ ] Jovi alone executes `Issue-DecisionV11.ps1` and confirms `ISSUE DECISION V11 <candidate-prefix>`.
- [ ] Recheck formal V11 body/sidecar, issuance bindings and false authority flags.
- [ ] Run V11 `--check` requiring `target_count=13`, `writes=0` and no V11 receipt child.
- [ ] Run V11 `--apply` once using a new child receipt directory. Require receipt/journal sidecars, 13 full rows, Framework 40/40 and V10/V9 history preservation.
- [ ] A post-write failure requires signed V11 rollback/recover, independent recovery audit, and a new candidate/Decision; never retry V11 in place.

### Task 6: Independent V11 Post-Apply audit and handoff

- [ ] A second fresh Luna auditor rehashes all after targets, Framework 40/40, receipt/journal/backups, formal lineage and protected non-target tree.
- [ ] Auditor must execute the seven installed-contract commands from Task 1 in the real root and require `SECURITY_SEMANTICS_PASS` 20/20.
- [ ] Require `MANIFEST.sha256`, Hook three components, human-only tree, approvals, V7/V9/V10/V11 decisions and V9/V10 history to be unchanged; control plane remains `S1/CLOSED`; no Gate, import, main X2 or platform action exists.
- [ ] Only `PASS` Post-Apply result may unblock the original V9 plan’s closeout/Gate work. Any FAIL stops at rollback/new candidate.

## Self-review checklist

- V10’s regression is covered by an actual V11 isolated APPLY followed by the unchanged security-semantic entrypoint; a passing receipt alone is explicitly insufficient.
- The S2A1/runner pair has one coherent byte contract: runner expects 20, active file defines 20.
- V11 reduces rather than expands live write scope: 12 structural bodies plus Framework manifest.
- V9 and V10 failure/rollback evidence is immutable and hash-bound.
- No instruction above authorizes human-only scripts, approvals, real Commerce, Git, or external Xianyu actions.
