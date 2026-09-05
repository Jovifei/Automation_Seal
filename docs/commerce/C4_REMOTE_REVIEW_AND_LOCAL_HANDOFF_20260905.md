# Jovi Commerce C4 Remote Review & Local Codex Handoff — 2026-09-05

**Review verdict:** `CONTINUE_WITH_CONTROLLED_C4_PREP`

**Explicit non-verdicts:**
- `DO_NOT_REDO_C3`
- `DO_NOT_START_REAL_PILOT_YET`
- `DO_NOT_PUBLISH_C4_DRAFT_AS_IS`
- `DO_NOT_FLIP_REAL_ACTION_FLAGS`

## 1. Executive conclusion

The project should continue in the same high-level direction — C3 is technically closed and the next business milestone is a small C4 Human Pilot — but the old execution report that says “directly publish for 99 CNY and start 5–10 orders” is stale and must not be followed literally.

The correct immediate phase is:

`C4 Pre-Publish QA / Pilot Preparation`

Only after this phase is closed with auditable local evidence may Jovi review and sign the C4 Human Pilot Decision.

## 2. What the previous work did well

### Commerce Runtime / C2-C3 engineering

The earlier work shows strong engineering discipline and should be preserved rather than rebuilt:

- Medusa is already the selected Commerce Core; do not restart commerce-core selection.
- C2 synthetic digital-delivery E2E has independent PASS evidence.
- C3 uses a real Modbus SKU while keeping the product repository read-only.
- Product qualification, deterministic packaging, release/hash binding, replay/recovery and fail-closed negative tests are present.
- C3 reported 40/40 isolated product tests.
- C3 listing evidence contains 12 explicit evidence-bound claims.
- Exactly-one Entitlement / DeliveryReceipt invariants were verified in synthetic C3 execution.
- Product deliverables and delivery package are SHA256-bound.
- Six real commercial flags remained false.
- Recent Governance branch commits already corrected several unsafe C4-draft issues: empty real Pilot ledger, `DO_NOT_PUBLISH_AS_IS`, evidence-bound listing requirement, privacy minimization, corrected CRC/SHA terminology, transparent `0.2.0-dev` / unsigned status.
- `C3 Reference QA` on the reviewed Governance head before this remote-review patch set completed successfully.

These are assets. Do not throw them away by restarting C3 or building a second commerce backend.

## 3. What needed correction

### 3.1 The pasted status report is stale

The report that describes Governance head as `ad0e72d` is no longer current. During this review the active Governance branch had already advanced beyond it and contained newer C4-safety corrections.

Likewise, the report refers to `c4_human_pilot_execution_plan.md`, but the current authoritative Governance branch uses `C4_HUMAN_PILOT_PLAN_V1.md` and `C4_PILOT_OPERATIONAL_KIT_V1.md`.

### 3.2 Exact Runtime Git SHA discrepancy

Current GitHub remote observations:

Repository: `Jovifei/jovi-medusa-commerce-v1`

- `main` -> `63db06e9628331982893929f39b1037077138480`
- `feature/c3-modbus-real-sku-staging` -> `63db06e9628331982893929f39b1037077138480`
- parent -> `5b190edce6a530264560a6822b347255fba014ba`
- tree -> `8829d0029a2ac0400aaecb5c5604cf61c3b2e555`

Existing Governance records contain a different full SHA:

`63db06e9fd2e1cbdf6e7926b48ba72d3fbe06cb1`

They share only the short prefix `63db06e9`.

This is **not** sufficient reason to revoke the C3 functional PASS, but it is a governance-chain defect that must be reconciled before the C4 Human Decision.

See:

`docs/commerce/C3_RUNTIME_REMOTE_RECONCILIATION_20260905.md`

Required local verdict:

`C3_RUNTIME_GIT_RECONCILIATION_PASS`

Never fabricate a 40-character Git SHA by expanding a short prefix.

### 3.3 Old C4 listing / presale assumptions were too aggressive

The current Runtime C3 evidence supports exactly 12 claims. A remote convenience pre-review has now been added:

`docs/commerce/C4_REMOTE_CLAIM_PRE_REVIEW_20260905.json`

Important corrections include:

