---
name: embedded-license-auditor
description: "Audit source code, SDKs, middleware, fonts, documents and assets for commercial distribution obligations."
---

# Embedded License Auditor

## Scope

Audit every code file or asset not authored solely for this product, including copied snippets, SDKs, HALs, RTOS components, middleware, fonts, icons, photos, example data, documents, model files, and build tools distributed in the package.

## Workflow

1. Build an inventory with name, source URL, exact version/commit, file paths, author/owner, license, modifications, and distribution mode.
2. Read the actual license and notices; do not rely only on badges or repository topics.
3. Determine obligations: attribution, notice retention, source offer, reciprocal licensing, patent terms, trademark limits, model/data restrictions, and commercial restrictions.
4. Distinguish build-time tools from distributed components.
5. Compare obligations with the intended sales and delivery model.
6. Mark each item `ALLOW`, `ALLOW_WITH_NOTICE`, `REVIEW`, or `BLOCK`.
7. Generate notices and source-offer instructions where required.
8. Quarantine unknown or contradictory rights; never resolve ambiguity by assumption.

## Outputs

- `license_inventory.csv`
- `THIRD_PARTY_NOTICES.md`
- `LICENSE_DECISIONS.md`
- source-offer package if applicable
- quarantine list with remediation owner

## Release gate

No `PENDING`, `UNKNOWN`, or `BLOCK` item may enter an approved commercial package.
