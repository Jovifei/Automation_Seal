---
name: product-package-release
description: "Create immutable, tested, license-complete product release candidates and human review jobs."
---

# Product Package Release

## Preconditions

- Specification tasks are complete or explicitly deferred.
- P0 tests pass.
- License inventory has no unresolved item.
- Product support and compatibility boundaries are documented.

## Workflow

1. Build from a clean working tree or recorded source snapshot.
2. Run tests, static analysis, secret scanning, and package-specific validation.
3. Remove caches, logs, raw secrets, personal metadata, and unrelated files.
4. Generate changelog, SBOM/dependency inventory, notices, build report, test report, and rollback notes.
5. Create an immutable archive with versioned filename.
6. Record every file size and SHA256 in a manifest.
7. Create a review item with `scripts/new-review-item.ps1` or an equivalent non-approval path.
8. Stop. Never call human-only approval, publishing, messaging, or delivery tools.

## Outputs

- Versioned candidate archive.
- SHA256 manifest.
- Build/test/license/security reports.
- Review checklist.
- Review-queue job.

Any post-manifest change creates a new candidate version and invalidates prior approval.