- do not ask buyers about “Python basics” by default; C3 evidence does not establish Python as an ordinary buyer requirement;
- do not claim source project/QUICKSTART/requirements/com0com/virtual-serial content unless the local final package inventory proves it;
- do not say CRC is hardware error correction;
- do not call a SHA256 hash a digital signature;
- do not promise a fixed “3-minute setup” time;
- do not claim universal compatibility, permanent updates or unlimited support;
- do not use an absolute “digital goods are non-refundable” policy.

The final authoritative `C4_LISTING_CLAIM_REVIEW.json` must still be generated from the local original C3 evidence and recomputed hashes.

### 3.4 Xianyu workflow must be verified in the actual account/UI

Official remote material confirms that Xianyu's developer ecosystem has virtual/no-logistics delivery concepts and refund/dispute flows, but this does not prove that Jovi's ordinary personal-seller flow exposes the same exact option for this SKU.

Therefore do not hard-code “click 无需物流发货” as an assured step before Jovi verifies the actual UI/category/order behavior.

See:

`docs/commerce/C4_XIANYU_RULES_REMOTE_PRECHECK_20260905.md`

Required Human check verdict:

`C4_XIANYU_HUMAN_RULE_CHECK_PASS`

### 3.5 Branch protection remains absent

Remote review observed the Governance active branch and Runtime `main`/C3 feature without branch protection. This is a governance-hardening gap, not a reason to rewrite C2/C3. It should be addressed before/around mainline cleanup where account/plan capabilities allow it.

## 4. Current authoritative direction

```text
C2 Synthetic Commerce E2E
  -> PASS
C3 First Real SKU Staging
  -> PASS
C3 Runtime Promotion
  -> reported PASS; exact Git identity reconciliation required
C4 Pre-Publish QA / Pilot Preparation
  -> CURRENT
C4 Human Pilot Decision
  -> issued_from_human=false
Human Pilot 5–10 orders or fixed time window
  -> NOT STARTED
C4 Audit
  -> FUTURE
C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION
  -> FUTURE
```

## 5. Locked commercial boundaries

Until a later explicit Human Decision changes an individual permission, all remain false:

- `production_integration_allowed=false`
- `real_payment=false`
- `real_customer=false`
- `xianyu=false`
- `auto_delivery=false`
- `n8n_production=false`

C4 Pilot preparation does **not** authorize automatic platform writes.

## 6. Current first-SKU anchors

Reported/audited product:

- product: `Modbus RTU Diagnostic Toolkit`
- version: `0.2.0-dev`
- product HEAD: `25ef15386b21bcc53277c0d5af5973ad8ea272eb`
- installer: `JoviModbusDiagnosticToolkit-0.2.0-dev-unsigned.exe`
- installer SHA256: `d86ccc3136bc2ed201622c5f961738e9e81762e74e71ac5772ea6d4b5a408e02`
- portable ZIP SHA256: `7525e4c8d4fd55900d46c51e075b92e47d61c7d8e1393383e2e92206855a9628`
- deterministic Commerce package: `SYNTH-C3-MODBUS-RTU-0.2.0-dev.zip`
- delivery package SHA256: `4bd5703ae80fcea9c1dcf7d5d1ea2a02fe282a5cf6ef3f04a2c9703db5188e59`
- delivery package size: `82,853,839` bytes

These are reported anchors. C4 must use locally recomputed values, not simply copy them from this handoff.

## 7. Exact next actions for local Codex

### Step 0 — Receive current Governance branch

In `E:\project\jovi-automation`:

- fetch `origin`;
- checkout/update `commerce-c3-real-sku-readiness-20260905`;
- confirm no local unpublished work is overwritten;
- read this handoff and the three new pre-publish review records before making changes.

### Step 1 — Reconcile Runtime exact Git identity

In `E:\project\jovi-medusa-commerce-v1`, collect raw Git output and close:

`C3_RUNTIME_GIT_RECONCILIATION_PASS`

Do not force-push and do not rewrite history simply to match old documentation.

### Step 2 — Recompute C3 source/product/package anchors

Recompute from local files:

- Runtime HEAD / tree / lockfile hash;
- Product HEAD;
- installer SHA/size/signing status;
- portable ZIP SHA/size;
- deterministic delivery package SHA/size;
- C3 listing-evidence file SHA;
- required C3 sidecars/evidence integrity.

Product repository remains strict read-only; run any tests from isolated export/clone/sandbox if needed.

### Step 3 — Generate final C4 claim review

Read the local original:

`E:\project\jovi-medusa-commerce-v1\governance\c3\C3_LISTING_CLAIM_EVIDENCE.json`

