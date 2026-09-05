# C2 Cloud Reference Pack

**Status:** `REFERENCE_ORACLE_READY_FOR_LOCAL_RUNTIME_ADOPTION`

This package contains governance-side executable reference assets for Commerce C2. It is intentionally independent of the local Medusa runtime and must not be described as a runtime implementation.

## What is implemented here

1. A completely original synthetic digital product fixture: `Synthetic Commerce Validation Pack`.
2. Exact per-file SHA256 values and a product manifest.
3. A cross-machine deterministic ZIP contract: `C2_DETERMINISTIC_ZIP_V1`.
4. A Python reference builder/oracle and self-tests.
5. A machine-readable C2 contract schema for ProductManifest, DigitalRelease, DeliveryPackage, DownloadGrant, ListingCandidate and XianyuDraftBundle.
6. A 21-case fail-closed negative-test matrix.
7. A C2 independent-audit checklist.
8. A local Codex handoff prompt.

## Deterministic ZIP V1 contract

- ZIP method: `STORE` (no compression).
- Member names: POSIX relative paths only, sorted lexicographically.
- Fixed timestamp: `1980-01-01 00:00:00`.
- Fixed regular-file mode: `0644`.
- No comments, no extra fields, no host path metadata.
- Archive contains `MANIFEST.json` plus the delivery assets.
- `MANIFEST.json` is UTF-8, JSON keys sorted, indent=2, one final LF.
- Runtime TypeScript code is expected to reproduce the test-vector ZIP SHA exactly for this fixture.

## Reference test vector

Expected package SHA256 and file hashes are in `reference/commerce/c2/test-vector.json`.

The runtime may use a different internal implementation, but if it claims `C2_DETERMINISTIC_ZIP_V1` compatibility it must reproduce this vector byte-for-byte.

## OSS relation

The domain separation is inspired by selective review of MIT `makepay-apps/medusa-plugin-digital-downloads` at commit `a5343ba18cee85b3eed674ed55d0de7e32aaa448`, especially its separate digital-download module, private storage abstraction and delivery flow. No upstream source code is copied into this cloud reference implementation. Jovi remains the sole Payment Evidence / Entitlement / DeliveryReceipt authority.

## What still must be done locally

The local Runtime must implement Medusa persistence/workflows, Windows reparse-point protection, database atomicity/idempotency, DownloadGrant issuance and consumption, Admin UI integration, replay/recovery and the full C2 evidence package. The local executor must first independently recompute the R2-R3 audit closure.
