---
name: skill-router
description: "Route Jovi Automation tasks to the narrowest matching project skill and enforce the current phase gate."
---

# Skill Router

## Use when

Use this skill at the beginning of any task that spans research, product development, licensing, content, release, AI evaluation, or Xianyu integration.

## Inputs

- User request and expected deliverable.
- Current stage in `STATUS.md`.
- Applicable gate receipt under `workspace/approvals/`.
- Related PRD or source document.

## Workflow

1. Read `AGENTS.md`, `CODEX_MASTER_TASK.md`, `STATUS.md`, and the relevant acceptance rows.
2. Identify whether the task is read-only, internal-write, human-only, or external-platform action.
3. Refuse to route external publish, message, delivery, price, refund, payment, captcha, or risk-control actions.
4. Choose one primary skill and no more than two supporting skills.
5. Verify every required gate before the first write command.
6. Record selected skills, reason, allowed roots, evidence path, and stop condition in the stage report.

## Routing map

- Market or competitor question → `market-opportunity-research`.
- Literature/document-heavy research → `research-evidence-builder`.
- PRD conversion → `prd-to-spec-kit`.
- Embedded implementation → `embedded-product-builder` plus `embedded-license-auditor`.
- Photography product → `photo-product-builder`.
- Content variants → `content-repurposer`.
- Release candidate → `product-package-release`.
- Third-party Skill → `skill-security-auditor`.
- Xianyu X0/X1 → `xianyu-integration-auditor`.
- Xianyu draft package → `xianyu-draft-bundle-builder` plus `xianyu-listing-draft`.
- AI reply evaluation → `llm-reply-evaluator`.

## Output

A short routing record containing phase, primary skill, supporting skills, permissions, evidence destination, unresolved inputs, and exact stop condition.
