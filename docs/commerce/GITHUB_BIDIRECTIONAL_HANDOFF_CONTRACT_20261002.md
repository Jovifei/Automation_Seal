# GitHub Bidirectional Handoff Contract

Updated: 2026-10-03

## Purpose

Define the authoritative implementation handoff for the complete Medusa replacement without mixing Runtime source into Governance or enabling any real-platform action.

## Repositories and authority

Governance:

`Jovifei/Automation_Seal`

Role:
- current-route policy and acceptance criteria;
- bounded implementation plans;
- audit/rollback contracts;
- cross-repo Git bindings;
- review conclusions.

Replacement Runtime:

`Jovifei/Automation_Jovi`

Current remote fact:
- repository exists;
- visibility: Public;
- size: 0 / source not uploaded;
- default branch: `main`.

Runtime role after clean intake:
- replacement implementation source;
- CI/build/test evidence;
- synthetic persistence/idempotency/restore evidence.

## Authoritative workflow

1. **Remote ChatGPT** defines a bounded stage and, after Runtime source intake, directly implements/fixes code on an authorized GitHub branch, commits it, opens/updates the PR, and returns immutable receipts.
2. **Local Codex** pulls that exact commit/branch, runs local build/tests, fixes failures within the stage, and pushes the repair commit back to the reviewed branch.
3. **Remote ChatGPT** independently reviews the returned Git diff, GitHub CI, and released local execution evidence before accepting the stage or issuing the next bounded implementation.
4. Jovi retains final human acceptance and every real-platform permission decision.

This explicitly supersedes the earlier planner-only interpretation.

## Clean source provenance

Only the independently curated root is eligible for Runtime publication:

`734949ba047d33c76fc9fee013b1373404c14a6f`

Reported local qualification:
- 14 allowed source files exported from Git objects with raw-blob equality;
- `INTAKE_MANIFEST.json` binds source blob, SHA256 and size;
- Python 3.14 offline suite: 21 tests PASS;
- Gitleaks v8.24.0: worktree 0 findings;
- Gitleaks v8.24.0: complete independent new history 0 findings.

The previous candidate and inherited history are **not eligible**:

`c091ac3f63ba96b37aba59d3f4184caf4659bff5`

Reason: inherited upstream scan still contains 10 unresolved/unqualified findings. Do not push, graft, merge, import, or make that old history reachable from `Automation_Jovi`.

## Visibility gate

The target repository is currently Public/empty. Local GitHub settings inspection reported secret scanning and push protection enabled in the current state, while the Private conversion confirmation warned that Advanced Security would be disabled.

Therefore:
- source publication waits for Jovi's explicit decision on this specific security-effect tradeoff;
- do not describe Private conversion as security-neutral;
- do not claim Gitleaks CI is fully equivalent to GitHub secret scanning/push protection/Advanced Security.

## Required Git evidence after source publication

Before any Runtime code-review claim:
- repository identity exactly `Jovifei/Automation_Jovi`;
- eligible root SHA exactly `734949ba047d33c76fc9fee013b1373404c14a6f` or an explicitly reviewed descendant created only from the independent root;
- parent/history check proves the disallowed `c091ac3...` lineage is not reachable;
- intake manifest is present and validates all 14 allowed source entries;
- branch/ref and full SHA are recorded;
- no credentials/secrets;
- real-action gates remain false.

## Safety boundary

Remain unchanged:
- `issued_from_human=false`
- `production_integration_allowed=false`
- `real_payment=false`
- `real_customer=false`
- `xianyu=false`
- `auto_delivery=false`
- `n8n_production=false`

No cookies, tokens, browser profiles, payment credentials, real customer PII, or real platform data are accepted.

## Rollback

Rollback means:
- stop accepting the replacement candidate;
- keep Governance history and evidence;
- keep the last accepted Runtime Git ref immutable;
- revert bounded implementation commits or abandon their feature branch/PR;
- never force-push or rewrite history to manufacture acceptance.
