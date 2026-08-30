[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $PSScriptRoot
$ReportDirectory = Join-Path $Root 'reports\security'
$BootstrapTemplate = Join-Path $Root 'tests\hooks\pre_tool_bootstrap.ps1'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$Results = @()

function Add-Result {
  param([string]$Name, [bool]$Passed, [string]$Detail)
  $script:Results += [pscustomobject]@{ name = $Name; passed = $Passed; detail = $Detail }
  Write-Output ("[{0}] {1}: {2}" -f $(if ($Passed) { 'PASS' } else { 'FAIL' }), $Name, $Detail)
}

function Write-Utf8File {
  param([string]$Path, [string]$Text)
  $parent = Split-Path -Parent $Path
  [System.IO.Directory]::CreateDirectory($parent) | Out-Null
  [System.IO.File]::WriteAllText($Path, $Text, $script:Utf8NoBom)
}

function Invoke-CapturedProcess {
  param(
    [string]$FileName,
    [string]$Arguments,
    [string]$WorkingDirectory,
    [string]$InputText
  )
  $startInfo = New-Object System.Diagnostics.ProcessStartInfo
  $startInfo.FileName = $FileName
  $startInfo.Arguments = $Arguments
  $startInfo.WorkingDirectory = $WorkingDirectory
  $startInfo.UseShellExecute = $false
  $startInfo.CreateNoWindow = $true
  $startInfo.RedirectStandardInput = $true
  $startInfo.RedirectStandardOutput = $true
  $startInfo.RedirectStandardError = $true
  $process = New-Object System.Diagnostics.Process
  $process.StartInfo = $startInfo
  if (-not $process.Start()) { throw 'Process did not start.' }
  $stdoutTask = $process.StandardOutput.ReadToEndAsync()
  $stderrTask = $process.StandardError.ReadToEndAsync()
  $inputBytes = $script:Utf8NoBom.GetBytes($InputText)
  $process.StandardInput.BaseStream.Write($inputBytes, 0, $inputBytes.Length)
  $process.StandardInput.Close()
  $timedOut = -not $process.WaitForExit(15000)
  if ($timedOut) {
    $process.Kill()
    $process.WaitForExit()
  }
  return [pscustomobject]@{ exit_code = $process.ExitCode; stdout = $stdoutTask.Result; stderr = $stderrTask.Result }
}

function Test-DenyJson {
  param([string]$Text)
  try {
    $items = @($Text | ConvertFrom-Json -ErrorAction Stop)
    return $items.Count -eq 1 -and
      $items[0].hookSpecificOutput.hookEventName -eq 'PreToolUse' -and
      $items[0].hookSpecificOutput.permissionDecision -eq 'deny' -and
      -not [string]::IsNullOrWhiteSpace([string]$items[0].hookSpecificOutput.permissionDecisionReason)
  } catch {
    return $false
  }
}

function Get-Sha256Text {
  param([string]$Text)
  $bytes = $script:Utf8NoBom.GetBytes($Text)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  try { return ([System.BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant() }
  finally { $sha.Dispose() }
}

function New-RootFixture {
  param([string]$Base, [string]$Name, [ValidateSet('actual', 'stdin', 'deny', 'throw', 'stderr2', 'duplicate')][string]$Mode)
  $fixture = Join-Path $Base $Name
  $codeDir = Join-Path $fixture 'scripts\codex'
  [System.IO.Directory]::CreateDirectory($codeDir) | Out-Null
  Write-Utf8File (Join-Path $fixture 'AGENTS.md') '# synthetic fixture'
  Write-Utf8File (Join-Path $fixture 'PROJECT_STATE.json') '{}'
  Copy-Item -LiteralPath (Join-Path $Root 'scripts\codex\Invoke-PreToolGuard.ps1') -Destination (Join-Path $codeDir 'Invoke-PreToolGuard.ps1')
  if ($Mode -eq 'actual') {
    Copy-Item -LiteralPath (Join-Path $Root 'scripts\codex\pre_tool_guard.py') -Destination (Join-Path $codeDir 'pre_tool_guard.py')
  } elseif ($Mode -eq 'stdin') {
    $stub = @'
import hashlib
import pathlib
import sys
raw = sys.stdin.buffer.read()
expected = pathlib.Path(__file__).with_name("expected.sha256").read_text(encoding="utf-8").strip()
if hashlib.sha256(raw).hexdigest() != expected:
    print('{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"stdin mismatch"}}')
'@
    Write-Utf8File (Join-Path $codeDir 'pre_tool_guard.py') $stub
  } elseif ($Mode -eq 'deny') {
    $denyStub = @'
print('{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"synthetic deny"}}')
'@
    Write-Utf8File (Join-Path $codeDir 'pre_tool_guard.py') $denyStub
  } elseif ($Mode -eq 'throw') {
    Write-Utf8File (Join-Path $codeDir 'Invoke-PreToolGuard.ps1') "throw 'synthetic wrapper exception'"
  } elseif ($Mode -eq 'stderr2') {
    Write-Utf8File (Join-Path $codeDir 'Invoke-PreToolGuard.ps1') "[Console]::Error.WriteLine('JOVI_HOOK_WRAPPER_DENY'); exit 2"
  } elseif ($Mode -eq 'duplicate') {
    $duplicateStub = @'
Write-Output '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"first"}}'
Write-Output '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"second"}}'
exit 0
'@
    Write-Utf8File (Join-Path $codeDir 'Invoke-PreToolGuard.ps1') $duplicateStub
  }
  return $fixture
}

function Get-CommandWindowsCandidate {
  $body = Get-Content -LiteralPath $BootstrapTemplate -Raw -Encoding utf8
  $escapedBody = $body.Replace('"', '\"')
  return 'powershell -NoProfile -Command "& { ' + $escapedBody + ' }"'
}

function Invoke-Bootstrap {
  param([string]$WorkingDirectory, [string]$InputText)
  $commandWindows = Get-CommandWindowsCandidate
  $hostPath = Join-Path $PSHOME 'powershell.exe'
  if (-not (Test-Path -LiteralPath $hostPath -PathType Leaf)) { $hostPath = 'powershell.exe' }
  $arguments = $commandWindows.Substring('powershell '.Length)
  return Invoke-CapturedProcess -FileName $hostPath -Arguments $arguments -WorkingDirectory $WorkingDirectory -InputText $InputText
}

function Invoke-Wrapper {
  param([string]$Wrapper, [string]$ProjectRoot, [string]$InputText, [string[]]$Candidates = @())
  $hostPath = Join-Path $PSHOME 'powershell.exe'
  if (-not (Test-Path -LiteralPath $hostPath -PathType Leaf)) { $hostPath = 'powershell.exe' }
  $candidateArgs = if ($Candidates.Count) { ' -PythonCandidates ' + (($Candidates | ForEach-Object { '"' + $_ + '"' }) -join ' ') } else { '' }
  return Invoke-CapturedProcess -FileName $hostPath -Arguments ('-NoProfile -File "' + $Wrapper + '" -ProjectRoot "' + $ProjectRoot + '"' + $candidateArgs) -WorkingDirectory $ProjectRoot -InputText $InputText
}

$controlFiles = @('.codex\hooks.json', 'scripts\codex\Invoke-PreToolGuard.ps1', 'scripts\codex\pre_tool_guard.py') | ForEach-Object { Join-Path $Root $_ }
$before = @{}
foreach ($file in $controlFiles) { $before[$file] = (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash }
$tempBase = Join-Path ([System.IO.Path]::GetTempPath()) ('jovi-h0-hook-' + [Guid]::NewGuid().ToString('N'))
[System.IO.Directory]::CreateDirectory($tempBase) | Out-Null

try {
  $hooksPath = Join-Path $Root '.codex\hooks.json'
  $hooks = $null
  $preToolUse = $null
  $hookHandler = $null
  $configuredCommandWindows = ''
  $testedCommandWindows = Get-CommandWindowsCandidate
  try {
    $hooks = Get-Content -LiteralPath $hooksPath -Raw -Encoding utf8 | ConvertFrom-Json -ErrorAction Stop
    $preToolUse = @($hooks.hooks.PreToolUse)[0]
    $hookHandler = @($preToolUse.hooks)[0]
    if ($null -eq $hookHandler) { throw 'PreToolUse handler is missing.' }
    Add-Result 'hooks_json_is_valid' $true 'hooks.json parsed and contains a PreToolUse handler.'
  } catch {
    Add-Result 'hooks_json_is_valid' $false 'hooks.json did not parse or lacks a PreToolUse handler.'
  }
  if ($null -ne $hookHandler) {
    $handlerFields = @($hookHandler.PSObject.Properties.Name)
    $preToolUseFields = @($preToolUse.PSObject.Properties.Name)
    $hasCurrentWindowsField = $handlerFields -contains 'commandWindows'
    $hasLegacyWindowsField = $handlerFields -contains 'command_windows'
    $configuredCommandWindows = if ($hasCurrentWindowsField) { [string]$hookHandler.commandWindows } else { '' }
    $configuredCommand = if ($handlerFields -contains 'command') { [string]$hookHandler.command } else { '' }
    $configuredMatcher = if ($preToolUseFields -contains 'matcher') { [string]$preToolUse.matcher } else { '' }
    $configuredTimeout = if ($handlerFields -contains 'timeout') { [int]$hookHandler.timeout } else { -1 }
    $configuredStatusMessage = if ($handlerFields -contains 'statusMessage') { [string]$hookHandler.statusMessage } else { '' }
    $configuredType = if ($handlerFields -contains 'type') { [string]$hookHandler.type } else { '' }
    Add-Result 'hooks_json_commandWindows_present' $hasCurrentWindowsField 'approved Windows field exists.'
    Add-Result 'hooks_json_command_windows_absent' (-not $hasLegacyWindowsField) 'legacy Windows field is absent.'
    Add-Result 'hooks_json_non_windows_command_unchanged' ($configuredCommand -eq 'python3 scripts/codex/pre_tool_guard.py') 'non-Windows command is unchanged.'
    Add-Result 'hooks_json_matcher_unchanged' ($configuredMatcher -eq '.*') 'matcher is unchanged.'
    Add-Result 'hooks_json_timeout_unchanged' ($configuredTimeout -eq 12) 'timeout is unchanged.'
    Add-Result 'hooks_json_status_message_unchanged' ($configuredStatusMessage -eq 'checking Jovi stage and safety rules') 'statusMessage is unchanged.'
    Add-Result 'hooks_json_type_unchanged' ($configuredType -eq 'command') 'type is unchanged.'
    Add-Result 'hooks_json_commandWindows_matches_real_fixture' ($configuredCommandWindows -eq $testedCommandWindows) 'configured commandWindows equals the real Windows fixture command.'
  } else {
    Add-Result 'hooks_json_commandWindows_present' $false 'not evaluated because hooks.json is invalid.'
    Add-Result 'hooks_json_command_windows_absent' $false 'not evaluated because hooks.json is invalid.'
    Add-Result 'hooks_json_non_windows_command_unchanged' $false 'not evaluated because hooks.json is invalid.'
    Add-Result 'hooks_json_matcher_unchanged' $false 'not evaluated because hooks.json is invalid.'
    Add-Result 'hooks_json_timeout_unchanged' $false 'not evaluated because hooks.json is invalid.'
    Add-Result 'hooks_json_status_message_unchanged' $false 'not evaluated because hooks.json is invalid.'
    Add-Result 'hooks_json_type_unchanged' $false 'not evaluated because hooks.json is invalid.'
    Add-Result 'hooks_json_commandWindows_matches_real_fixture' $false 'not evaluated because hooks.json is invalid.'
  }

  $fixture = New-RootFixture -Base $tempBase -Name 'Hook Root With Spaces' -Mode actual
  $nested2 = Join-Path $fixture 'level one\level two'
  $nested3 = Join-Path $nested2 'level three'
  [System.IO.Directory]::CreateDirectory($nested3) | Out-Null
  $payload = @{ hook_event_name = 'PreToolUse'; cwd = $nested3; tool_name = 'Bash'; tool_input = @{ command = 'Get-Content README_FIRST.md' } } | ConvertTo-Json -Compress -Depth 6
  $rootRun = Invoke-Bootstrap -WorkingDirectory $fixture -InputText $payload
  Add-Result 'bootstrap_root_no_git_spaces_allow' ($rootRun.exit_code -eq 0 -and [string]::IsNullOrWhiteSpace($rootRun.stdout) -and [string]::IsNullOrWhiteSpace($rootRun.stderr) -and -not (Test-Path -LiteralPath (Join-Path $fixture '.git'))) 'one root candidate; stdout empty'
  $nestedRun = Invoke-Bootstrap -WorkingDirectory $nested2 -InputText $payload
  Add-Result 'bootstrap_second_level_allow' ($nestedRun.exit_code -eq 0 -and [string]::IsNullOrWhiteSpace($nestedRun.stdout) -and [string]::IsNullOrWhiteSpace($nestedRun.stderr)) 'second-level cwd'
  $nested3Run = Invoke-Bootstrap -WorkingDirectory $nested3 -InputText $payload
  Add-Result 'bootstrap_third_level_allow' ($nested3Run.exit_code -eq 0 -and [string]::IsNullOrWhiteSpace($nested3Run.stdout) -and [string]::IsNullOrWhiteSpace($nested3Run.stderr)) 'third-level cwd'

  $stdinFixture = New-RootFixture -Base $tempBase -Name 'Stdin Fixture' -Mode stdin
  $stdinPayload = @{ hook_event_name = 'PreToolUse'; cwd = $stdinFixture; tool_name = 'Bash'; tool_input = @{ command = 'Get-Content README_FIRST.md' }; marker = 'complete synthetic stdin' } | ConvertTo-Json -Compress -Depth 6
  Write-Utf8File (Join-Path $stdinFixture 'scripts\codex\expected.sha256') (Get-Sha256Text $stdinPayload)
  $stdinRun = Invoke-Bootstrap -WorkingDirectory $stdinFixture -InputText $stdinPayload
  Add-Result 'bootstrap_forwards_complete_stdin' ($stdinRun.exit_code -eq 0 -and [string]::IsNullOrWhiteSpace($stdinRun.stdout) -and [string]::IsNullOrWhiteSpace($stdinRun.stderr)) 'fixture guard accepted raw UTF-8 payload hash'

  $denyFixture = New-RootFixture -Base $tempBase -Name 'Deny Fixture' -Mode deny
  $denyRun = Invoke-Bootstrap -WorkingDirectory $denyFixture -InputText $stdinPayload
  Add-Result 'bootstrap_forwards_one_deny_json' ($denyRun.exit_code -eq 0 -and [string]::IsNullOrWhiteSpace($denyRun.stderr) -and (Test-DenyJson $denyRun.stdout)) 'one parseable PreToolUse deny object'

  $outside = Join-Path $tempBase 'No Root'
  [System.IO.Directory]::CreateDirectory($outside) | Out-Null
  $noRoot = Invoke-Bootstrap -WorkingDirectory $outside -InputText $stdinPayload
  Add-Result 'bootstrap_root_not_found' ($noRoot.exit_code -eq 2 -and [string]::IsNullOrWhiteSpace($noRoot.stdout) -and $noRoot.stderr.Trim() -eq 'JOVI_HOOK_ROOT_NOT_FOUND') 'fixed stderr contract'

  $missing = Join-Path $tempBase 'Missing Wrapper'
  [System.IO.Directory]::CreateDirectory($missing) | Out-Null
  Write-Utf8File (Join-Path $missing 'AGENTS.md') '# synthetic'
  Write-Utf8File (Join-Path $missing 'PROJECT_STATE.json') '{}'
  $missingRun = Invoke-Bootstrap -WorkingDirectory $missing -InputText $stdinPayload
  Add-Result 'bootstrap_wrapper_missing' ($missingRun.exit_code -eq 2 -and [string]::IsNullOrWhiteSpace($missingRun.stdout) -and $missingRun.stderr.Trim() -eq 'JOVI_HOOK_ROOT_NOT_FOUND') 'missing wrapper prevents a root candidate'

  $decoy = Join-Path $fixture 'decoy root'
  [System.IO.Directory]::CreateDirectory($decoy) | Out-Null
  Write-Utf8File (Join-Path $decoy 'AGENTS.md') '# decoy'
  Write-Utf8File (Join-Path $decoy 'PROJECT_STATE.json') '{}'
  [System.IO.Directory]::CreateDirectory((Join-Path $decoy 'scripts\codex')) | Out-Null
  Write-Utf8File (Join-Path $decoy 'scripts\codex\Invoke-PreToolGuard.ps1') 'exit 0'
  $decoyNested = Join-Path $decoy 'child\grandchild'
  [System.IO.Directory]::CreateDirectory($decoyNested) | Out-Null
  $ambiguous = Invoke-Bootstrap -WorkingDirectory $decoyNested -InputText $stdinPayload
  Add-Result 'bootstrap_nested_decoy_root_denied' ($ambiguous.exit_code -eq 2 -and [string]::IsNullOrWhiteSpace($ambiguous.stdout) -and $ambiguous.stderr.Trim() -eq 'JOVI_HOOK_ROOT_AMBIGUOUS') 'multiple root candidates deny'

  $throwFixture = New-RootFixture -Base $tempBase -Name 'Throw Fixture' -Mode throw
  $throwRun = Invoke-Bootstrap -WorkingDirectory $throwFixture -InputText $stdinPayload
  Add-Result 'bootstrap_wrapper_throw_denied' ($throwRun.exit_code -eq 2 -and [string]::IsNullOrWhiteSpace($throwRun.stdout) -and $throwRun.stderr.Trim() -eq 'JOVI_HOOK_WRAPPER_FAILURE') 'no wrapper exception leakage'

  $stderrFixture = New-RootFixture -Base $tempBase -Name 'Stderr Fixture' -Mode stderr2
  $stderrRun = Invoke-Bootstrap -WorkingDirectory $stderrFixture -InputText $stdinPayload
  Add-Result 'bootstrap_stderr_exit2_denied' ($stderrRun.exit_code -eq 2 -and [string]::IsNullOrWhiteSpace($stderrRun.stdout) -and $stderrRun.stderr.Trim() -eq 'JOVI_HOOK_WRAPPER_DENY') 'recognized stderr plus exit 2 contract'

  $duplicateFixture = New-RootFixture -Base $tempBase -Name 'Duplicate Fixture' -Mode duplicate
  $duplicateRun = Invoke-Bootstrap -WorkingDirectory $duplicateFixture -InputText $stdinPayload
  Add-Result 'bootstrap_duplicate_deny_rejected' ($duplicateRun.exit_code -eq 2 -and [string]::IsNullOrWhiteSpace($duplicateRun.stdout) -and $duplicateRun.stderr.Trim() -eq 'JOVI_HOOK_WRAPPER_FAILURE') 'multiple JSON objects are not forwarded'

  $actualWrapper = Join-Path $fixture 'scripts\codex\Invoke-PreToolGuard.ps1'
  $py314Run = Invoke-Wrapper -Wrapper $actualWrapper -ProjectRoot $fixture -InputText $payload
  Add-Result 'wrapper_accepts_python_ge311' ($py314Run.exit_code -eq 0 -and [string]::IsNullOrWhiteSpace($py314Run.stdout) -and [string]::IsNullOrWhiteSpace($py314Run.stderr)) 'default launcher accepts available Python >= 3.11'
  $fallbackRun = Invoke-Wrapper -Wrapper $actualWrapper -ProjectRoot $fixture -InputText $payload -Candidates @('__missing_python__;python')
  Add-Result 'wrapper_falls_back_from_missing_launcher' ($fallbackRun.exit_code -eq 0 -and [string]::IsNullOrWhiteSpace($fallbackRun.stdout) -and [string]::IsNullOrWhiteSpace($fallbackRun.stderr)) ("missing candidate then python; exit={0}; stdout={1}; stderr={2}" -f $fallbackRun.exit_code, $fallbackRun.stdout.Length, $fallbackRun.stderr.Length)
  $noPythonRun = Invoke-Wrapper -Wrapper $actualWrapper -ProjectRoot $fixture -InputText $payload -Candidates @('__missing_python__')
  Add-Result 'wrapper_no_python_denies' ($noPythonRun.exit_code -eq 0 -and [string]::IsNullOrWhiteSpace($noPythonRun.stderr) -and (Test-DenyJson $noPythonRun.stdout)) 'single JSON deny'
  $emptyRun = Invoke-Wrapper -Wrapper $actualWrapper -ProjectRoot $fixture -InputText ''
  Add-Result 'wrapper_empty_stdin_denies' ($emptyRun.exit_code -eq 0 -and [string]::IsNullOrWhiteSpace($emptyRun.stderr) -and (Test-DenyJson $emptyRun.stdout)) 'single JSON deny'
  $malformedRun = Invoke-Wrapper -Wrapper $actualWrapper -ProjectRoot $fixture -InputText '{not-json'
  Add-Result 'wrapper_malformed_stdin_denies' ($malformedRun.exit_code -eq 0 -and [string]::IsNullOrWhiteSpace($malformedRun.stderr) -and (Test-DenyJson $malformedRun.stdout)) 'single JSON deny'

  $pythonCommand = (Get-Command -Name python -ErrorAction Stop).Source
  $guardUnit = Invoke-CapturedProcess -FileName $pythonCommand -Arguments '"tests\hooks\test_pre_tool_guard.py"' -WorkingDirectory $Root -InputText ''
  Add-Result 'structured_guard_regression_suite' ($guardUnit.exit_code -eq 0) ("exit={0}; output={1}" -f $guardUnit.exit_code, (($guardUnit.stdout + $guardUnit.stderr).Trim().Replace("`r", '').Replace("`n", '; ')))

  $after = @{}
  foreach ($file in $controlFiles) { $after[$file] = (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash }
  $changedControls = @($controlFiles | Where-Object { $before[$_] -ne $after[$_] })
  Add-Result 'real_control_files_unchanged_by_tests' ($changedControls.Count -eq 0) 'only temporary fixtures received synthetic writes'
  Add-Result 'no_external_xianyu_access' ($tempBase -notmatch 'xianyu-auto-reply' -and $Results.detail -notmatch 'E:\\project\\xianyu-auto-reply') 'all fixtures are under the system temporary directory'
} finally {
  if (Test-Path -LiteralPath $tempBase) { Remove-Item -LiteralPath $tempBase -Recurse -Force }
}

[System.IO.Directory]::CreateDirectory($ReportDirectory) | Out-Null
$passedCount = @($Results | Where-Object { $_.passed }).Count
$failedCount = @($Results | Where-Object { -not $_.passed }).Count
$report = [ordered]@{
  phase = 'H0'
  mode = 'OFFLINE_SYNTHETIC_WINDOWS_POWERSHELL'
  passed = $failedCount -eq 0
  passed_count = $passedCount
  failed_count = $failedCount
  skipped_count = 0
  root_not_found = $noRoot
  wrapper_failure = $throwRun
  deny_output = $denyRun.stdout
  configured_commandWindows = $configuredCommandWindows
  tested_commandWindows = $testedCommandWindows
  results = $Results
}
[System.IO.File]::WriteAllText((Join-Path $ReportDirectory 'H0_HOOK_TESTS.json'), ($report | ConvertTo-Json -Depth 8), $Utf8NoBom)
$lines = @('# H0 Hook Test Results', '', "- Passed: $passedCount", "- Failed: $failedCount", '- Skipped: 0', '', '| Test | Result | Detail |', '|---|---|---|')
foreach ($item in $Results) { $lines += "| $($item.name) | $(if ($item.passed) { 'PASS' } else { 'FAIL' }) | $($item.detail.Replace('|', '\|')) |" }
[System.IO.File]::WriteAllText((Join-Path $ReportDirectory 'H0_HOOK_TESTS.md'), (($lines -join "`n") + "`n"), $Utf8NoBom)
exit $(if ($failedCount -eq 0) { 0 } else { 2 })
