# C3 OSS / Windows Release Acceleration (2026-09-05)

## Goal

Reuse mature tooling where it shortens C3, without changing a working product packaging stack merely to adopt newer tooling.

## Upstream references checked

### PyInstaller

- Repo: `pyinstaller/pyinstaller`
- Reference branch: `develop`
- Reference head observed during C3 planning: `5a80d1b93f1fbad3d8c0bdce90ce01f49927a9a1`
- Use in C3: **reference only unless the Modbus product already uses PyInstaller**.

If the product already uses PyInstaller:

1. record the actual installed/pinned version;
2. record the `.spec`/build recipe hash;
3. retain the existing product build recipe;
4. do not upgrade PyInstaller inside Commerce staging;
5. if the existing recipe is broken, return the issue to the product repository.

### Inno Setup

- Repo: `jrsoftware/issrc`
- Reference branch: `main`
- Reference head observed during C3 planning: `1ae7bf81dc0d2013235dfe4bb0b6f4e4a0b6b25c`
- Use in C3: **reference only unless the Modbus product already uses Inno Setup**.

If the product already uses Inno Setup:

1. record the actual compiler version;
2. bind the `.iss` recipe SHA256;
3. preserve the existing installer bytes;
4. do not upgrade the compiler from the Commerce repository;
5. record Authenticode status separately from installer build success.

## Existing security tooling to reuse

Reuse the tools already adopted by the Commerce Runtime:

- Gitleaks: source/secret scan;
- Syft: source and artifact/SBOM inventory;
- existing Jovi SHA/sidecar validators.

Do not add a second overlapping dependency/license system in C3 unless a concrete gap is found.

## Optional later hardening

`sigstore/cosign` can later sign/attest release blobs or provenance after the Runtime has its own GitHub remote and the release process is defined. It is **not** a C3 acceptance criterion and must not block the first real-SKU staging.

Windows Authenticode code signing is a separate product-distribution concern and requires a suitable signing certificate. C3 records actual signed/unsigned status; it does not fabricate or bypass Windows trust signals.

## Windows release evidence to capture

For each primary deliverable record:

- exact filename;
- SHA256;
- byte size;
- file version/product version when available;
- build recipe and tool versions;
- Authenticode status (`SIGNED`, `UNSIGNED`, `NOT_VERIFIED`, or `NOT_APPLICABLE`);
- local Windows smoke-test result;
- supported Windows versions only when evidence exists;
- optional local antivirus scan evidence before C4 pilot.

## Rule: Commerce never rebuilds the SKU

C3 consumes qualified release bytes. It may wrap them into the audited deterministic C2 DeliveryPackage, but may not modify executable/installer/portable ZIP bytes.

If release bytes do not exist or fail qualification, stop with `C3_PRODUCT_NOT_RELEASE_READY` and return a minimal fix request to `jovi-modbus-diagnostic-toolkit-v1`.
