# Medusa Adoption Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the R1–R4 adoption blockers without adding storefront, real providers, platform actions, or production authorization.

**Architecture:** Keep Medusa as the commerce core, but make one Jovi policy command the only business path that can persist entitlement and delivery receipt. Persist synthetic provenance on every Jovi record, use a stable run identifier for replay, and freeze source/dependency/test evidence before independent review.

**Tech Stack:** Medusa v2.19.0, TypeScript, Jest, MikroORM/PostgreSQL 16, pnpm 10.32.0, Node 22 LTS target.

## Global Constraints

- All runtime and source changes stay below `E:\Claude_allow\Download\jovi-medusa-v2-spike`.
- Evidence is written only below `workspace/review-queue/commerce-v1/medusa-v2-spike-remediation/`.
- No Storefront, Stripe, email, webhook, external download, Xianyu, real customer data, remote, Hook, R12 apply, or production repository.
- `environment` is exactly `SYNTHETIC_X2`; `synthetic_only=true`; `real_commerce_pilot_started=false`.
- Tests precede every behavior change and must be observed RED before implementation.

---

### Task 1: Persist provenance and make unsafe values unrepresentable

**Files:**
- Modify: `src/modules/jovi-commerce/domain.ts`
- Modify: `src/modules/jovi-commerce/models/jovi-asset.ts`
- Modify: `src/modules/jovi-commerce/models/jovi-entitlement.ts`
- Modify: `src/modules/jovi-commerce/models/jovi-delivery-receipt.ts`
- Test: `src/modules/jovi-commerce/__tests__/domain.unit.spec.ts`

**Interfaces:**
- Produces: `SyntheticProvenance`, provenance-bearing asset/entitlement/receipt and a receipt whose `auto_send` is always false.

- [ ] Add failing tests for missing/invalid environment, run id, fixture SHA and pilot flag.
- [ ] Run domain Jest and confirm failures are caused by absent provenance validation.
- [ ] Add the minimal provenance types, validators and model fields.
- [ ] Run domain Jest and TypeScript until green.
- [ ] Generate and apply a new Jovi module migration.

### Task 2: Replace direct business CRUD with one policy command

**Files:**
- Modify: `src/modules/jovi-commerce/service.ts`
- Create: `src/modules/jovi-commerce/policy-command.ts`
- Replace: `src/modules/jovi-commerce/__tests__/service.spec.ts`

**Interfaces:**
- Consumes: verified payment state, validated asset, terms SHA and provenance.
- Produces: `confirmPaymentAndPrepareDelivery(input)` returning one idempotent entitlement/receipt pair.

- [ ] Write integration tests proving unpaid requests create zero records, valid requests create all records, replay returns the same records, conflicting evidence fails, and `auto_send=true` cannot be persisted.
- [ ] Run integration Jest and observe the intended RED failures.
- [ ] Implement the smallest policy command and service wrapper; keep raw generated CRUD internal to the service.
- [ ] Run integration Jest and TypeScript until green.

### Task 3: Make the synthetic X2 runner replay-safe

**Files:**
- Modify: `src/scripts/jovi-x2.ts`
- Create: `src/modules/jovi-commerce/__tests__/x2-contract.unit.spec.ts`

**Interfaces:**
- Produces: output containing `synthetic_only`, `environment`, `test_run_id`, `source_fixture_sha256`, `real_commerce_pilot_started=false`, and `payment_mode=synthetic_programmatic_mark_paid`.

- [ ] Write failing output-contract and deterministic-run tests.
- [ ] Run the targeted tests and confirm RED.
- [ ] Derive a stable run id from the fixture SHA, reuse matching records, reject conflicts, and call only the policy command.
- [ ] Run the targeted tests and full Jovi suite until green.
- [ ] Execute X2 twice and prove the second execution returns the same logical order/entitlement/receipt without new partial state.

### Task 4: Freeze reproducible evidence

**Files:**
- Create below `workspace/review-queue/commerce-v1/medusa-v2-spike-remediation/`: source manifest, environment, commands, test results, replay results, oracle comparison, license/SBOM summary, independent-audit package manifest, and JSON SHA sidecars.

**Interfaces:**
- Produces: an immutable review package for the separate read-only audit conversation.

- [ ] Verify Node 22 LTS is locally available; if unavailable, record `BLOCKED_NODE22_LTS` and do not claim R4 PASS.
- [ ] Destroy and recreate only the named spike PostgreSQL container/data after validating the exact paths.
- [ ] Re-run migrations, tests, typecheck, Backend/Admin health, loopback inspection and two-pass X2 replay.
- [ ] Hash every relevant source file, `pnpm-lock.yaml`, package metadata and evidence JSON.
- [ ] Generate the final package manifest and run a sensitive-content scan.
- [ ] Set each R1–R4 gate literally PASS or FAIL; do not issue a human Decision.

### Task 5: Freeze handoff for independent audit

**Files:**
- Update: `docs/commerce/MEDUSA_ADOPTION_FRAMEWORK.md`
- Create: `workspace/review-queue/commerce-v1/medusa-v2-spike-remediation/INDEPENDENT_AUDIT_HANDOFF.md`

- [ ] Verify every framework claim against the frozen evidence.
- [ ] Copy the existing independent-audit prompt into the handoff by reference, not by altering its safety boundaries.
- [ ] Update Obsidian progress/decisions/workflow through checkpoint DryRun and no-argument wrapper.
- [ ] Mirror changed Markdown through mirror DryRun and no-argument wrapper.
- [ ] Stop for a new independent audit conversation; do not self-issue adoption PASS.

