[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$ArtifactPath,
  [Parameter(Mandatory=$true)][ValidatePattern('^[A-Za-z0-9._-]+$')][string]$JobId,
  [string]$Title='Review item'
)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$source=(Resolve-Path $ArtifactPath).Path
if((Get-Item $source).PSIsContainer){throw 'ArtifactPath must be a single immutable file.'}
$job=Join-Path $root "workspace/review-queue/$JobId"
if(Test-Path $job){throw "Review job exists: $job"}
New-Item -ItemType Directory -Force -Path $job | Out-Null
$artifact=Join-Path $job (Split-Path $source -Leaf)
Copy-Item -Force $source $artifact
$hash=(Get-FileHash -Algorithm SHA256 $artifact).Hash.ToLowerInvariant()
[ordered]@{schema_version=1;job_id=$JobId;title=$Title;artifact=(Split-Path $artifact -Leaf);sha256=$hash;created_at=(Get-Date).ToString('o');status='awaiting_human_review';external_actions_allowed=$false} | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $job 'manifest.json')
@"
# Human review required

Job: $JobId
Title: $Title
Artifact: $(Split-Path $artifact -Leaf)
SHA256: $hash
Approval code: $($hash.Substring(0,12))

Review content, tests, rights, privacy, secrets and external-action risks. Agents must not approve.
"@ | Set-Content -Encoding UTF8 (Join-Path $job 'REVIEW_REQUIRED.md')
Write-Host "Review item created: $job"
