# C4 Runtime Remote Promotion Closure — 2026-09-06

**Status:** `C4_RUNTIME_REMOTE_PROMOTION_CLOSED`

This record closes the remote Runtime side of C4 Pre-Publish QA. It does not authorize the C4 Human Pilot.

## 1. Runtime authoritative remote

Repository:

`Jovifei/jovi-medusa-commerce-v1`

C3 main before C4 readiness promotion:

`63db06e9628331982893929f39b1037077138480`

C4 readiness feature head and promoted Runtime `main`:

`b7ec762f29092106ad10c88d72bc682b5f9e7ac2`

Runtime PR:

`#1 — C4 pre-publish readiness evidence and human-decision gate`

Promotion method:

`FAST_FORWARD`

GitHub records PR #1 as merged, with merge commit SHA equal to the feature head itself:

`b7ec762f29092106ad10c88d72bc682b5f9e7ac2`

## 2. Independent remote diff review

The C4 feature line was reviewed against C3 Runtime main.

C4 introduced no changes under:

`audit-source/**`

The promoted changes are limited to governance/readiness evidence, delivery-archive ignore rules and CI-harness maintenance. No Commerce business implementation was changed for C4 Pre-Publish QA.

## 3. CI defects exposed and repaired before promotion

### 3.1 Historical R6 source-tree baseline

The old Runtime PR workflow still compared the current audited Runtime against the original R6 import source-tree hash:

`e533f0ce0010cc0f75848b9854d8ccd4da364768f31174349d8981827342f8aa`

The existing authoritative tree verifier recomputed the current C3-derived `audit-source` tree as:

`3101604bf10c9c6ed3c9b67a23e5ef77a6704472835ccfd536c2cc0b6b8e568a`

with 94 files.

Because the C4 diff contains zero `audit-source/**` changes, this was classified as a stale CI baseline rather than C4 source drift. The correction and rationale are preserved in Runtime:

`governance/c4/C4_RUNTIME_CI_BASELINE_RECONCILIATION.md`

No audited source file was modified to make this check pass.

### 3.2 C2 fixture path on GitHub Actions

Two C2 unit suites initially failed before their assertions because GitHub Actions could not discover the already tracked frozen fixture through local-machine path assumptions.

The test code already supports:

`JOVI_C2_FIXTURE_ROOT`

Runtime CI now binds that variable to the tracked fixture:

`audit-source/tests/fixtures/c2-synthetic-digital-pack`

and validates its `SHA256SUMS.txt` before unit execution.

No unit-test source and no fixture byte was modified.

### 3.3 Current synthetic regression harness

Historical R6/C2 evidence scripts remain preserved. A separate current C4 CI harness was added at:

`governance/c4/ci/regression.sh`

It is cross-platform for GitHub Actions/Linux and Windows Git-Bash path handling and runs the inherited synthetic Commerce surface in an isolated Docker network.

## 4. Final Runtime GitHub Actions result

Workflow run:

`34016366716`

Head:

`b7ec762f29092106ad10c88d72bc682b5f9e7ac2`

Conclusion:

`SUCCESS`

### Static checks

- audited `audit-source` tree SHA: PASS (`3101604b...`, 94 files)
- frozen R2 evidence sidecars: PASS
- C4 governance sidecars: PASS
- C2 fixture checksums: PASS
- frozen pnpm dependency install: PASS
- TypeScript: PASS
- secret scan: PASS, 0 findings
- Jest unit: 9/9 suites PASS, 41/41 tests PASS
- License/SBOM: PASS

### Isolated Runtime regression

- Jest unit: PASS
- Jest module integration: PASS
- X2 first: PASS
- X2 replay: PASS
- X2 concurrency: PASS
- X2 negative: PASS
- C2 first: PASS
- C2 replay: PASS
- C2 concurrency: PASS
- C2 negative: PASS
- C2 HTTP download: PASS

Terminal result:

`C4_RUNTIME_SYNTHETIC_REGRESSION_PASS`

## 5. Runtime C4 evidence preserved on main

Runtime main now contains the local C4 readiness evidence, including:

- C3 Runtime Git reconciliation;
- listing claim review;
- customer package inventory;
- manual delivery transport freeze;
- Xianyu human-rule check record;
- C4 pre-publish readiness record;
- Runtime CI baseline reconciliation;
- current C4 CI regression harness and integrity sidecar.

Local evidence reports the C4 readiness terminal state:

`C4_PRE_PUBLISH_QA_READY_FOR_HUMAN_DECISION`

## 6. Human authorization boundary

The following remains unchanged:

`issued_from_human=false`

All six real-action flags remain false:

- `production_integration_allowed=false`
- `real_payment=false`
- `real_customer=false`
- `xianyu=false`
- `auto_delivery=false`
- `n8n_production=false`

This closure does not authorize:

- publishing a real Xianyu listing;
- confirming a real payment through automation;
- saving raw buyer PII/Profile/chat data;
- automatic delivery;
- automatic refund/dispute handling;
- any production/n8n real-platform action.

## 7. Next authority

Governance must now bind this promoted Runtime main and close Governance PR #5 with its own C3/C4 CI green.

After Governance mainline closure, the only required business gate before a real C4 Pilot starts is Jovi's explicit Human Pilot Decision, including final price and final pilot size/time-window binding.

A recommended decision candidate may use `99 CNY` and `maximum 10 paid Pilot orders or 14 calendar days, whichever occurs first`, but those values remain proposals until Jovi explicitly signs them.
