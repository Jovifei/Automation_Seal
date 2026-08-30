Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-BootstrapFailure {
  param([Parameter(Mandatory = $true)][string]$Code)
  [Console]::Error.WriteLine($Code)
  exit 2
}

function Read-Utf8StandardInput {
  $inputStream = [Console]::OpenStandardInput()
  $buffer = New-Object System.IO.MemoryStream
  try {
    $inputStream.CopyTo($buffer)
    $encoding = New-Object System.Text.UTF8Encoding($false)
    return ($encoding.GetString($buffer.ToArray())).TrimStart([char]0xFEFF)
  } finally {
    $buffer.Dispose()
  }
}

function Get-CanonicalDirectory {
  param([Parameter(Mandatory = $true)][string]$Path)
  $resolved = Resolve-Path -LiteralPath $Path -ErrorAction Stop
  if (-not (Test-Path -LiteralPath $resolved.Path -PathType Container)) {
    throw 'Not a filesystem directory.'
  }
  $full = [System.IO.Path]::GetFullPath($resolved.Path)
  $volumeRoot = [System.IO.Path]::GetPathRoot($full)
  if ([string]::IsNullOrWhiteSpace($volumeRoot)) {
    throw 'Path has no filesystem root.'
  }
  if ($full -eq $volumeRoot) {
    return $volumeRoot
  }
  return $full.TrimEnd([System.IO.Path]::DirectorySeparatorChar)
}

function Get-ProjectRootCandidates {
  $cursor = Get-CanonicalDirectory -Path (Get-Location).Path
  $seen = @{}
  $candidates = @()
  while ($true) {
    $agents = Join-Path $cursor 'AGENTS.md'
    $state = Join-Path $cursor 'PROJECT_STATE.json'
    $wrapper = Join-Path $cursor 'scripts\codex\Invoke-PreToolGuard.ps1'
    if ((Test-Path -LiteralPath $agents -PathType Leaf) -and (Test-Path -LiteralPath $state -PathType Leaf) -and (Test-Path -LiteralPath $wrapper -PathType Leaf)) {
      $candidate = Get-CanonicalDirectory -Path $cursor
      if (-not $seen.ContainsKey($candidate)) {
        $seen[$candidate] = $true
        $candidates += $candidate
      }
    }
    $parent = [System.IO.Directory]::GetParent($cursor)
    if ($null -eq $parent) {
      break
    }
    $next = Get-CanonicalDirectory -Path $parent.FullName
    if ($next -eq $cursor) {
      break
    }
    $cursor = $next
  }
  return @($candidates)
}

function Test-PreToolDenyJson {
  param([Parameter(Mandatory = $true)][string]$Text)
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

function Invoke-WrapperProcess {
  param(
    [Parameter(Mandatory = $true)][string]$Wrapper,
    [Parameter(Mandatory = $true)][string]$ProjectRoot,
    [Parameter(Mandatory = $true)][string]$InputJson
  )
  $hostPath = Join-Path $PSHOME 'powershell.exe'
  if (-not (Test-Path -LiteralPath $hostPath -PathType Leaf)) {
    $hostPath = 'powershell.exe'
  }
  $startInfo = New-Object System.Diagnostics.ProcessStartInfo
  $startInfo.FileName = $hostPath
  $startInfo.Arguments = '-NoProfile -File "' + $Wrapper + '" -ProjectRoot "' + $ProjectRoot + '"'
  $startInfo.UseShellExecute = $false
  $startInfo.CreateNoWindow = $true
  $startInfo.RedirectStandardInput = $true
  $startInfo.RedirectStandardOutput = $true
  $startInfo.RedirectStandardError = $true

  $process = New-Object System.Diagnostics.Process
  $process.StartInfo = $startInfo
  if (-not $process.Start()) {
    throw 'Wrapper process did not start.'
  }
  $stdoutTask = $process.StandardOutput.ReadToEndAsync()
  $stderrTask = $process.StandardError.ReadToEndAsync()
  $inputBytes = (New-Object System.Text.UTF8Encoding($false)).GetBytes($InputJson)
  $process.StandardInput.BaseStream.Write($inputBytes, 0, $inputBytes.Length)
  $process.StandardInput.Close()
  $process.WaitForExit()
  return [pscustomobject]@{
    ExitCode = $process.ExitCode
    Stdout = $stdoutTask.Result
    Stderr = $stderrTask.Result
  }
}

try {
  $rawInput = Read-Utf8StandardInput
  $roots = @(Get-ProjectRootCandidates)
  if ($roots.Count -eq 0) {
    Write-BootstrapFailure 'JOVI_HOOK_ROOT_NOT_FOUND'
  }
  if ($roots.Count -ne 1) {
    Write-BootstrapFailure 'JOVI_HOOK_ROOT_AMBIGUOUS'
  }

  $projectRoot = $roots[0]
  $wrapper = Join-Path $projectRoot 'scripts\codex\Invoke-PreToolGuard.ps1'
  $result = Invoke-WrapperProcess -Wrapper $wrapper -ProjectRoot $projectRoot -InputJson $rawInput

  if ($result.ExitCode -eq 0 -and [string]::IsNullOrWhiteSpace($result.Stdout) -and [string]::IsNullOrWhiteSpace($result.Stderr)) {
    exit 0
  }
  if ($result.ExitCode -eq 0 -and [string]::IsNullOrWhiteSpace($result.Stderr) -and (Test-PreToolDenyJson -Text $result.Stdout)) {
    [Console]::Out.Write($result.Stdout)
    exit 0
  }
  if ($result.ExitCode -eq 2 -and [string]::IsNullOrWhiteSpace($result.Stdout) -and $result.Stderr.Trim() -eq 'JOVI_HOOK_WRAPPER_DENY') {
    [Console]::Error.WriteLine('JOVI_HOOK_WRAPPER_DENY')
    exit 2
  }
  Write-BootstrapFailure 'JOVI_HOOK_WRAPPER_FAILURE'
} catch {
  Write-BootstrapFailure 'JOVI_HOOK_BOOTSTRAP_FAILURE'
}
