[CmdletBinding()]
param([string]$LocalRepoPath='E:\project\xianyu-auto-reply')
$ErrorActionPreference='Stop'
$root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$audit=Join-Path $root 'reports/xianyu/x0/audit.json'
if(-not (Test-Path $audit)){throw 'Run X0 audit first.'}
$out=Join-Path $root 'reports/xianyu/x1'
New-Item -ItemType Directory -Force -Path $out | Out-Null
python (Join-Path $PSScriptRoot 'generate_xianyu_hardening_plan.py') --repo $LocalRepoPath --audit $audit --out $out
if($LASTEXITCODE -ne 0){throw 'Hardening plan generation failed.'}
Write-Host 'Proposal created only in Jovi reports. No Xianyu file was changed.'
