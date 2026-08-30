---
name: content-repurposer
description: "Turn one approved technical case or photo workflow into platform-specific content drafts without publishing."
---

# Content Repurposer

## Preconditions

The source case, code, screenshots, photos, and claims must already be approved for public use.

## Workflow

1. Extract one factual outcome, audience problem, evidence, and product boundary.
2. Produce channel-specific drafts rather than identical cross-posts.
3. Keep technical claims, compatibility, source attribution, and limitations consistent.
4. Remove customer identifiers, secrets, private repositories, and unsupported claims.
5. Generate headline alternatives and one call to action allowed by the target platform.
6. Add a fact-check and rights checklist to every content bundle.
7. Place all outputs in `workspace/review-queue/`; never publish.

## Outputs

- Bilibili outline and chapter plan.
- Short-video script and shot list.
- Xiaohongshu post and carousel copy.
- Xianyu listing draft through `xianyu-listing-draft`.
- FAQ, captions, transcript, and thumbnail text.
- `FACT_CHECK.md` and `ASSET_RIGHTS.md`.

## Quality gate

A reviewer must be able to trace every technical claim to the approved source case and every visual/audio asset to a rights record.
