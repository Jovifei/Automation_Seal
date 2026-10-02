# Replacement Runtime Implementation Stage Plan

## Stage R1 — Source Intake

Goal:
Accept the new Runtime baseline without replacing history.

Acceptance:
- private repository available;
- exact baseline commit recorded;
- no secrets;
- no real-platform integration;
- Governance only stores evidence/contracts.

## Stage R2 — Build and CI Baseline

Required evidence:
- reproducible install;
- build/test commands;
- CI workflow;
- dependency/security scan;
- failure rollback path.

## Stage R3 — Runtime Review

Remote review checks:
- architecture;
- data boundaries;
- APIs;
- persistence;
- tests;
- security boundaries.

No commercial PASS is granted from source upload alone.

## Rollback

Rollback requires:
- preserved baseline SHA;
- reversible branch movement;
- no history rewrite;
- no deletion of audit evidence.
