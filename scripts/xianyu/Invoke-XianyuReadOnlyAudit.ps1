[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$LocalRepoPath
)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
. (Join-Path $root 'scripts/common.ps1')
$out=Join-Path $root 'reports/xianyu/x0'
New-Item -ItemType Directory -Force -Path $out | Out-Null
Invoke-JoviPython -Script (Join-Path $PSScriptRoot 'xianyu_readonly_audit.py') -Arguments @('--repo',$LocalRepoPath,'--output-dir',$out) | Out-Null
Write-Host "Xianyu X0 report: $out"
exit 0
