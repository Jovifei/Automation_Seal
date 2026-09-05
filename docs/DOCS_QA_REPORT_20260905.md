# Documentation Alignment QA Report — 2026-09-05

**Scope:** `Jovifei/Automation_Seal` branch `commerce-c3-real-sku-readiness-20260905`  
**Purpose:** prove that new-agent entrypoints now describe the current Commerce V1 stage rather than historical Phase 0/Track P-I/Medusa-adoption routes.

## 1. QA target

Current canonical execution state in living docs:

`C4_HUMAN_PILOT_DECISION_PENDING`

Technical chain documented as completed:

`Governance -> Medusa R6 -> R2-R3 -> C2 Independent PASS -> C3 Independent PASS -> Runtime C3 Promotion PASS`

## 2. Living entrypoints updated

Root:
- `README.md`
- `README_FIRST.md`
- `00_先读我.txt`
- `AGENTS.md`
- `CODEX_START_PROMPT.txt`
- `CODEX_MASTER_TASK.md`
- `PROJECT_STATE.json`
- `NEXT_STEP_MAP.md`
- `FAST_TRACK.md`
- `DECISIONS_REQUIRED.md`
- `USER_ACTION_CHECKLIST.md`
- `FIRST_RUN_TROUBLESHOOTING.md`
- `CHANGELOG.md`

Docs:
- `docs/CURRENT_PROJECT_GUIDE.md`
- `docs/HISTORICAL_DOCUMENT_STATUS.md`
- `docs/DOCUMENTATION_ALIGNMENT_20260905.md`
- `docs/README.md`
- `docs/目录总览.md`
- `docs/00_*.md` through `docs/08_*.md`
- six category README files

Commerce:
- `docs/commerce/README.md`
- current topology / runtime governance / GitHub governance
- C2-C4 landing roadmap
- Post-R6 and 2026-09-03 handoff marked historical/completed
- OSS reuse map
- C3 audit mirror cleanup
- C4 plan / decision candidate / operational kit hardening

## 3. Historical evidence preservation

The documentation alignment intentionally did **not** rewrite historical evidence trees such as:

- `docs/openspec/changes/archive/**`
- `docs/superpowers/**`
- historical Medusa independent-audit result files
- frozen task plans with sidecars
- stale/failed evidence packages

Historical content can still contain old phrases such as Track P/I, X0-X4, Gate A, R2/R6 pending states, etc. These are now explicitly classified as historical and are not current execution authority.

## 4. Critical stale-state corrections

Corrected in living docs:

- `READY_FOR_CODEX_PHASE_0_A_X0` -> historical only
- `AWAITING_GATE_A_TRACK_APPROVALS` -> removed as current machine state
- Track P/I -> historical, not current execution route
- X0-X4 -> historical, not current C4 route
- “Medusa candidate / not adopted” -> Medusa v2.19.0 adopted Commerce Core
- old Python/SQLite C0-C6 -> historical only
- “C2/C3 pending” -> C2 and C3 completed with independent PASS
- “Runtime main still old baseline” -> local promoted C3 main recorded as reported anchor requiring local recomputation
- “Runtime remote=none” -> current state must be live-checked

## 5. C4 safety corrections

### C3 mirror
- Removed Windows escape/control-character corruption from boundary flag text.
- Preserved mirror status; did not alter local Runtime evidence.

### C4 Operational Kit
- Added `PRE_PUBLISH_QA_REQUIRED / DO_NOT_PUBLISH_AS_IS`.
- Removed prefilled fake completed Pilot orders.
- Real Pilot ledger now begins with zero real rows.
- Replaced unsupported marketing copy with `[VERIFIED_*]` evidence-bound skeleton.
- CRC is no longer described as correction.
- SHA256 is described as integrity hash/check value, not digital signature.
- `0.2.0-dev` and unsigned installer are explicit.
- Support taxonomy no longer hard-codes unverified product commands/features.

### C4 Decision Candidate
- Remains `issued_from_human=false`.
- Explicit Pre-Publish QA gate added.
- 99 CNY and 5–10 order values are described as candidates, not validated commercial facts.

## 6. OSS route consistency

Living docs now consistently state:

### Adopted
- Medusa v2.19.0
- Playwright
- Gitleaks v8.24.0
- Syft v1.20.0
- Redis/PostgreSQL/Docker

### Selective architecture reuse
- `makepay-apps/medusa-plugin-digital-downloads` @ `a5343ba18cee85b3eed674ed55d0de7e32aaa448`

### Product packaging references
- PyInstaller
- Inno Setup

### Deferred / non-blocking for C4
- Trivy
- harden-runner
- dependency-review
- SLSA/cosign
- n8n production
- Storefront/S3

## 7. Machine state consistency

`PROJECT_STATE.json` now records:

- `current_state = C4_HUMAN_PILOT_DECISION_PENDING`
- stage `C4_HUMAN_PILOT`
- `issued_from_human = false`
- six real-action flags false
- C2/C3/promotion listed completed
- old Gate approvals explicitly historical
- local C3/Runtime/Product anchors explicitly marked `recompute_before_use`

## 8. CI / repository QA

The branch uses GitHub Actions `C3 Reference QA` to compile/run reference verifier self-tests and parse machine-readable contracts. Documentation changes must retain a green run before merge.

This report itself does not claim local Commerce Runtime evidence was remotely recomputed; Runtime/Product anchors remain local facts that must be rechecked on the target machine.

## 9. Remaining known gaps after documentation cleanup

These are real project work, not documentation drift:

1. final C4 listing claim review against local C3 evidence;
2. current Xianyu digital-goods/refund rule refresh;
3. Jovi beta/dev/unsigned vs stable-first decision;
4. manual delivery transport freeze;
5. dedicated Runtime Git remote live check/create if needed;
6. Automation_Seal main branch protection;
7. Jovi C4 Human Pilot Decision;
8. real C4 Pilot/commercial validation.

## 10. Verdict

`DOCUMENTATION_MAINLINE_ALIGNED_FOR_C4_HANDOFF`

New agents should start with:

1. `docs/CURRENT_PROJECT_GUIDE.md`
2. `docs/HISTORICAL_DOCUMENT_STATUS.md`
3. `PROJECT_STATE.json`
4. `NEXT_STEP_MAP.md`
5. `docs/commerce/README.md`

and should not execute historical Phase 0/Track P-I/X0-X4/R2/R6/C2/C3 plans as current work.
