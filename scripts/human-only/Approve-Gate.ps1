[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][ValidatePattern('^GATE_[A-Z0-9]+$')][string]$Gate,
  [Parameter(Mandatory=$true)][ValidateSet('P','I','X','GENERAL')][string]$Track,
  [Parameter(Mandatory=$true)][string]$PlanPath,
  [Parameter(Mandatory=$true)][ValidatePattern('^[a-fA-F0-9]{64}$')][string]$ExpectedSha256,
  [Parameter(Mandatory=$true)][string]$Approver
)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$resolved=(Resolve-Path $PlanPath).Path
$current=(Get-FileHash -Algorithm SHA256 $resolved).Hash.ToLowerInvariant()
if($current -ne $ExpectedSha256.ToLowerInvariant()){throw 'Plan SHA256 mismatch. Do not approve.'}
$plan=Get-Content -Raw -Encoding UTF8 $resolved | ConvertFrom-Json
if($plan.gate -ne $Gate){throw "Plan gate does not match $Gate."}
if(-not $plan.tracks.$Track){throw "Plan does not contain track $Track."}
if($plan.tracks.$Track.status -eq 'BLOCKED'){throw "Track $Track is blocked. Resolve blockers before approval."}
Write-Host "Gate: $Gate"
Write-Host "Track: $Track"
Write-Host "Plan: $resolved"
Write-Host "SHA256: $current"
Write-Host "Actions:"
$plan.tracks.$Track.actions | ForEach-Object { Write-Host " - $_" }
$code=Read-Host "Type the first 16 characters of the SHA256 to approve this track"
if($code.Trim().ToLowerInvariant() -ne $current.Substring(0,16)){throw 'Approval code mismatch.'}
$dir=Join-Path $root 'workspace/approvals'
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$out=Join-Path $dir "$Gate.$Track.approval.json"
if(Test-Path $out){throw 'Approval already exists. Revoke only through a documented rollback.'}
[ordered]@{
  schema_version=2
  gate=$Gate
  track=$Track
  plan_path=$resolved
  plan_sha256=$current
  approver=$Approver
  approved_at=(Get-Date).ToString('o')
} | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 $out
Write-Host "Approval receipt written: $out"
