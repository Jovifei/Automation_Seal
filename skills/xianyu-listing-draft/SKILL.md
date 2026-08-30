---
name: xianyu-listing-draft
description: "Create lawful Xianyu listing and fixed reply candidates with explicit compatibility, exclusions and human confirmation."
---

# Xianyu Listing Draft

## Inputs

- Approved product manifest.
- Rights status and evidence.
- Compatibility and exclusions.
- Support policy and test evidence.

## Workflow

1. Describe the user problem and concrete deliverable, not resource quantity hype.
2. State version, supported environment, compatibility, prerequisites, and excluded cases.
3. Add buyer notice, refund/dispute handling boundaries, and purchase-before-contact requirement where appropriate.
4. Draft fixed FAQ/reply candidates for support scope and required diagnostic information.
5. Flag any price, schedule, success, refund, safety, or legal commitment for human handling.
6. Ensure no off-platform contact, piracy, shared accounts, unauthorized courses/software, or misleading guarantee.
7. Output draft files only; never publish or send.

## Outputs

- `listing_draft.md`
- fixed reply candidates with `auto_send=false`
- compatibility/exclusion table
- escalation rules
- fact/right/source checklist

## Gate

Only `ORIGINAL` or `VERIFIED_LICENSE` products can proceed to a human-approved manual-import candidate.
