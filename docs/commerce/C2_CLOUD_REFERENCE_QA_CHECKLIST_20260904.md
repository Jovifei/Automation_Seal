# C2 Cloud Reference QA Checklist

This checklist validates only the governance-side reference pack. It does **not** replace the local Runtime C2 independent audit.

## A. Source boundary

- [ ] Work from `Jovifei/Automation_Seal` branch `commerce-c2-cloud-reference-20260904`.
- [ ] Record the actual remote HEAD before use.
- [ ] Confirm the reference pack adds no Approval/Decision/control-plane permission expansion.
- [ ] Confirm no real payment, customer, Xianyu, automatic delivery or production action is executed.

## B. Fixture binding

Run SHA256 over:

- `reference/commerce/c2/fixture/README.txt` -> `23ce668014753df1ba1b4d6b13d31666e805d42d5fdd285872db8401f6909df2`
- `reference/commerce/c2/fixture/checklist.json` -> `962d1634316ba7a11272bfe895f94aef36cd2b389d7d12255e95225207e2ceb8`
- `reference/commerce/c2/fixture/sample-report.html` -> `9d1519db237c9b0be238db22a92814e02693c96f6c35353ed79d584cd63a046e`
- `reference/commerce/c2/fixture/product-manifest.json` -> `71d638c59255b6a6520ecda3c36dccd77a44e42b0dc126e4514b09b0619ffade`

Any mismatch is a hard FAIL.

## C. Zero-dependency executable verification

Run from repository root:

```powershell
python scripts/commerce/c2_verify_cloud_reference.py
```

Required lines:

- `C2_REFERENCE_TESTS_PASS`
- `C2_DOWNLOAD_GRANT_POLICY_TESTS_PASS`
- final JSON contains `"verdict": "C2_CLOUD_REFERENCE_PASS"`
- final JSON contains package SHA `d13f5d95cc9e46bfa8a871e5a8542552a38964db1ff7fdd68cfedb83ab6623ca`

## D. Deterministic package contract

Independently build twice with `c2_reference_builder.py` and prove:

- bytes A == bytes B;
- SHA A == SHA B == test vector;
- member order is exactly `MANIFEST.json`, `README.txt`, `checklist.json`, `sample-report.html`;
- method is STORE;
- timestamp is fixed to 1980-01-01 00:00:00;
- file mode is normalized to 0644;
- no ZIP comments or extra fields.

## E. Negative behavior

The cloud Oracle must independently reject at least:

- `../escape`;
- `C:/escape`;
- UNC absolute path;
- backslash path syntax;
- asset byte tampering.

The local Runtime remains responsible for Windows junction/reparse-point checks and every case in `negative-test-matrix.json`.

## F. DownloadGrant separation

Verify the reference policy rejects:

- wrong token;
- wrong order;
- expired grant;
- revoked grant;
- revoked Entitlement.

A grant is a temporary access capability only. It must never mint ownership.

## G. OSS provenance

The cloud reference code is original and does not copy upstream plugin source. The design review references MIT `makepay-apps/medusa-plugin-digital-downloads` commit `a5343ba18cee85b3eed674ed55d0de7e32aaa448`. If the local Runtime copies/adapts any upstream source, it must create `THIRD_PARTY_NOTICES.md` with exact source paths and modifications.

## H. Local handoff gate

Only after A-G PASS may the local Runtime executor use the reference pack. Local Runtime success still requires the full C2 plan, database/replay/recovery/Playwright checks and a separate independent audit.
