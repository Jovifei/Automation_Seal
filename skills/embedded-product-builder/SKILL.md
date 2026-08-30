---
name: embedded-product-builder
description: "Build testable embedded digital products with host-side tests, documentation, compatibility and release evidence."
---

# Embedded Product Builder

## Inputs

- Approved specification and tasks.
- Target chip/board/toolchain when board-specific work is required.
- Third-party dependency inventory.
- Supported and unsupported use cases.

## Workflow

1. Start with host-testable pure modules: parser, CRC, state machine, timeout, ring buffer, image header, or protocol logic.
2. Establish repository structure, formatting, compiler warnings, reproducible commands, and test fixtures.
3. Write tests before or with implementation, including normal, boundary, malformed, timeout, duplicate, and recovery cases.
4. Run static analysis and multiple compiler configurations where practical.
5. Only after hardware facts are confirmed, add board/HAL integration in an isolated adapter layer.
6. Record real hardware tests separately from simulated/host tests; never claim hardware validation without evidence.
7. Produce compatibility matrix, troubleshooting tree, configuration reference, and known limitations.
8. Run license and secret audits before packaging.

## Required deliverables

- Source and examples.
- Automated tests and test vectors.
- Build scripts and exact tool versions.
- `BUILD_REPORT.md` and `TEST_RESULTS.md`.
- Compatibility matrix.
- Quick start and troubleshooting.
- `THIRD_PARTY_NOTICES.md` and license inventory.
- Review-queue release candidate.

## Safety boundaries

Do not include employer/customer code, unsafe high-voltage claims, unverified charging/power designs, credentials, proprietary SDK files without redistribution rights, or generated code that has not been compiled/tested.
