[CmdletBinding()]
param()
$ErrorActionPreference='Continue'
. (Join-Path $PSScriptRoot 'common.ps1')
$root=Split-Path -Parent $PSScriptRoot
$out=Join-Path $root 'reports/phase-a/upstream-versions.json'
try {
  $code=Invoke-JoviPython -Script (Join-Path $PSScriptRoot 'research/resolve_versions.py') -Arguments @('--output',$out) -AllowFailure
  if($code -ne 0){ throw "exit code $code" }
  Write-Host "Version refresh report: $out"
} catch {
  Write-Warning "Narrow version refresh failed: $($_.Exception.Message). Frozen sources remain available; current facts are NOT_VERIFIED."
}
exit 0
