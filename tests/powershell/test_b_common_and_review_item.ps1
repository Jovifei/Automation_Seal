[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$passed = 0
$failed = 0
$results = New-Object System.Collections.Generic.List[object]

function Invoke-RevisionTest {
  param(
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][scriptblock]$Body
  )

  try {
    & $Body
    $script:passed++
    $script:results.Add([pscustomobject]@{ Name = $Name; Result = 'PASS'; Detail = '' })
  } catch {
    $script:failed++
    $script:results.Add([pscustomobject]@{ Name = $Name; Result = 'FAIL'; Detail = $_.Exception.Message })
  }
}

function Assert-True {
  param(
    [Parameter(Mandatory = $true)][bool]$Condition,
    [Parameter(Mandatory = $true)][string]$Message
  )

  if (-not $Condition) {
    throw $Message
  }
}

function Assert-Parser {
  param([Parameter(Mandatory = $true)][string]$Path)

  $tokens = $null
  $parseErrors = $null
  [System.Management.Automation.Language.Parser]::ParseFile($Path, [ref]$tokens, [ref]$parseErrors) | Out-Null
  if (@($parseErrors).Count -ne 0) {
    throw (($parseErrors | ForEach-Object { $_.Message }) -join '; ')
  }
}

function New-CmdShim {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string[]]$Lines
  )

  [System.IO.File]::WriteAllText($Path, (($Lines -join "`r`n") + "`r`n"), [System.Text.Encoding]::ASCII)
  return $Path
}

function New-CmdCandidate {
  param([Parameter(Mandatory = $true)][string]$ShimPath)

  return [pscustomobject]@{ FileName = $env:ComSpec; Prefix = @('/d', '/c', $ShimPath) }
}

$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
$commonPath = Join-Path $root 'scripts\common.ps1'
$reviewItemPath = Join-Path $root 'scripts\new-review-item.ps1'
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('jovi-b-revision-v2-test-' + [Guid]::NewGuid().ToString('N'))
$cleanupVerified = $false

