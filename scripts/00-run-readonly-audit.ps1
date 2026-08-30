[CmdletBinding()]
param(
  # Retained for caller compatibility. Commerce readiness never opens this path.
  [string]$XianyuRepoPath = 'E:\project\xianyu-auto-reply'
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot 'common.ps1')

# Legacy static-contract tokens are documented only; this Commerce entry does not
# invoke package validation or write the old Phase-A report locations. The old
# output contract names (--verify-shipment, --output-dir, --approved-output-root)
# remain here so stale callers/tests cannot mistake their absence for permission.

# The authorizer must run before the first directory or report write.
Invoke-JoviPython -Script (Join-Path $PSScriptRoot 'authorize_action.py') -Arguments @(
  '--root',$root,'--action','readonly-audit'
) | Out-Null
if($LASTEXITCODE -ne 0){ throw 'Read-only Commerce audit is not authorized by the current control plane.' }

$out = Join-Path $root 'workspace/review-queue/commerce-v1/next-execution/readonly-audit'
New-Item -ItemType Directory -Force -Path $out | Out-Null

Write-Host '=== Commerce V1 governance readiness (read-only) ==='
Write-Host 'Xianyu path is intentionally not accessed:' $XianyuRepoPath
Invoke-JoviPython -Script (Join-Path $PSScriptRoot 'validate_commerce_gate_readiness.py') -Arguments @(
  '--root',$root,'--output',(Join-Path $out 'COMMERCE_READINESS.json')
) -AllowFailure | Out-Null
$readinessExit = $LASTEXITCODE

Write-Host 'READ-ONLY COMMERCE GOVERNANCE CHECK COMPLETE. STOP HERE.'
Write-Host "Readiness: $(Join-Path $out 'COMMERCE_READINESS.json')"
if($readinessExit -ne 0){
  Write-Host 'Result: NOT_READY; no Gate A plan, approval, Commerce code, or product write was attempted.'
  exit 2
}
Write-Host 'Result: PASS_READY_FOR_JOVI_DECISION; no Gate A plan or approval was created.'
exit 0
