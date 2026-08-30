[CmdletBinding()]
param()
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot 'common.ps1')
$reportDir = Join-Path $root 'reports/phase-a'
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
$report = Join-Path $reportDir 'preflight.json'
$results = [ordered]@{
  schema_version=3
  timestamp=(Get-Date).ToString('o')
  root=$root
  checks=@()
}
function Add-Check($name,$ok,$detail,$trackP='optional',$trackI='optional'){
  $results.checks += [ordered]@{
    name=$name
    ok=[bool]$ok
    detail="$detail"
    track_p=$trackP
    track_i=$trackI
  }
  $mark = if($ok){'[PASS]'}else{'[WARN]'}
  Write-Host "$mark $name - $detail"
}
function Has-Command($name){ [bool](Get-Command $name -ErrorAction SilentlyContinue) }
function Safe-Version($name,$args=@('--version')){
  if(-not (Has-Command $name)){ return 'missing' }
  try { return ((& $name @args 2>&1 | Select-Object -First 4 | Out-String).Trim()) } catch { return 'present; version unavailable' }
}

Add-Check 'Project root exists' (Test-Path $root) $root 'required' 'required'
Add-Check 'AGENTS.md exists' (Test-Path (Join-Path $root 'AGENTS.md')) 'project instruction file' 'required' 'required'
Add-Check 'PROJECT_STATE.json exists' (Test-Path (Join-Path $root 'PROJECT_STATE.json')) 'machine-readable handoff state' 'required' 'required'
Add-Check 'Path length below 180' ($root.Length -lt 180) "length=$($root.Length)" 'recommended' 'recommended'
Add-Check 'Path has no spaces' ($root -notmatch '\s') $root 'recommended' 'recommended'

try {
  $os = Get-CimInstance Win32_OperatingSystem
  Add-Check 'Windows 64-bit' (($os.OSArchitecture -match '64') -and ($os.Caption -match 'Windows')) "$($os.Caption) $($os.Version)" 'required' 'required'
} catch {
  Add-Check 'Windows 64-bit' $false $_.Exception.Message 'required' 'required'
}

try {
  $driveName = (Split-Path -Qualifier $root).TrimEnd(':')
  $free = [math]::Round((Get-PSDrive -Name $driveName).Free/1GB,1)
  Add-Check 'Free disk >= 5 GB for Track P' ($free -ge 5) "$free GB free" 'required' 'optional'
  Add-Check 'Free disk >= 30 GB for Track I' ($free -ge 30) "$free GB free" 'optional' 'required'
} catch {
  Add-Check 'Free disk' $false $_.Exception.Message 'required' 'required'
}

try {
  $py=Get-JoviPython
  Add-Check 'Python 3.11+' $true "$($py.Exe) $($py.Prefix -join ' ') $($py.Version)" 'required' 'required'
} catch {
  Add-Check 'Python 3.11+' $false $_.Exception.Message 'required' 'required'
}

$commands = @(
  @{n='git'; p='recommended'; i='recommended'},
  @{n='codex'; p='recommended'; i='recommended'},
  @{n='node'; p='optional'; i='optional'},
  @{n='npm'; p='optional'; i='optional'},
  @{n='docker'; p='optional'; i='required'},
  @{n='wsl'; p='optional'; i='recommended'},
  @{n='nvidia-smi'; p='optional'; i='optional'}
)
foreach($item in $commands){
  $exists=Has-Command $item.n
  Add-Check $item.n $exists (Safe-Version $item.n) $item.p $item.i
}

if(Has-Command docker){
  docker info *> $null
  Add-Check 'Docker daemon running' ($LASTEXITCODE -eq 0) "exit=$LASTEXITCODE" 'optional' 'required'
  docker compose version *> $null
  Add-Check 'Docker Compose v2' ($LASTEXITCODE -eq 0) "exit=$LASTEXITCODE" 'optional' 'required'
}

try {
  $scheme=(powercfg /GETACTIVESCHEME 2>&1 | Out-String).Trim()
  Add-Check 'Power plan captured' ($LASTEXITCODE -eq 0) $scheme 'recommended' 'recommended'
} catch {
  Add-Check 'Power plan captured' $false $_.Exception.Message 'recommended' 'recommended'
}

foreach($p in 5678,5000,9000,5900,6080){
  $busy = Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue
  Add-Check "Port $p inventory" $true ($(if($busy){'currently in use'}else{'free'})) 'optional' 'optional'
}

$results | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $report
Write-Host "Preflight report: $report"
exit 0
