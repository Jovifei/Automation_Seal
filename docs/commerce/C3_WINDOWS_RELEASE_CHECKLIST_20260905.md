# C3 Windows Real-SKU Release Checklist

This checklist is executed against `E:\project\jovi-modbus-diagnostic-toolkit-v1` read-only.

## A. Repository identity

- [ ] `git rev-parse HEAD` captured.
- [ ] tracked worktree has no modifications.
- [ ] index has no staged modifications.
- [ ] every untracked file is either absent or explicitly listed as a qualified generated release artifact with SHA256/size.
- [ ] Commerce has made zero writes to the product repository.

## B. Version identity

- [ ] one authoritative version source is identified.
- [ ] version evidence file SHA256 is frozen.
- [ ] GUI/about/version metadata does not conflict with release version.
- [ ] installer/package filename version does not conflict with release version.

## C. Deliverables

For every customer-facing deliverable:

- [ ] relative path captured using `/` separators.
- [ ] file exists.
- [ ] SHA256 captured.
- [ ] byte size captured.
- [ ] media type/role captured.
- [ ] original bytes are preserved by Commerce.
- [ ] installer/executable signing status recorded factually.

Primary release artifact priority:

1. existing installer, if product already has one and it passes qualification;
2. existing portable ZIP, if documented and tested;
3. existing executable only if that is the intended supported delivery format.

C3 must not invent a new delivery format just to pass the gate.

## D. Windows behavior

- [ ] documented launch/smoke test passes on the local Windows environment.
- [ ] serial-port/Modbus basic flow is testable without making unsupported hardware claims.
- [ ] supported OS claims are backed by actual evidence.
- [ ] required runtime/driver dependencies are documented.
- [ ] administrator privilege requirement, if any, is documented.
- [ ] unsigned installer/executable status, if applicable, is disclosed internally for C4 planning.

## E. Tests

- [ ] canonical unit/integration test command identified.
- [ ] test output persisted to an evidence file.
- [ ] test evidence SHA256 frozen.
- [ ] packaging/build smoke output persisted if applicable.
- [ ] no tests are weakened or skipped merely to qualify the SKU.

## F. License / third-party inventory

- [ ] every distributable third-party package/library is inventoried.
- [ ] version and license recorded.
- [ ] source/project URL recorded when available.
- [ ] required license notices included.
- [ ] `THIRD_PARTY_NOTICES` present, or `NOT_REQUIRED_WITH_EVIDENCE` documented.
- [ ] no dependency is silently omitted because it is bundled by PyInstaller or an installer.

## G. Listing claim evidence

Every listing statement is one of:

- `VERIFIED` with evidence path + SHA256; or
- omitted from listing.

Mandatory evidence-backed categories:

- [ ] supported protocols/functions actually implemented;
- [ ] supported Windows versions;
- [ ] supported connection/interface types;
- [ ] included files/features;
- [ ] software version;
- [ ] update policy;
- [ ] support boundary;
- [ ] known limitations.

Do not publish/prepare unsupported absolute claims such as `all devices`, `100% compatible`, `permanent updates`, or `guaranteed repair`.

## H. Security / distribution facts

- [ ] Gitleaks source scan passes.
- [ ] Syft source/package inventory generated where applicable.
- [ ] no customer secrets or real platform credentials are present.
- [ ] Authenticode status is one of `SIGNED`, `UNSIGNED`, `NOT_VERIFIED`, `NOT_APPLICABLE`.
- [ ] SmartScreen/reputation is not represented as a guarantee.
- [ ] optional Windows Defender/local AV artifact scan recorded before C4 pilot.

## I. Commerce integration

- [ ] C3 Product Manifest references exact qualified artifacts.
- [ ] immutable DigitalRelease created.
- [ ] deterministic DeliveryPackage build A/B byte-equal.
- [ ] DeliveryPackage manifest contains original product-artifact SHA256.
- [ ] listing candidate is `candidate_only=true`.
- [ ] Xianyu draft is `platform_action_allowed=false`.
- [ ] synthetic order/payment only.
- [ ] exactly one Entitlement.
- [ ] exactly one DeliveryReceipt.
- [ ] DownloadGrant works in loopback test.
- [ ] downloaded package SHA equals delivery package SHA.
- [ ] replay/recovery produce one logical result.

## J. Stop gate

If all above pass, freeze evidence and stop:

`READY_FOR_C3_INDEPENDENT_AUDIT`

If the product repository itself fails a product qualification item, do not patch it from Commerce. Stop:

`C3_PRODUCT_NOT_RELEASE_READY`

and produce a minimal product-repository fix request.
