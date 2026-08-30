[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [ValidateNotNullOrEmpty()]
  [string]$ProjectRoot,
  [string[]]$PythonCandidates
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-PreToolDeny {
  param([Parameter(Mandatory = $true)][string]$Reason)

  $response = [ordered]@{
    hookSpecificOutput = [ordered]@{
      hookEventName = 'PreToolUse'
      permissionDecision = 'deny'
      permissionDecisionReason = $Reason
    }
  }
  [Console]::Out.WriteLine(($response | ConvertTo-Json -Compress -Depth 4))
}

function Read-Utf8StandardInput {
  $inputStream = [Console]::OpenStandardInput()
  $buffer = New-Object System.IO.MemoryStream
  try {
    $inputStream.CopyTo($buffer)
    $text = $script:Utf8NoBom.GetString($buffer.ToArray())
    return $text.TrimStart([char]0xFEFF)
  } finally {
    $buffer.Dispose()
  }
}

function Test-PythonCandidate {
  param([Parameter(Mandatory = $true)]$Candidate)

  $name = [string]$Candidate.FileName
  if ([string]::IsNullOrWhiteSpace($name)) {
    return $null
  }
  $command = Get-Command -Name $name -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($null -eq $command) {
    return $null
  }

  $arguments = @()
  if ($null -ne $Candidate.Arguments) {
    $arguments = @($Candidate.Arguments | ForEach-Object { [string]$_ })
  }

  $probe = 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'
  $hadNativePreference = $null -ne (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue)
  if ($hadNativePreference) {
    $savedNativePreference = $PSNativeCommandUseErrorActionPreference
    $PSNativeCommandUseErrorActionPreference = $false
  }
  try {
    & $command.Source @arguments -c $probe 2>$null
    if ($LASTEXITCODE -eq 0) {
      return [pscustomobject]@{
        FileName = [string]$command.Source
        Arguments = $arguments
      }
    }
  } catch {
    # An unavailable launcher is a normal probe miss. The caller will try the next candidate.
  } finally {
    if ($hadNativePreference) {
      $PSNativeCommandUseErrorActionPreference = $savedNativePreference
    }
  }
  return $null
}

function Get-PythonInterpreter {
  param([object[]]$Candidates)

  if ($null -eq $Candidates) {
    $Candidates = @(
      [pscustomobject]@{ FileName = 'py'; Arguments = @('-3') },
      [pscustomobject]@{ FileName = 'python'; Arguments = @() },
      [pscustomobject]@{ FileName = 'python3'; Arguments = @() }
    )
    $pathPython = Get-Command -Name 'python.exe' -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -ne $pathPython) {
      $Candidates += [pscustomobject]@{ FileName = [string]$pathPython.Source; Arguments = @() }
    }
  } else {
    $Candidates = @($Candidates | ForEach-Object {
      [string]$_ -split ';' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | ForEach-Object {
        [pscustomobject]@{ FileName = [string]$_; Arguments = @() }
      }
    })
  }

  foreach ($candidate in @($Candidates)) {
    $interpreter = Test-PythonCandidate -Candidate $candidate
    if ($null -ne $interpreter) {
      return $interpreter
    }
  }
  return $null
}

function Invoke-PythonGuard {
  param(
    [Parameter(Mandatory = $true)]$Interpreter,
    [Parameter(Mandatory = $true)][string]$GuardScript,
    [Parameter(Mandatory = $true)][string]$Root,
    [Parameter(Mandatory = $true)][string]$InputJson
  )

  $startInfo = New-Object System.Diagnostics.ProcessStartInfo
  $startInfo.FileName = [string]$Interpreter.FileName
  $allArguments = @($Interpreter.Arguments) + @('"' + $GuardScript + '"', '--root', '"' + $Root + '"')
  $startInfo.Arguments = ($allArguments -join ' ')
  $startInfo.UseShellExecute = $false
  $startInfo.CreateNoWindow = $true
  $startInfo.RedirectStandardInput = $true
  $startInfo.RedirectStandardOutput = $true
  $startInfo.RedirectStandardError = $true

  $process = New-Object System.Diagnostics.Process
  $process.StartInfo = $startInfo
  if (-not $process.Start()) {
    throw 'Python guard did not start.'
  }
  $stdoutTask = $process.StandardOutput.ReadToEndAsync()
  $stderrTask = $process.StandardError.ReadToEndAsync()
  $inputBytes = $script:Utf8NoBom.GetBytes($InputJson)
  $process.StandardInput.BaseStream.Write($inputBytes, 0, $inputBytes.Length)
  $process.StandardInput.Close()
  $process.WaitForExit()
  $stdout = $stdoutTask.Result
  $stderr = $stderrTask.Result
  return [pscustomobject]@{
    ExitCode = $process.ExitCode
    Stdout = $stdout
    Stderr = $stderr
  }
}

try {
  $script:Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  $rawInput = Read-Utf8StandardInput
  if ([string]::IsNullOrWhiteSpace($rawInput)) {
    Write-PreToolDeny 'Hook input was empty.'
    exit 0
  }
  try {
    $parsedInput = @($rawInput | ConvertFrom-Json -ErrorAction Stop)
    if ($parsedInput.Count -ne 1 -or $parsedInput[0] -isnot [pscustomobject]) {
      throw 'Input is not one JSON object.'
    }
  } catch {
    Write-PreToolDeny 'Hook input was malformed.'
    exit 0
  }

  $guardScript = Join-Path $PSScriptRoot 'pre_tool_guard.py'
  if (-not (Test-Path -LiteralPath $guardScript -PathType Leaf)) {
    Write-PreToolDeny 'Hook guard was unavailable.'
    exit 0
  }
  if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
    Write-PreToolDeny 'Hook project root was invalid.'
    exit 0
  }

  $interpreter = Get-PythonInterpreter -Candidates $PythonCandidates
  if ($null -eq $interpreter) {
    Write-PreToolDeny 'Python 3.11 or newer was unavailable.'
    exit 0
  }

  $result = Invoke-PythonGuard -Interpreter $interpreter -GuardScript $guardScript -Root $ProjectRoot -InputJson $rawInput
  if ($result.ExitCode -ne 0 -or -not [string]::IsNullOrWhiteSpace($result.Stderr)) {
    Write-PreToolDeny 'Hook guard failed safely.'
    exit 0
  }
  if ([string]::IsNullOrWhiteSpace($result.Stdout)) {
    exit 0
  }

  try {
    $parsedOutput = @($result.Stdout | ConvertFrom-Json -ErrorAction Stop)
    if (
      $parsedOutput.Count -ne 1 -or
      $parsedOutput[0].hookSpecificOutput.hookEventName -ne 'PreToolUse' -or
      $parsedOutput[0].hookSpecificOutput.permissionDecision -ne 'deny' -or
      [string]::IsNullOrWhiteSpace([string]$parsedOutput[0].hookSpecificOutput.permissionDecisionReason)
    ) {
      throw 'Guard response is not a PreToolUse deny object.'
    }
  } catch {
    Write-PreToolDeny 'Hook guard returned an invalid response.'
    exit 0
  }
  [Console]::Out.WriteLine($result.Stdout.Trim())
  exit 0
} catch {
  Write-PreToolDeny 'Hook wrapper failed safely.'
  exit 0
}
