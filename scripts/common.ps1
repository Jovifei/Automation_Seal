function ConvertTo-JoviProcessArgument {
  param([AllowNull()][string]$Value)

  if ($null -eq $Value -or $Value.Length -eq 0) {
    return '""'
  }
  if ($Value -notmatch '[\s"]') {
    return $Value
  }

  $builder = New-Object System.Text.StringBuilder
  [void]$builder.Append('"')
  $slashCount = 0
  foreach ($character in $Value.ToCharArray()) {
    if ($character -eq '\') {
      $slashCount++
      continue
    }
    if ($character -eq '"') {
      if ($slashCount -gt 0) {
        [void]$builder.Append((('\' * ($slashCount * 2)) -join ''))
      }
      [void]$builder.Append('\')
      [void]$builder.Append('"')
      $slashCount = 0
      continue
    }
    if ($slashCount -gt 0) {
      [void]$builder.Append((('\' * $slashCount) -join ''))
      $slashCount = 0
    }
    [void]$builder.Append($character)
  }
  if ($slashCount -gt 0) {
    [void]$builder.Append((('\' * ($slashCount * 2)) -join ''))
  }
  [void]$builder.Append('"')
  return $builder.ToString()
}

function Invoke-JoviProcess {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory = $true)][string]$FileName,
    [string[]]$Arguments = @(),
    [ValidateRange(0, 60000)][int]$TimeoutMilliseconds = 0
  )

  $startInfo = New-Object System.Diagnostics.ProcessStartInfo
  $startInfo.FileName = $FileName
  $quotedArguments = @($Arguments | ForEach-Object { ConvertTo-JoviProcessArgument -Value ([string]$_) })
  $startInfo.Arguments = ($quotedArguments -join ' ')
  $startInfo.UseShellExecute = $false
  $startInfo.CreateNoWindow = $true
  $startInfo.RedirectStandardOutput = $true
  $startInfo.RedirectStandardError = $true

  $process = New-Object System.Diagnostics.Process
  $process.StartInfo = $startInfo
  try {
    if (-not $process.Start()) {
      return [pscustomobject]@{ Started = $false; TimedOut = $false; ExitCode = $null; Stdout = ''; Stderr = ''; Error = 'START_FAILED' }
    }
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $exited = if ($TimeoutMilliseconds -gt 0) { $process.WaitForExit($TimeoutMilliseconds) } else { $process.WaitForExit(); $true }
    if (-not $exited) {
      try { $process.Kill() } catch {}
      $process.WaitForExit()
      return [pscustomobject]@{ Started = $true; TimedOut = $true; ExitCode = $null; Stdout = $stdoutTask.Result; Stderr = $stderrTask.Result; Error = 'TIMED_OUT' }
    }
    return [pscustomobject]@{ Started = $true; TimedOut = $false; ExitCode = $process.ExitCode; Stdout = $stdoutTask.Result; Stderr = $stderrTask.Result; Error = '' }
  } catch {
    return [pscustomobject]@{ Started = $false; TimedOut = $false; ExitCode = $null; Stdout = ''; Stderr = ''; Error = 'START_FAILED' }
  } finally {
    $process.Dispose()
  }
}

function ConvertFrom-JoviPythonVersion {
  param([AllowNull()][string]$Text)

  if ([string]::IsNullOrWhiteSpace($Text)) {
    return $null
  }
  $match = [regex]::Match($Text, '(?im)(?:^|\s)(?:Python\s+)?(?<major>\d+)\.(?<minor>\d+)(?:\.(?<build>\d+))?(?=\s|$)')
  if (-not $match.Success) {
    return $null
  }
  try {
    $major = [int]$match.Groups['major'].Value
    $minor = [int]$match.Groups['minor'].Value
    $build = if ($match.Groups['build'].Success) { [int]$match.Groups['build'].Value } else { 0 }
    return New-Object System.Version($major, $minor, $build)
  } catch {
    return $null
  }
}

function Get-JoviPython {
  [CmdletBinding()]
  param(
    [object[]]$Candidates,
    [ValidateRange(100, 60000)][int]$ProbeTimeoutMilliseconds = 5000
  )

  $savedErrorActionPreference = $ErrorActionPreference
  $savedLastExitCode = $global:LASTEXITCODE
  $savedLocation = Get-Location
  $savedPath = $env:PATH
  $failureMessage = 'Python 3.11+ is required. See FIRST_RUN_TROUBLESHOOTING.md.'
  try {
    if ($null -eq $Candidates) {
      $Candidates = @(
        [pscustomobject]@{ FileName = 'py'; Prefix = @('-3') },
        [pscustomobject]@{ FileName = 'python'; Prefix = @() },
        [pscustomobject]@{ FileName = 'python3'; Prefix = @() }
      )
      $pathPython = Get-Command -Name 'python.exe' -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
      if ($null -ne $pathPython) {
        $Candidates += [pscustomobject]@{ FileName = [string]$pathPython.Source; Prefix = @() }
      }
    }

    $minimumVersion = New-Object System.Version -ArgumentList 3, 11
    $seen = @{}
    foreach ($candidate in @($Candidates)) {
      if ($candidate -is [string]) {
        $fileName = [string]$candidate
        $prefix = @()
      } else {
        $fileName = [string]$candidate.FileName
        $prefix = if ($null -eq $candidate.Prefix) { @() } else { @($candidate.Prefix | ForEach-Object { [string]$_ }) }
      }
      if ([string]::IsNullOrWhiteSpace($fileName)) {
        continue
      }
      $key = $fileName.Trim().ToLowerInvariant() + '|' + ($prefix -join "`0")
      if ($seen.ContainsKey($key)) {
        continue
      }
      $seen[$key] = $true

      $probe = Invoke-JoviProcess -FileName $fileName -Arguments (@($prefix) + @('--version')) -TimeoutMilliseconds $ProbeTimeoutMilliseconds
      if (-not $probe.Started -or $probe.TimedOut -or $probe.ExitCode -ne 0 -or -not [string]::IsNullOrWhiteSpace($probe.Stderr)) {
        continue
      }
      $version = ConvertFrom-JoviPythonVersion -Text $probe.Stdout
      if ($null -eq $version -or $version -lt $minimumVersion) {
        continue
      }
      return [ordered]@{ Exe = $fileName; Prefix = $prefix; Version = $version.ToString() }
    }
    throw $failureMessage
  } catch {
    throw $failureMessage
  } finally {
    $ErrorActionPreference = $savedErrorActionPreference
    $env:PATH = $savedPath
    if ((Get-Location).Path -ne $savedLocation.Path) {
      Set-Location -LiteralPath $savedLocation.Path
    }
    $global:LASTEXITCODE = $savedLastExitCode
  }
}

function Invoke-JoviPython {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory = $true)][string]$Script,
    [string[]]$Arguments = @(),
    [switch]$AllowFailure
  )

  $py = Get-JoviPython
  $result = Invoke-JoviProcess -FileName $py.Exe -Arguments (@($py.Prefix) + @($Script) + @($Arguments))
  if (-not [string]::IsNullOrEmpty($result.Stdout)) {
    [Console]::Out.Write($result.Stdout)
  }
  if (-not [string]::IsNullOrEmpty($result.Stderr)) {
    [Console]::Error.Write($result.Stderr)
  }
  if (-not $result.Started) {
    $global:LASTEXITCODE = 1
    throw "Python process could not start: $Script"
  }
  if ($result.TimedOut) {
    $global:LASTEXITCODE = 124
    throw "Python step timed out: $Script"
  }
  $code = [int]$result.ExitCode
  $global:LASTEXITCODE = $code
  if ((-not $AllowFailure) -and $code -ne 0) {
    throw "Python step failed with exit code ${code}: $Script"
  }
  return $code
}
