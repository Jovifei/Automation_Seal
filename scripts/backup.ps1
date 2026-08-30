[CmdletBinding()]
param([string]$SecretBackupPath)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot 'common.ps1')
Invoke-JoviPython -Script (Join-Path $PSScriptRoot 'verify-gate-approval.py') -Arguments @('--root',$root,'--gate','GATE_A','--track','I') | Out-Null
if($LASTEXITCODE -ne 0){throw 'GATE_A Track I approval is missing or invalid.'}
$stamp=Get-Date -Format 'yyyyMMdd-HHmmss'
$dest=Join-Path $root "backups/$stamp"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$envPath=Join-Path $root 'deploy/.env.runtime'
if(-not (Test-Path $envPath)){$envPath=Join-Path $root 'deploy/.env'}
if(-not (Test-Path $envPath)){throw 'deploy/.env is missing.'}
$settings=@{}
Get-Content $envPath | Where-Object {$_ -match '^[A-Z0-9_]+='} | ForEach-Object {$k,$v=$_.Split('=',2);$settings[$k]=$v}
$dump='/tmp/jovi-postgres.dump'
docker exec jovi-postgres pg_dump -U $settings.POSTGRES_USER -d $settings.POSTGRES_DB -Fc -f $dump
if($LASTEXITCODE -ne 0){throw 'PostgreSQL dump failed.'}
docker cp "jovi-postgres:$dump" (Join-Path $dest 'postgres.dump')
docker exec jovi-postgres rm -f $dump | Out-Null
if(Test-Path (Join-Path $root 'data/changedetection')){Copy-Item -Recurse (Join-Path $root 'data/changedetection') (Join-Path $dest 'changedetection')}
if(Test-Path (Join-Path $root 'workspace')){Copy-Item -Recurse (Join-Path $root 'workspace') (Join-Path $dest 'workspace')}
docker cp 'jovi-n8n:/home/node/.n8n' (Join-Path $dest 'n8n-data') | Out-Null
Copy-Item -Force (Join-Path $root 'LOCKED_VERSIONS.json') $dest -ErrorAction SilentlyContinue
if($SecretBackupPath){
  New-Item -ItemType Directory -Force -Path $SecretBackupPath | Out-Null
  Copy-Item -Force $envPath (Join-Path $SecretBackupPath "jovi-env-$stamp.txt")
  Write-Warning 'Encrypt and protect the secret backup immediately.'
}else{
  'deploy/.env is not included. Re-run with an encrypted/removable SecretBackupPath.' | Set-Content -Encoding UTF8 (Join-Path $dest 'SECRETS_NOT_BACKED_UP.txt')
}
'Xianyu data is intentionally excluded. Back it up independently using docs/05.' | Set-Content -Encoding UTF8 (Join-Path $dest 'XIANYU_BACKUP_SEPARATE.txt')
Get-ChildItem -Recurse -File $dest | Where-Object {$_.Name -ne 'sha256.json'} | Get-FileHash -Algorithm SHA256 | Select-Object Path,Hash | ConvertTo-Json -Depth 3 | Set-Content -Encoding UTF8 (Join-Path $dest 'sha256.json')
Write-Host "Backup complete: $dest"
