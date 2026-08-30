---
name: xianyu-draft-bundle-builder
description: "Build and validate immutable Xianyu manual-import candidate bundles without any platform write action."
---

# Xianyu Draft Bundle Builder

## Preconditions

- Stage is X2 or later with required gate receipt.
- Product rights are `ORIGINAL` or `VERIFIED_LICENSE`.
- Inputs contain no real customer data.

## Workflow

1. Use `deploy/xianyu/xianyu_bundle.schema.json`.
2. Generate `bundle.json`, listing draft, fixed/draft reply rules, empty or stage-allowed delivery catalog, rights evidence, and test report.
3. Force all external actions to false and approval status to PENDING.
4. Generate `manifest.sha256.json` covering every candidate file.
5. Generate `package.sha256.txt` from the manifest file.
6. Validate schema, semantics, listed-file hashes, sizes, unsafe paths, and unlisted files.
7. Run negative tests for publish/message/delivery flags, unresolved rights, path traversal, embedded approval, and tampering.
8. Place package in the review queue and stop.

## Stage constraints

- X2: synthetic data only; delivery catalog must be empty.
- X3: fixed reply candidates only; no auto-send.
- X4: exactly one approved SKU; still manual import and user enablement.

Codex never runs `Approve-XianyuBundle.ps1`.
