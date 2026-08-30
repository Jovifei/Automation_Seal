---
name: xianyu-integration-auditor
description: "Audit the existing local Xianyu automation repository using redacted read-only evidence and produce a staged hardening plan."
---

# Xianyu Integration Auditor

## Fixed target

Default local path: `E:\project\xianyu-auto-reply`.

## X0 permissions

Allowed: repository existence, Git branch/HEAD/status, file names/sizes/hashes, Compose risk flags, container name/status/ports, health status, and bounded OpenAPI path/method inventory for a proven Xianyu container port.

Forbidden: SQLite table contents, Cookie values, buyer messages, card inventory, passwords, tokens, API keys, browser-profile contents, write endpoints, container lifecycle changes, and platform verification endpoints.

## Workflow

1. Run `Invoke-XianyuReadOnlyAudit.ps1` only.
2. Capture before/after Git status and file hashes proving no mutation.
3. Compare local commit/config structure with `deploy/xianyu/upstream.snapshot.json`.
4. Report loopback exposure, defaults, root execution, whole-repo mounts, automatic features, update behavior, and verification automation as booleans without secret values.
5. Produce an X1 hardening proposal only under `reports/xianyu/x1/`.
6. Create a gate plan and stop; never copy proposal files into the Xianyu repository.

## Outputs

- Redacted `audit.json` and `audit.md`.
- Local/upstream delta report.
- X1 hardening plan with SHA256.
- Rollback prerequisites and user decisions.

Any inability to prove read-only behavior blocks the integration.
