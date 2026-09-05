# C3 Real SKU Staging — Independent Audit Prompt Template

You are a fresh **C3 Real SKU Staging Independent Auditor**.

You did not implement C3 and must remain read-only.

Target Runtime:

`E:\project\jovi-medusa-commerce-v1`

Target product source:

`E:\project\jovi-modbus-diagnostic-toolkit-v1`

Your final verdict may only be:

- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_FAIL`

Do not fix findings yourself.

## 1. Recompute predecessors

Independently verify original evidence for:

- R6 Post-Import PASS;
- R2-R3 independent PASS;
- C2 independent PASS;
- all required SHA/sidecars;
- six real-action flags false.

A governance mirror is not enough; read Runtime evidence.

## 2. Verify C3 implementation boundary

Confirm C3 Runtime feature branch was derived from the audited C2 closure and that no unrelated/unreviewed business changes are hidden between the C2 audit closure and C3 base.

Confirm Runtime `main` was not silently changed during C3 implementation.

## 3. Product source qualification

Read `C3_MODBUS_SOURCE_QUALIFICATION.json` and independently recompute:

- product Git HEAD;
- tracked diff state;
- staged/index state;
- exact untracked file set;
- exact qualified release artifact SHA256/size;
- authoritative version evidence;
- canonical test evidence;
- supported Windows evidence;
- license inventory;
- third-party notices;
- known limitations/support boundary;
- Authenticode status.

Run the cloud verifier independently:

`python scripts/commerce/c3_verify_real_sku_readiness.py ...`

Do not accept a claim because the implementation report says it passed.

## 4. Product repository zero-write proof

Independently verify:

`C3_PRODUCT_SOURCE_ZERO_WRITE_PROOF.json`

Run:

`python scripts/commerce/c3_verify_product_zero_write.py ...`

Confirm:

- before HEAD == after HEAD == qualified HEAD;
- tracked/index clean before and after;
- exact qualified untracked artifact set unchanged;
- artifact SHA/size unchanged;
- product_repo_write_attempts=0;
- verdict `PASS_ZERO_WRITE`.

If the implementation Agent ran tests/builds directly in the real product repo and then cleaned/reset the repo, FAIL: the zero-write history was violated.

## 5. Listing claim evidence

For every final listing title/description/bullet/compatibility/support/update statement:

- locate its claim ID;
- independently read the evidence file;
- recompute evidence SHA;
- decide whether the evidence actually supports the wording.

Unsupported marketing claims must cause FAIL or be removed before the audit candidate is frozen.

Specifically inspect for absolute/unproven claims such as:

- all Modbus devices;
- 100% compatibility;
- all Windows versions;
- permanent updates;
- guaranteed repair;
- no driver required.

## 6. Real source artifact preservation

Independently hash original Modbus release artifacts in the product repository and compare with:

- source qualification;
- C3 Product Manifest;
- DigitalRelease / DeliveryAsset;
- DeliveryPackage manifest;
- C3 Release Candidate.

Commerce may wrap but may not rebuild/modify the original product artifact bytes.

## 7. C3 E2E

Freshly execute/recompute the full staging flow:

Real SKU
→ Synthetic Order
→ Synthetic Payment Evidence
→ Jovi Entitlement
→ DeliveryPackage
→ DeliveryReceipt
→ DownloadGrant
→ loopback download/hash verification
→ Xianyu Draft Bundle

Require:

- final state `READY_FOR_HUMAN_DELIVERY`;
- exactly one Entitlement;
- exactly one DeliveryReceipt;
- original artifact SHA bound into package manifest;
- downloaded package SHA == delivery package SHA;
- listing/draft candidate only;
- no platform action.

## 8. Determinism / replay / recovery

Rebuild the same C3 wrapper twice and prove byte equality.

Replay the same synthetic order/payment and verify one logical result.

Execute required restart/recovery evidence and verify no duplicate release/package/entitlement/receipt.

## 9. Negative suite

Independently execute/review every case in:

`reference/commerce/c3/c3-negative-test-matrix.json`

Require at least all 25 cases and fail-closed no-partial-state semantics.

Pay special attention to:

- dirty product source;
- untracked release artifact drift;
- artifact SHA tamper;
- Commerce rebuild attempt;
- missing license/notices;
- unsupported compatibility claim;
- false Authenticode claim;
- SmartScreen guarantee claim;
- wrong product/version;
- platform/real flags injection.

## 10. Admin / security / supply chain

Re-run or independently validate:

- Admin Playwright cookie-session paths;
- C2 regressions;
- Gitleaks;
- Syft;
- sidecar integrity;
- source manifests;
- six boundary flags false.

## 11. Release candidate binding

Read `C3_RELEASE_CANDIDATE.json` and independently recompute every bound SHA.

It must bind:

- source qualification;
- zero-write proof;
- product manifest;
- listing claim evidence;
- source artifacts;
- delivery package;
- listing candidate;
- Xianyu draft;
- synthetic order/payment;
- exactly-once results;
- download verification;
- replay/recovery;
- six flags false.

## 12. Stop

If PASS, generate the independent result + SHA sidecar and stop at:

`C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`

Do **not** promote Runtime main, create a production deployment, run a real Xianyu action, or start C4.

The next action after PASS is a separate Jovi human Runtime promotion decision.
