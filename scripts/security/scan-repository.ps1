[CmdletBinding()]
param([string]$TargetPath='.')
$ErrorActionPreference='Continue'
$failed=0
if(Get-Command gitleaks -ErrorAction SilentlyContinue){
  gitleaks dir --redact=100 --report-format json --report-path gitleaks-report.json $TargetPath
  if($LASTEXITCODE -ne 0){$failed++}
}else{Write-Warning 'gitleaks not installed; secret scan skipped';$failed++}
if(Get-Command trivy -ErrorAction SilentlyContinue){
  trivy fs --scanners vuln,secret,misconfig --format json --output trivy-report.json $TargetPath
  if($LASTEXITCODE -ne 0){$failed++}
}else{Write-Warning 'trivy not installed; filesystem scan skipped';$failed++}
if($failed){exit 2}
