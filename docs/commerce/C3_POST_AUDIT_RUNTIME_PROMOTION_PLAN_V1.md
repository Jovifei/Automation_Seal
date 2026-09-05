# C3 Post-Audit Runtime Promotion Plan V1

## Problem this solves

The Commerce Runtime protected `main` intentionally remained at the original controlled-import baseline while R2-R3, C2, and C3 were developed and independently audited on descendant feature branches.

That is correct during validation, but C4 should not run indefinitely from a temporary feature branch. After C3 passes, the exact audited runtime bytes must become an explicit authoritative release line before a human pilot.

## Preconditions

All must exist and be recomputed locally:

- `R6_POST_IMPORT_PASS`
- `R2R3_INDEPENDENT_AUDIT_PASS`
- `C2_INDEPENDENT_AUDIT_PASS`
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- C3 audit closure commit is clean and frozen
- six real-action flags remain false

## Human Decision required

Create a separate Jovi human decision:

`JOVI_RUNTIME_C3_PROMOTION_DECISION_V1`

The decision must bind:

- current Runtime main SHA;
- C3 audited implementation SHA;
- C3 audit closure SHA;
- C3 audit result SHA256;
- C3 source-tree SHA256;
- pnpm lock SHA256;
- C3 release-candidate SHA256;
- C3 product source HEAD and artifact SHA256 values;
- rollback main SHA.

## Promotion scope

Allowed only after the human decision:

1. prove the C3 audit closure commit is the intended descendant of the existing Runtime main/history;
2. move Runtime `main` to the **exact already-audited C3 closure commit**, preferably by fast-forward when ancestry permits;
3. do not squash/rewrite audited commits in a way that changes source bytes;
4. create a release marker/tag such as `c3-pilot-candidate-v1` only after exact binding is verified;
5. run a read-only Post-Promotion Audit.

No product/runtime code edits are allowed in the promotion transaction.

## Post-Promotion Audit

A fresh read-only auditor must verify:

- `main == audited C3 closure commit` or an explicitly approved byte-equivalent promotion commit;
- source tree equals audited C3 source tree;
- pnpm lock unchanged;
- product release artifact SHA bindings unchanged;
- all C3 evidence sidecars still match;
- C3 E2E critical smoke/replay still pass;
- six real-action flags remain false;
- no production deployment or platform action occurred.

Pass state:

`C3_RUNTIME_PROMOTION_AUDIT_PASS`

## Runtime GitHub remote

Only after C3 audit/pass and Jovi promotion authorization should the Runtime be bound to its own remote, recommended:

`Jovifei/jovi-medusa-commerce-v1`

Do not copy Runtime source into `Automation_Seal`.

Initial remote push should preserve audited history/branches/tags. After push:

- protect `main` / PR-only;
- block force push and deletion;
- require typecheck/unit/integration/security/provenance checks once workflows are confirmed stable;
- keep real deployment disabled.

## What this does NOT authorize

Promotion does not authorize:

- production deployment;
- real payment automation;
- real customer data ingestion;
- automatic Xianyu access;
- auto delivery;
- n8n production;
- automatic refund;
- Storefront publication.

## C4 entry

Only after:

`C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`

and

`C3_RUNTIME_PROMOTION_AUDIT_PASS`

may Jovi consider the separate:

`C4_HUMAN_PILOT_DECISION`

This keeps Pilot execution anchored to a formal Runtime main rather than an ephemeral feature branch.