try {
  Invoke-RevisionTest 'common_ps1_parser' { Assert-Parser -Path $commonPath }
  Invoke-RevisionTest 'new_review_item_ps1_parser' { Assert-Parser -Path $reviewItemPath }
  Invoke-RevisionTest 'b_revision_test_script_parser' { Assert-Parser -Path $PSCommandPath }

  New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
  $shimDirectory = Join-Path $tempRoot 'shim'
  New-Item -ItemType Directory -Force -Path $shimDirectory | Out-Null
  $badPyShim = New-CmdShim -Path (Join-Path $shimDirectory 'bad-py.cmd') -Lines @('@echo off', 'echo requested Python version is unavailable 1>&2', 'exit /b 23')
  $unparseableShim = New-CmdShim -Path (Join-Path $shimDirectory 'unparseable-python.cmd') -Lines @('@echo off', 'echo version output is malformed', 'exit /b 0')
  $lowVersionShim = New-CmdShim -Path (Join-Path $shimDirectory 'low-python.cmd') -Lines @('@echo off', 'echo Python 3.10.9', 'exit /b 0')
  $goodShim = New-CmdShim -Path (Join-Path $shimDirectory 'good-python.cmd') -Lines @('@echo off', 'echo Python 3.14.2', 'exit /b 0')
  $executionShim = New-CmdShim -Path (Join-Path $shimDirectory 'execution-python.cmd') -Lines @('@echo off', 'if /I "%~1"=="--version" (', '  echo Python 3.14.2', '  exit /b 0', ')', 'echo synthetic script failure 1>&2', 'exit /b 37')
  $syntheticTarget = Join-Path $tempRoot 'synthetic target.py'
  [System.IO.File]::WriteAllText($syntheticTarget, 'raise SystemExit(37)', [System.Text.Encoding]::UTF8)

  . $commonPath

  Invoke-RevisionTest 'missing_candidate_continues_to_good_python' {
    $missing = [pscustomobject]@{ FileName = (Join-Path $tempRoot 'missing python.exe'); Prefix = @() }
    $selected = Get-JoviPython -Candidates @($missing, (New-CmdCandidate -ShimPath $goodShim))
    Assert-True -Condition ($selected.Prefix[-1] -eq $goodShim) -Message 'A missing candidate prevented fallback to the good interpreter.'
  }
  Invoke-RevisionTest 'py_unavailable_version_continues_to_python' {
    $selected = Get-JoviPython -Candidates @((New-CmdCandidate -ShimPath $badPyShim), (New-CmdCandidate -ShimPath $goodShim))
    Assert-True -Condition ($selected.Prefix[-1] -eq $goodShim) -Message 'An unavailable py candidate prevented fallback to python.'
  }
  Invoke-RevisionTest 'actual_machine_selects_python_311_or_newer' {
    $selected = Get-JoviPython
    Assert-True -Condition (([version]$selected.Version) -ge ([version]'3.11')) -Message 'The selected machine interpreter is below Python 3.11.'
  }
  Invoke-RevisionTest 'stderr_nonzero_candidate_continues' {
    $selected = Get-JoviPython -Candidates @((New-CmdCandidate -ShimPath $badPyShim), (New-CmdCandidate -ShimPath $goodShim))
    Assert-True -Condition ($selected.Prefix[-1] -eq $goodShim) -Message 'stderr plus a nonzero candidate did not fall back.'
  }
  Invoke-RevisionTest 'unparseable_version_candidate_continues' {
    $selected = Get-JoviPython -Candidates @((New-CmdCandidate -ShimPath $unparseableShim), (New-CmdCandidate -ShimPath $goodShim))
    Assert-True -Condition ($selected.Prefix[-1] -eq $goodShim) -Message 'Unparseable version output did not fall back.'
  }
  Invoke-RevisionTest 'low_version_candidate_continues' {
    $selected = Get-JoviPython -Candidates @((New-CmdCandidate -ShimPath $lowVersionShim), (New-CmdCandidate -ShimPath $goodShim))
    Assert-True -Condition ($selected.Prefix[-1] -eq $goodShim) -Message 'A Python version below 3.11 did not fall back.'
  }
  Invoke-RevisionTest 'verified_good_candidate_selected' {
    $selected = Get-JoviPython -Candidates @((New-CmdCandidate -ShimPath $goodShim))
    Assert-True -Condition (($selected.Version -eq '3.14.2') -and ($selected.Prefix[-1] -eq $goodShim)) -Message 'The verified good candidate was not selected.'
  }
  Invoke-RevisionTest 'all_candidates_fail_stable_message' {
    $message = $null
    try {
      $null = Get-JoviPython -Candidates @((New-CmdCandidate -ShimPath $badPyShim), (New-CmdCandidate -ShimPath $unparseableShim), (New-CmdCandidate -ShimPath $lowVersionShim))
    } catch {
      $message = $_.Exception.Message
    }
    Assert-True -Condition ($message -eq 'Python 3.11+ is required. See FIRST_RUN_TROUBLESHOOTING.md.') -Message 'All-candidate failure did not return the stable sanitized message.'
  }
  Invoke-RevisionTest 'discovery_restores_error_action_preference' {
    $previousPreference = $ErrorActionPreference
    try {
      $ErrorActionPreference = 'Stop'
      $null = Get-JoviPython -Candidates @((New-CmdCandidate -ShimPath $badPyShim), (New-CmdCandidate -ShimPath $goodShim))
      Assert-True -Condition ($ErrorActionPreference -eq 'Stop') -Message 'Get-JoviPython changed ErrorActionPreference.'
    } finally {
      $ErrorActionPreference = $previousPreference
    }
  }
  Invoke-RevisionTest 'discovery_preserves_last_exitcode' {
    $previousCode = $global:LASTEXITCODE
    try {
      $global:LASTEXITCODE = 4242
      $null = Get-JoviPython -Candidates @((New-CmdCandidate -ShimPath $badPyShim), (New-CmdCandidate -ShimPath $goodShim))
      Assert-True -Condition ($global:LASTEXITCODE -eq 4242) -Message 'Get-JoviPython changed LASTEXITCODE.'
    } finally {
      $global:LASTEXITCODE = $previousCode
    }
  }

  function Get-JoviPython {
    return [ordered]@{ Exe = $env:ComSpec; Prefix = @('/d', '/c', $executionShim); Version = '3.14.2' }
  }

  Invoke-RevisionTest 'invoke_jovi_python_nonzero_throws_with_code_and_script' {
    $message = $null
    try {
      $null = Invoke-JoviPython -Script $syntheticTarget
    } catch {
      $message = $_.Exception.Message
    }
    Assert-True -Condition (($message -match 'exit code 37') -and ($message -match [regex]::Escape($syntheticTarget))) -Message 'The nonzero invocation error omitted its exit code or script path.'
  }
  Invoke-RevisionTest 'invoke_jovi_python_allow_failure_returns_real_exit_code' {
    $code = Invoke-JoviPython -Script $syntheticTarget -AllowFailure
    Assert-True -Condition ($code -eq 37) -Message 'AllowFailure did not return exit code 37.'
  }
  Invoke-RevisionTest 'invoke_jovi_python_sets_last_exitcode' {
    $null = Invoke-JoviPython -Script $syntheticTarget -AllowFailure
    Assert-True -Condition ($global:LASTEXITCODE -eq 37) -Message 'Invoke-JoviPython did not retain the target exit code.'
  }

  $fixtureRoot = Join-Path $tempRoot 'fixture root with spaces'
  $fixtureScripts = Join-Path $fixtureRoot 'scripts'
  New-Item -ItemType Directory -Force -Path $fixtureScripts | Out-Null
  $fixtureReviewScript = Join-Path $fixtureScripts 'new-review-item.ps1'
  Copy-Item -LiteralPath $reviewItemPath -Destination $fixtureReviewScript -Force
  $sourceArtifact = Join-Path $tempRoot 'sample artifact.txt'
  [System.IO.File]::WriteAllText($sourceArtifact, 'synthetic review artifact', [System.Text.Encoding]::UTF8)
  $jobId = 'B-REVISION-V2-TEST'
  $title = 'Synthetic isolated review'
  & $fixtureReviewScript -JobId $jobId -Title $title -ArtifactPath $sourceArtifact
  $jobDirectory = Join-Path (Join-Path $fixtureRoot 'workspace\review-queue') $jobId
  $manifestPath = Join-Path $jobDirectory 'manifest.json'
  $reviewPath = Join-Path $jobDirectory 'REVIEW_REQUIRED.md'

  Invoke-RevisionTest 'new_review_item_generates_valid_isolated_manifest' {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    $artifactPath = Join-Path $jobDirectory $manifest.artifact
    Assert-True -Condition (($manifest.job_id -eq $jobId) -and ($manifest.title -eq $title) -and ($manifest.artifact -eq 'sample artifact.txt') -and ($manifest.sha256 -match '^[0-9a-f]{64}$') -and (Test-Path -LiteralPath $artifactPath)) -Message 'The isolated manifest is invalid or incomplete.'
  }
  Invoke-RevisionTest 'review_required_contains_required_fields' {
    $review = Get-Content -LiteralPath $reviewPath -Raw
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    $approvalCode = $manifest.sha256.Substring(0, 12)
    Assert-True -Condition (($review -match [regex]::Escape("Job: $jobId")) -and ($review -match [regex]::Escape("Title: $title")) -and ($review -match [regex]::Escape('Artifact: sample artifact.txt')) -and ($review -match [regex]::Escape("SHA256: $($manifest.sha256)")) -and ($review -match [regex]::Escape("Approval code: $approvalCode"))) -Message 'REVIEW_REQUIRED.md omitted required review data.'
  }
  Invoke-RevisionTest 'new_review_item_fixture_does_not_target_real_workspace' {
    Assert-True -Condition ((Split-Path -Parent $jobDirectory) -like ($fixtureRoot + '*')) -Message 'The review-item fixture escaped its temporary workspace.'
  }
  Invoke-RevisionTest 'b_targets_have_no_external_or_prohibited_execution_reference' {
    $externalAdapterName = 'xianyu' + '-auto-reply'
    $targetText = (Get-Content -LiteralPath $commonPath -Raw) + (Get-Content -LiteralPath $reviewItemPath -Raw)
    Assert-True -Condition (($targetText -notmatch [regex]::Escape($externalAdapterName)) -and ($targetText -notmatch 'Invoke-WebRequest|docker|wsl|human-only')) -Message 'A Batch B target references a prohibited external action.'
  }
} finally {
  if (Test-Path -LiteralPath $tempRoot) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
  }
  $cleanupVerified = -not (Test-Path -LiteralPath $tempRoot)
}

Invoke-RevisionTest 'temporary_shims_scripts_and_directory_are_cleaned' {
  Assert-True -Condition $cleanupVerified -Message 'The temporary test directory was not removed.'
}

foreach ($result in $results) {
  Write-Host ('{0} {1} {2}' -f $result.Result, $result.Name, $result.Detail)
}
Write-Host ('Summary: {0} passed; {1} failed; 0 skipped.' -f $passed, $failed)
if ($failed -ne 0) {
  exit 1
}
