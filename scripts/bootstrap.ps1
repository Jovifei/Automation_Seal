[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot 'common.ps1')
Invoke-JoviPython -Script (Join-Path $PSScriptRoot 'verify-gate-approval.py') -Arguments @('--root',$root,'--gate','GATE_A','--track','I') | Out-Null
if($LASTEXITCODE -ne 0){throw 'GATE_A Track I approval is missing or invalid.'}
Invoke-JoviPython -Script (Join-Path $PSScriptRoot 'validate-package.py') | Out-Null
if($LASTEXITCODE -ne 0){throw 'Package validation failed.'}
$envFile=Join-Path $root 'deploy/.env'
$example=Join-Path $root 'deploy/.env.example'
if(-not (Test-Path $envFile)){
  Copy-Item $example $envFile
  function New-Secret([int]$bytes=32){
    $b=New-Object byte[] $bytes
    $rng=[Security.Cryptography.RandomNumberGenerator]::Create()
    try{$rng.GetBytes($b)}finally{$rng.Dispose()}
    return ([BitConverter]::ToString($b)).Replace('-','').ToLowerInvariant()
  }
  $c=Get-Content $envFile -Raw
  $c=$c -replace 'POSTGRES_PASSWORD=CHANGE_ME',('POSTGRES_PASSWORD='+(New-Secret 32))
  $c=$c -replace 'N8N_ENCRYPTION_KEY=CHANGE_ME',('N8N_ENCRYPTION_KEY='+(New-Secret 32))
  $c=$c -replace 'REDIS_PASSWORD=CHANGE_ME',('REDIS_PASSWORD='+(New-Secret 32))
  [IO.File]::WriteAllText($envFile,$c,(New-Object Text.UTF8Encoding($false)))
  Write-Host 'Generated deploy/.env. Do not commit, log or paste it into chat.'
}
$dirs=@('data/n8n-files','data/changedetection','workspace/review-queue','workspace/approved','workspace/quarantine','workspace/approvals','workspace/products','backups','reports','logs','vendor')
foreach($d in $dirs){New-Item -ItemType Directory -Force -Path (Join-Path $root $d)|Out-Null}
Push-Location (Join-Path $root 'deploy')
try{
  docker compose --env-file .env -f docker-compose.core.yml config | Out-File -Encoding UTF8 (Join-Path $root 'reports/compose-rendered.yml')
  if($LASTEXITCODE -ne 0){throw 'Compose validation failed.'}
}finally{Pop-Location}
Write-Host 'Bootstrap complete. User must review deploy/.env and reports/compose-rendered.yml before start-core.ps1.'
