---
name: llm-reply-evaluator
description: "Evaluate AI reply drafts on synthetic Xianyu conversations for promises, privacy, policy, escalation and prompt-injection failures."
---

# LLM Reply Evaluator

## Data rule

Use synthetic messages only. Never export real buyer messages, order data, account identifiers, Cookies, or system secrets into an evaluation dataset.

## Test categories

- Price, delivery-time, success-rate, warranty, and refund commitments.
- Off-platform contact or payment requests.
- Pirated course, cracked software, shared account, and unauthorized asset requests.
- Complaint, dispute, refund, harassment, and legal escalation.
- High-risk electrical, battery, medical, legal, or safety topics.
- Prompt injection, secret extraction, role confusion, and context leakage.
- Account acting as buyer rather than seller.
- Unsupported product/MCU/toolchain questions.

## Workflow

1. Define an explicit policy rubric and expected action for every case.
2. Build reproducible Promptfoo configuration pinned to a reviewed version.
3. Compare fixed templates and candidate models separately.
4. Use deterministic assertions for forbidden phrases/actions and human escalation.
5. Record false positives, false negatives, latency, cost, and model/version.
6. Require 100% pass on prohibited-action cases before X3.
7. Even after passing, keep real auto-send disabled unless the user creates a later explicit policy decision.

## Outputs

- Synthetic dataset.
- Promptfoo config.
- Machine-readable results.
- Failure analysis and revised policy.
- X3 readiness decision.
