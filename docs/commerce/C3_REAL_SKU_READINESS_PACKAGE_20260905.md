# Commerce C3 — Real SKU Readiness Package (2026-09-05)

## Purpose

C2 proved the Commerce Runtime with an original synthetic digital product. C3 must prove that the same audited Commerce pipeline can ingest the first **real** product without silently modifying the product repository or inventing commercial claims.

Target product source (local-only):

`E:\project\jovi-modbus-diagnostic-toolkit-v1`

Target Commerce Runtime (local-only):

`E:\project\jovi-medusa-commerce-v1`

## C3 non-negotiable boundary

Commerce is a **consumer and packager** of the product repository. It is not allowed to repair, rebuild, refactor, re-version or otherwise mutate the Modbus product source in C3.

If product qualification fails, return the finding to the product repository and stop C3.

## Required phase flow

1. Recompute C2 audit closure and boundary flags locally.
2. Inspect the Modbus product repository read-only.
3. Freeze `C3_MODBUS_SOURCE_QUALIFICATION.json`.
4. Freeze real `C3_PRODUCT_MANIFEST.json` from evidence only.
5. Freeze `C3_LISTING_CLAIM_EVIDENCE.json`; every commercial claim must have evidence.
6. Create immutable C3 DigitalRelease using existing C2 models.
7. Wrap existing product artifacts into a deterministic DeliveryPackage. Do not rebuild product bytes in Commerce.
8. Generate listing candidate + Xianyu draft candidate only.
9. Execute Real SKU + Synthetic Order + Synthetic Payment C3 E2E.
10. Replay/recovery/negative tests.
11. Freeze `C3_RELEASE_CANDIDATE.json`.
12. Stop at `READY_FOR_C3_INDEPENDENT_AUDIT`.

## Product source qualification must prove

- Git HEAD is recorded.
- Worktree and index are clean.
- No unexplained untracked release artifact exists.
- Version has an authoritative source.
- Deliverable files exist and their byte SHA256/size are recorded.
- Windows build/smoke evidence exists.
- Supported OS claims are evidence-backed.
- License inventory and third-party notices are present or the product is rejected.
- Known limitations/support boundary are explicit.
- Authenticode/signing status is recorded as fact (`SIGNED`, `UNSIGNED`, or `NOT_VERIFIED`); never infer it.
- Windows SmartScreen/reputation is not a guaranteed product feature and must not be promised.

## Listing truth rule

Every title/description/bullet/compatibility/support/delivery claim must map to a `VERIFIED` evidence record. Unsupported claims are omitted, not softened into marketing language.

Examples that are prohibited unless explicitly proven:

- "supports all Modbus devices"
- "100% compatible"
- "all Windows versions"
- "permanent free updates"
- "guaranteed to solve every communication problem"
- "no driver required"

## Release bytes rule

The C3 Commerce release must bind the exact product artifacts found in the product repository. Commerce may create a deterministic wrapper ZIP/manifest, but it may not replace or rebuild the installer/executable/portable ZIP.

The DeliveryPackage manifest must contain the original source artifact SHA256 values.

## OSS reuse rule

Do not change the product packaging stack merely because another project exists.

- If the product already uses PyInstaller, keep its existing pinned recipe/spec and validate it against upstream `pyinstaller/pyinstaller` behavior as needed.
- If the product already uses Inno Setup, keep its existing `.iss` recipe and record compiler/version; upstream reference is `jrsoftware/issrc`.
- Reuse already-adopted Gitleaks and Syft for C3 source/delivery scanning.
- `sigstore/cosign` blob signing/attestation is optional future release hardening and is **not** a C3 pass criterion.

## Success definition

C3 succeeds only when a real Modbus product release can traverse:

`Real Product Source -> Qualified Real Artifact -> C3 Product Manifest -> Immutable DigitalRelease -> Deterministic DeliveryPackage -> Listing Candidate -> Synthetic Order -> Synthetic Payment Evidence -> exactly-one Entitlement -> exactly-one DeliveryReceipt -> DownloadGrant -> loopback download hash verification -> Xianyu Draft Bundle`

Final business state remains `READY_FOR_HUMAN_DELIVERY`.

All real-action flags remain false.

## Stop condition

Implementation agent must stop at:

`READY_FOR_C3_INDEPENDENT_AUDIT`

Only a fresh read-only independent auditor may return:

- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_FAIL`
