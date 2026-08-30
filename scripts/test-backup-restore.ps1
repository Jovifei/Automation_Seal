[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$BackupDirectory
)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot 'common.ps1')
Invoke-JoviPython -Script (Join-Path $PSScriptRoot 'verify-gate-approval.py') -Arguments @('--root',$root,'--gate','GATE_A','--track','I') | Out-Null
if($LASTEXITCODE -ne 0){throw 'GATE_A Track I approval is missing or invalid.'}
$backup=(Resolve-Path $BackupDirectory).Path
$dump=Join-Path $backup 'postgres.dump'
if(-not (Test-Path $dump -PathType Leaf)){throw 'postgres.dump is missing.'}
$envPath=Join-Path $root 'deploy/.env.runtime'
if(-not (Test-Path $envPath)){$envPath=Join-Path $root 'deploy/.env'}
if(-not (Test-Path $envPath)){throw 'deploy/.env is missing.'}
$settings=@{}
Get-Content $envPath | Where-Object {$_ -match '^[A-Z0-9_]+='} | ForEach-Object {$k,$v=$_.Split('=',2);$settings[$k]=$v}
foreach($required in @('POSTGRES_IMAGE','POSTGRES_USER','POSTGRES_PASSWORD','POSTGRES_DB')){if(-not $settings[$required]){throw "Missing $required in deploy/.env"}}
$name='jovi-restore-test-'+([Guid]::NewGuid().ToString('N').Substring(0,10))
try{
  docker run -d --rm --name $name --tmpfs /var/lib/postgresql/data:rw,noexec,nosuid,size=1g `
    -e "POSTGRES_USER=$($settings.POSTGRES_USER)" `
    -e "POSTGRES_PASSWORD=$($settings.POSTGRES_PASSWORD)" `
    -e "POSTGRES_DB=$($settings.POSTGRES_DB)" `
    $settings.POSTGRES_IMAGE | Out-Null
  if($LASTEXITCODE -ne 0){throw 'Could not start isolated restore container.'}
  $ready=$false
  for($i=0;$i -lt 30;$i++){
    docker exec $name pg_isready -U $settings.POSTGRES_USER -d $settings.POSTGRES_DB *> $null
    if($LASTEXITCODE -eq 0){$ready=$true;break}
    Start-Sleep -Seconds 2
  }
  if(-not $ready){throw 'Isolated restore database did not become ready.'}
  docker cp $dump "${name}:/tmp/postgres.dump"
  if($LASTEXITCODE -ne 0){throw 'Could not copy dump into isolated container.'}
  docker exec $name pg_restore --clean --if-exists --no-owner -U $settings.POSTGRES_USER -d $settings.POSTGRES_DB /tmp/postgres.dump
  if($LASTEXITCODE -ne 0){throw 'pg_restore failed in isolated container.'}
  $tables=docker exec $name psql -U $settings.POSTGRES_USER -d $settings.POSTGRES_DB -Atc "select count(*) from pg_catalog.pg_tables where schemaname not in ('pg_catalog','information_schema');"
  if($LASTEXITCODE -ne 0){throw 'Could not verify restored database.'}
  $reportDir=Join-Path $root 'reports/restore-tests'
  New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
  [ordered]@{tested_at=(Get-Date).ToString('o');backup=$backup;container=$name;application_table_count=[int]$tables;result='PASS';production_modified=$false} | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 (Join-Path $reportDir ('postgres-'+(Get-Date -Format 'yyyyMMdd-HHmmss')+'.json'))
  Write-Host "[PASS] Isolated PostgreSQL restore succeeded; application tables: $tables"
}finally{
  docker rm -f $name *> $null
}
