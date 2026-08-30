# Smoke tests

## Package

```powershell
python .\scripts\validate-package.py
python .\scripts\run-static-tests.py
```

## Read-only audit

```powershell
.\scripts\00-run-readonly-audit.ps1 -XianyuRepoPath E:\project\xianyu-auto-reply
```

Verify the Xianyu Git working tree did not change.

## Gate tamper test

1. Approve a copied test plan.
2. Modify the plan by one byte.
3. `verify-gate-approval.py` must fail.

## Core

```powershell
.\scripts\bootstrap.ps1
.\scripts\start-core.ps1
.\scripts\healthcheck.ps1
.\scripts\backup.ps1 -SecretBackupPath "你的加密备份目录"
.\scripts\test-backup-restore.ps1 -BackupDirectory "刚生成的备份目录"
```

## Xianyu synthetic contract

```powershell
.\scripts\xianyu\Test-XianyuDraftContract.ps1
```

No real platform action is permitted during smoke tests.