Generate:

`governance/c4/C4_LISTING_CLAIM_REVIEW.json`

Every customer-visible technical claim must contain:

- final `claim_text`;
- `source_c3_claim_id`;
- `evidence_path`;
- recomputed `evidence_sha256`;
- `decision = KEEP | REWRITE | REMOVE`;
- reason.

No evidence -> REMOVE.

### Step 4 — Inventory the actual customer-facing package

Inspect the exact package bytes/file list. Produce a local package inventory so listing copy does not advertise files that are absent.

Do not mutate the product repository.

### Step 5 — Human Xianyu rule/category/fulfillment check

Jovi, not an automation agent, checks the live Xianyu account/UI for:

- exact allowed category;
- digital/virtual notices or qualifications;
- fees/deposit if any;
- fulfillment options actually shown;
- current refund/dispute wording;
- final listing acceptance.

No Cookie/Token/Profile automation.

### Step 6 — Jovi selects release posture

Only Jovi chooses:

- `BETA_PILOT`: continue with `0.2.0-dev` + unsigned, transparently disclosed; or
- `STABLE_FIRST`: stop C4, independently harden/release/sign the product, then perform necessary delta qualification/audit before resuming C4.

An agent must not infer this decision from earlier conversation text.

### Step 7 — Freeze manual delivery transport

Define one human-controlled transport for Pilot and record:

- canonical customer-facing filename/alias;
- authoritative underlying package SHA256;
- alias -> audited package mapping;
- access/revocation/expiry procedure where applicable;
- no payment/customer credential leakage.

### Step 8 — Produce C4 Pre-Publish readiness record

Generate:

`governance/c4/C4_PRE_PUBLISH_READINESS.json`

Required final state for agent work:

`C4_PRE_PUBLISH_QA_READY_FOR_HUMAN_DECISION`

This is **not** C4 authorization.

### Step 9 — Governance CI / PR #5 closure preparation

- update Governance branch with sanitized audit mirrors/records only;
- keep Runtime/product authority in their own repositories;
- run/observe Governance QA;
- ensure PR #5 reflects current exact facts;
- do not merge if reconciliation or required Pre-Publish evidence is unresolved.

### Step 10 — Stop at the Human Gate

Present the final Candidate to Jovi.

Do not change:

`issued_from_human=false`

to true on Jovi's behalf.

Do not publish a listing, accept payment, message a real buyer, deliver a real package, issue refunds or start counting Pilot orders before Jovi signs.

## 8. If Jovi chooses BETA_PILOT

Only after the Human Decision is signed:

- first price may remain `99.00 CNY` if Jovi chooses it; it is a hypothesis, not a validated market price;
- first scope may remain 5–10 orders or a fixed time window;
- all real platform actions remain manual;
- every real order starts from a zero-entry ledger and gets its own traceable package SHA / Entitlement / Receipt chain;
- measure human minutes/order, inquiries, non-purchase reasons, support categories, refunds/disputes and wrong-version/duplicate counts.

The commercial purpose is to learn whether real users pay and how expensive/manual each sale is — not to maximize automation during the first Pilot.

## 9. If Jovi chooses STABLE_FIRST

Stop C4 cleanly. The product repository becomes the sole authority for stable/signing work. Commerce must not directly mutate it.

After the product creates a new stable/signature-qualified release:

- re-qualify changed product/release artifacts;
- recompute SHA bindings;
- perform a scoped Commerce delta audit;
- regenerate C4 listing evidence and Decision Candidate.

Do not silently substitute a stable build for the already-audited C3 package.

## 10. Remote-review files added in this patch set

- `docs/commerce/C3_RUNTIME_REMOTE_RECONCILIATION_20260905.md`
- `docs/commerce/C4_REMOTE_CLAIM_PRE_REVIEW_20260905.json`
- `docs/commerce/C4_XIANYU_RULES_REMOTE_PRECHECK_20260905.md`
- this handoff
- a dedicated local-Codex receive/verify prompt under `prompts/commerce/`

## 11. Final assessment

The previous agent's **engineering direction is accepted**. Its old “start selling now” execution summary is **not accepted** as the current runbook.

Continue by closing C4 Pre-Publish QA. Do not rebuild C3, do not start a new commerce backend, and do not automate Xianyu/payment/delivery. Once the local evidence chain is reconciled and the Pilot package is clean, stop and ask Jovi for the explicit Human Pilot decision.
