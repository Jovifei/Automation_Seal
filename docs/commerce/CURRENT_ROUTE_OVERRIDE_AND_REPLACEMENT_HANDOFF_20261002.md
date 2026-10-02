# Current Route Override — GitHub Bidirectional Replacement Handoff

Date: 2026-10-02

## Authority

This document is a current-route override layer. Historical Medusa/C4 audit records remain preserved for traceability, but they are not the only active planning route after explicit Jovi direction for GitHub bidirectional handoff.

## Active Workflow

Remote ChatGPT/Governance:
- plan bounded stages;
- implement and fix code in the appropriate authorized GitHub repository (Governance here; Runtime source in its own repository after intake);
- review GitHub evidence;
- commit reviewable changes.

Local Codex:
- pull approved branches;
- build/test local Runtime baseline;
- fix implementation issues;
- push verified results.

Remote review:
- inspect immutable Git evidence;
- review tests and contracts;
- decide next bounded stage.

## Boundaries

- No Runtime source is copied into Governance.
- No credentials/secrets are stored.
- `issued_from_human=false` remains required.
- Real payment, Xianyu write actions, auto delivery and production automation remain disabled.

## Replacement Runtime Intake

The new Runtime repository is not accepted until:

1. repository exists and is private;
2. source baseline commit is uploaded unchanged;
3. commit SHA can be independently verified;
4. CI/test entrypoints are documented;
5. rollback reference is recorded.

Until then, Runtime code review is not claimed.
