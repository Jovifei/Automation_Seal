# Remaining Path to First Real Commerce Pilot — C3 to C4 (2026-09-05)

## Current position

Reported and governance-mirrored state:

- R6 Medusa controlled adoption: PASS
- R2-R3 Admin/session hardening: PASS
- C2 synthetic digital Commerce E2E: `C2_INDEPENDENT_AUDIT_PASS`
- C2 deterministic delivery / replay / recovery / negative / Admin / security: closed locally

The next stage is C3 real-SKU staging, not more Commerce-framework research.

## What is still missing before a usable product pilot

### 1. Real product qualification — C3

The Modbus product repository must prove:

- exact source HEAD;
- clean tracked/index state;
- explainable generated release artifacts;
- authoritative version;
- real installer/portable artifact hashes;
- Windows test evidence;
- supported-platform evidence;
- license and third-party notices;
- known limitations/support boundary;
- no Commerce writes to the product repository.

### 2. Real-SKU Commerce E2E — C3

Replace the C2 synthetic product fixture with the qualified Modbus release while keeping customer/order/payment synthetic.

Must prove:

- immutable release;
- deterministic delivery wrapper;
- original artifact SHA binding;
- evidence-backed listing;
- exactly-once entitlement/receipt;
- download grant/hash verification;
- replay/recovery;
- 25+ real-SKU negative cases;
- no platform action.

### 3. Independent C3 audit

A fresh read-only agent must issue either:

- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_FAIL`

No self-audit.

### 4. Runtime authoritative-main promotion

Today the Runtime `main` remains the controlled-import baseline while the audited improvements live on descendant feature branches.

Before C4:

- Jovi signs `JOVI_RUNTIME_C3_PROMOTION_DECISION_V1`;
- exact audited C3 closure becomes Runtime authoritative main/release line without source edits;
- fresh Post-Promotion Audit proves byte/hash equivalence and six flags false.

Required state:

`C3_RUNTIME_PROMOTION_AUDIT_PASS`

### 5. Runtime remote / CI

Recommended Runtime remote:

`Jovifei/jovi-medusa-commerce-v1`

After explicit authorization and local push:

- preserve audited history;
- protect main / PR-only;
- prevent force push/deletion;
- enable stable typecheck/unit/integration/security/provenance checks;
- no automatic production deployment.

This step is repository/productization hygiene, not permission to transact.

### 6. Pilot distribution readiness

Before first real user:

- exact release package/version frozen;
- listing candidate human-reviewed;
- installer/executable Authenticode status known;
- unsigned status, if any, understood for Windows user experience;
- optional local AV/Defender artifact scan recorded;
- onboarding/readme/support instructions reviewed;
- refund/support boundary reviewed;
- rollback package available.

Code signing may improve distribution trust but is not allowed to silently block C3. If required commercially, handle it as a product-distribution work item before or during C4 preparation.

### 7. C4 Human Pilot Decision

C4 still requires an explicit Jovi decision.

The initial pilot keeps all platform/payment/refund actions human-controlled.

Runtime stores only minimized/pseudonymous pilot references by default; `real_customer=false` can remain while no raw customer profile/PII is persisted.

### 8. 5–10 order pilot

Verify:

- listing clarity;
- inquiry→order behavior;
- human payment confirmation;
- package preparation;
- exact version delivery;
- support burden;
- duplicate/wrong-version/unauthorized-action count;
- privacy/redaction handling;
- refunds/disputes.

Target state:

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`

## What is NOT necessary before the first pilot

Do not delay the pilot for:

- another Commerce framework comparison;
- Storefront launch;
- automatic Xianyu publishing/messaging;
- n8n production;
- S3 migration;
- automatic refunds;
- full CRM/customer profile;
- SLSA/cosign rollout;
- large-scale multi-channel architecture;
- advanced analytics dashboard.

These are later optimizations only if the pilot proves commercial value.

## Product-landed definition for V1

For the first V1, "landed" means:

1. a real Modbus SKU is qualified and hash-bound;
2. C3 staging independent audit passes;
3. audited Runtime bytes are promoted to the authoritative release line;
4. first human-controlled real orders use the same release/entitlement/delivery pipeline;
5. 0 wrong-version delivery;
6. 0 duplicate entitlement/receipt;
7. 0 unauthorized platform action;
8. every delivery can be traced back to exact product source/release SHA;
9. support/refund/privacy boundaries are usable by Jovi;
10. Jovi has enough pilot evidence to decide the next permission to automate.
