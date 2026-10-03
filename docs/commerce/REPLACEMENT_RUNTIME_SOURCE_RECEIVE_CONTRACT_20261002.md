# Replacement Runtime Source Receive Contract

Updated: 2026-10-03

## Scope

This contract governs source intake into the actual Runtime repository:

`Jovifei/Automation_Jovi`

It does not claim Runtime source review before the eligible baseline is uploaded.

## Only eligible baseline

Independent curated root:

`734949ba047d33c76fc9fee013b1373404c14a6f`

The prepared publication HEAD is `0cdf07ea99b05bb32ca517021357ee03c5ffc3ce`,
a direct descendant of that root. Its independently reviewed documentation-only
fix corrects SOURCE_NOTICE.md and OFFLINE_README.md and adds INTAKE_REVIEW_FIXES.md.
It does not change Runtime/test blobs or rewrite the root/manifest.
The 14-file raw-blob/hash/size comparison is performed at the immutable initial
root, not incorrectly against amended HEAD documentation. Later changes must
be reviewed as explicit diffs from that root; this is not a scan exclusion.

Required source provenance:
- 14 allowed files;
- every allowed file raw-blob matches its selected source Git object;
- `INTAKE_MANIFEST.json` records source blob, SHA256 and size;
- intake metadata (README/AGENTS/source convention/git attributes) is additive and must not be misrepresented as copied historical source;
- Python 3.14 offline tests: at least the reported 21 PASS before upload;
- Gitleaks v8.24.0 worktree scan: 0 findings;
- Gitleaks v8.24.0 full **new-history** scan: 0 findings.

## Explicitly rejected history

Do not upload or connect the old candidate/history:

`c091ac3f63ba96b37aba59d3f4184caf4659bff5`

The inherited two upstream commits still have 10 unresolved/unqualified scan findings.

Reject intake if:
- the old commit becomes reachable;
- an old upstream parent is grafted/merged;
- the independent root unexpectedly has a parent;
- any of the 14 initial-root blobs differs from the frozen intake manifest;
- a subsequent change lacks explicit scoped review and provenance;
- a secret/credential appears;
- any real-platform gate changes.

## Repository visibility gate

Current GitHub fact: `Automation_Jovi` exists, is Public and empty.

Private conversion is pending Jovi's explicit confirmation because the GitHub confirmation UI reported an Advanced Security effect. No source is to be uploaded merely to bypass that decision.

## Remote intake review after upload

Remote ChatGPT must verify directly from GitHub:
1. repository identity and visibility;
2. exact root SHA and parentlessness/new-history provenance;
3. tree/file inventory and intake manifest;
4. absence of disallowed old history;
5. build/test/CI entrypoints;
6. security scans and real-action boundaries.

Only then may status advance to:

`REPLACEMENT_RUNTIME_BASELINE_RECEIVED_READY_FOR_REMOTE_IMPLEMENTATION`

Source upload alone is not an acceptance verdict.

## Post-intake execution

After intake passes:
- Remote ChatGPT creates a Runtime implementation branch and directly commits the bounded CI/build/restore stage.
- Local Codex pulls that exact commit, builds/tests locally, fixes failures, and pushes back.
- Remote ChatGPT re-reviews GitHub and released local evidence.

No planner-only fallback.

## Prohibited

- no real Xianyu writes;
- no real payment enablement;
- no raw customer PII;
- no credentials;
- no auto delivery/refund;
- no n8n production;
- no Governance-source mixing;
- no force push/history rewrite.
