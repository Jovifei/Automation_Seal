# Replacement Runtime Implementation Stage Plan

Updated: 2026-10-03

## Stage identity

Stage ID:

`RUNTIME-R1-CLEAN-INTAKE-CI-BUILD-RESTORE`

Purpose:

After the eligible clean root is safely published to `Jovifei/Automation_Jovi`, Remote ChatGPT will **implement** the first bounded Runtime engineering stage on GitHub. This is not planner-only work.

The stage ends before any real platform integration.

## Preconditions

All must be true before remote implementation starts:

1. Target repository is exactly `Jovifei/Automation_Jovi`.
2. Jovi has resolved the Public→Private security-effects decision.
3. Runtime source has been uploaded from the independent curated lineage only.
4. Eligible root:
   `734949ba047d33c76fc9fee013b1373404c14a6f`.
5. `c091ac3f63ba96b37aba59d3f4184caf4659bff5` and its inherited upstream history are not reachable.
6. The independent root has the expected clean provenance; no graft/merge recreates rejected history.
7. The 14 initial-root files match `INTAKE_MANIFEST.json` by source blob / SHA256 / size. Validate the immutable root; compare and review later HEAD changes separately.
8. No secrets/credentials.
9. All real-action flags remain false and `issued_from_human=false`.

If any precondition fails, stop at:

`RUNTIME_CLEAN_INTAKE_BLOCKED`

## Remote implementation branch

Remote ChatGPT creates a reviewed branch from the accepted clean baseline, for example:

`codex/runtime-r1-ci-build-restore`

No force-push and no main overwrite.

Remote ChatGPT then directly implements/fixes the following on GitHub and returns exact commit/PR receipts.

## Work package A — provenance and intake CI

Implement machine-verifiable intake checks that fail closed on:

- unexpected parent/history;
- reachable rejected `c091ac3...` lineage;
- 14-file manifest mismatch;
- source blob/hash/size mismatch;
- missing provenance metadata;
- secret finding;
- real-action flag drift.

CI must record the exact commit SHA and run on pull requests.

The currently reviewed publication head `0cdf07ea99b05bb32ca517021357ee03c5ffc3ce`
only amends intake documentation on top of the eligible root. CI must distinguish
root provenance verification from intentional reviewed implementation/doc changes
at HEAD; do not require HEAD to remain byte-identical forever or ignore mismatches.

Security scanning:
- Gitleaks v8.24.0 or the repository's accepted pinned equivalent;
- scan working tree;
- scan complete **new** Git history;
- expected finding count: 0.

Do not weaken tests or exclude source paths merely to obtain green CI.

## Work package B — reproducible test/build baseline

Remote review first reads the uploaded repository and binds the actual dependency/install/test commands instead of inventing them.

Minimum acceptance:
- Python runtime/version requirement explicitly pinned or checked; current qualified environment is Python 3.14;
- clean dependency/install path documented;
- offline/synthetic unit suite executes in CI;
- no regression below the qualified 21 passing tests unless the remote review explicitly documents why the test inventory changed;
- deterministic or reproducibly described build output;
- generated artifacts kept out of source-control unless intentionally versioned;
- no network call to real Xianyu/payment/customer endpoints.

If the Runtime includes a container path, implement a pinned/reproducible container build. If it does not yet include one, the remote implementation may add the minimum Dockerfile/compose only after inspecting the source topology.

## Work package C — synthetic runtime health

Implement a synthetic-only smoke path:

1. start the Runtime with test-only configuration;
2. verify a local health/readiness endpoint or equivalent process readiness;
3. exercise the minimum offline business state transition supported by the uploaded implementation;
4. prove no real platform credential or endpoint is required;
5. shut down cleanly.

The test environment must be loopback/private/synthetic only.

## Work package D — idempotency / restart / restore

The exact mechanism depends on the uploaded persistence model and is finalized only after source inspection.

Minimum acceptance where persistence exists:

- create deterministic synthetic state;
- execute the same synthetic request/event twice;
- prove duplicate externally meaningful records are not created;
- restart the process/container;
- prove accepted state remains readable and consistent;
- run a recovery/replay after restart;
- prove replay remains idempotent;
- if backup/export is supported, create a synthetic backup, restore it into an isolated fresh target, and compare required state.

If the initial Runtime is intentionally stateless, CI must instead prove that fact and test restart determinism; do not fabricate a persistence/restore feature merely to satisfy this section.

## Work package E — failure and rollback evidence

At least these failure classes must fail closed where applicable:

- malformed input;
- duplicate/replay;
- missing required local artifact/config;
- corrupted persisted synthetic state or invalid restore source;
- prohibited real-action configuration;
- secret-like test fixture accidentally added.

Rollback policy:
- main remains unchanged until PR review;
- last accepted clean baseline remains addressable;
- failed feature commits are reverted or the PR is abandoned;
- no history rewrite;
- no deletion of Governance or Runtime evidence;
- rollback never enables a real-action flag.

## Remote → local → remote acceptance loop

### Remote first pass

Remote ChatGPT:
- inspects the uploaded clean Runtime;
- implements work packages A–E on GitHub;
- runs available GitHub CI;
- returns branch, full commit SHA, PR, changed-file list and CI evidence.

### Local verification

Local Codex:
- pulls the exact remote commit;
- runs the bound install/build/unit/integration/synthetic/restart/restore suite;
- records command/exit/output evidence;
- fixes only stage-scoped failures;
- commits and pushes repairs back to the same reviewed branch.

### Remote re-review

Remote ChatGPT:
- verifies the pushed commit exists on GitHub;
- reviews the complete diff from accepted baseline;
- reviews GitHub CI;
- reads released local execution output;
- checks that no real-action gate changed;
- returns PASS / CHANGES_REQUIRED / BLOCKED with exact evidence.

## Acceptance state

Only after both GitHub CI and local execution evidence pass may the stage become:

`RUNTIME_R1_CLEAN_INTAKE_CI_BUILD_RESTORE_PASS`

That state still does **not** authorize:
- real Xianyu;
- payment;
- real customer data;
- auto delivery;
- refund/dispute automation;
- n8n production;
- C4 Human Pilot.

Those remain separate Human Decisions.
