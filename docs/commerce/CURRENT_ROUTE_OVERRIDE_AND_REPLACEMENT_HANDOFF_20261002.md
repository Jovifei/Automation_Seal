# Current Route Override — Complete Medusa Replacement / GitHub Bidirectional Handoff

Updated: 2026-10-03

## Authority

Jovi explicitly selected **COMPLETE_MEDUSA_REPLACEMENT**.

Historical Medusa R6/R2-R3/C2/C3/C4 materials remain immutable audit history, but they no longer define the active implementation route.

Actual replacement Runtime repository:

`Jovifei/Automation_Jovi`

Current remote state: repository exists, Public, empty, no Runtime source uploaded.

## Eligible source

Only the independent curated root may be published:

`734949ba047d33c76fc9fee013b1373404c14a6f`

Qualification reported from the local intake:
- 14 allowed raw blobs match;
- intake manifest binds provenance/hash/size;
- Python 3.14 offline 21 tests PASS;
- Gitleaks v8.24.0 new worktree/history: zero findings.

Old candidate `c091ac3f63ba96b37aba59d3f4184caf4659bff5` and inherited upstream history are forbidden because 10 scan findings remain unresolved/unqualified.

## Active workflow

Remote ChatGPT:
- plans a bounded stage;
- after source intake, implements/fixes directly in the authorized Runtime GitHub repository;
- commits changes and opens/updates a reviewable PR;
- reviews GitHub CI and immutable Git evidence.

Local Codex:
- pulls the exact reviewed remote commit;
- builds/tests in the real local environment;
- fixes stage-scoped failures;
- pushes the repair commit back.

Remote ChatGPT then:
- reviews the returned diff and CI;
- reads released execution evidence;
- accepts/blocks the stage and issues the next bounded implementation.

Jovi:
- performs final acceptance;
- controls repository visibility security tradeoffs;
- controls every real platform/commerce permission.

## Current stop

Before Runtime source publication:
- resolve the explicit Public→Private security-effects decision;
- do not upload old history;
- do not claim Runtime review.

After the clean root is uploaded and independently verified, the next stage is the Runtime CI/source-intake/build/restore implementation defined in:

`REPLACEMENT_RUNTIME_IMPLEMENTATION_STAGE_PLAN_20261002.md`

## Boundaries

- Runtime source stays out of Governance.
- No credentials/secrets.
- `issued_from_human=false`.
- All six real-action flags remain false.
- No real Xianyu/payment/customer/delivery/refund/n8n production behavior.
