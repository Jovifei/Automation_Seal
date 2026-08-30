[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][ValidatePattern('^[A-Za-z0-9._-]+$')][string]$JobId,
  [Parameter(Mandatory=$true)][string]$Approver,
  [string]$ApprovalCode
)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$job=Join-Path $root "workspace/review-queue/$JobId"
$m=Get-Content (Join-Path $job 'manifest.json') -Raw | ConvertFrom-Json
$artifact=Join-Path $job $m.artifact
$current=(Get-FileHash -Algorithm SHA256 $artifact).Hash.ToLowerInvariant()
if($current -ne $m.sha256){throw 'Artifact changed after queue creation.'}
$expected=$current.Substring(0,12)
if(-not $ApprovalCode){$ApprovalCode=Read-Host 'Type approval code'}
if($ApprovalCode.Trim().ToLowerInvariant() -ne $expected){throw 'Approval code mismatch.'}
$dest=Join-Path $root "workspace/approved/$JobId"
if(Test-Path $dest){throw 'Approved destination exists; releases are immutable.'}
[ordered]@{job_id=$JobId;decision='approved';approver=$Approver;approved_at=(Get-Date).ToString('o');sha256=$current} | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 (Join-Path $job 'approval.json')
Copy-Item -Recurse $job $dest
Write-Host "Approved copy: $dest"
