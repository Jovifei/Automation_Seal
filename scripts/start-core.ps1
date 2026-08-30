[CmdletBinding()]
param([switch]$WithResearch)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot 'common.ps1')
Invoke-JoviPython -Script (Join-Path $PSScriptRoot 'verify-gate-approval.py') -Arguments @('--root',$root,'--gate','GATE_A','--track','I') | Out-Null
$envPath=Join-Path $root 'deploy/.env'
$runtimeEnv=Join-Path $root 'deploy/.env.runtime'
if(-not (Test-Path $envPath)){throw 'deploy/.env missing. Run bootstrap.ps1.'}
$envText=Get-Content $envPath -Raw
if($envText -match 'CHANGE_ME'){throw 'deploy/.env contains CHANGE_ME.'}

function Read-EnvFile([string]$Path){
  $map=@{}
  Get-Content $Path | Where-Object {$_ -match '^[A-Z0-9_]+='} | ForEach-Object {
    $k,$v=$_.Split('=',2);$map[$k]=$v
  }
  return $map
}
function Resolve-ImageDigest([string]$Image){
  $raw=docker image inspect $Image 2>$null
  if($LASTEXITCODE -ne 0){throw "Could not inspect pulled image: $Image"}
  $data=$raw | ConvertFrom-Json
  $digests=@($data[0].RepoDigests) | Where-Object {$_ -match '@sha256:[a-f0-9]{64}$'}
  if(-not $digests){throw "No RepoDigest available for image: $Image"}
  $repo=($Image -replace '@sha256:[a-f0-9]{64}$','') -replace ':[^/:]+$',''
  $preferred=$digests | Where-Object {$_ -like "$repo@sha256:*"} | Select-Object -First 1
  if($preferred){return $preferred}
  return ($digests | Sort-Object | Select-Object -First 1)
}
function Replace-EnvValue([string]$Text,[string]$Key,[string]$Value){
  $escaped=[regex]::Escape($Key)
  if($Text -match "(?m)^$escaped="){
    return [regex]::Replace($Text,"(?m)^$escaped=.*$",("$Key=$Value"))
  }
  return $Text.TrimEnd()+"`r`n$Key=$Value`r`n"
}

Push-Location (Join-Path $root 'deploy')
try{
  $candidateArgs=@('--env-file','.env','-f','docker-compose.core.yml')
  if($WithResearch){$candidateArgs+=@('--profile','research')}
  docker compose @candidateArgs config | Out-Null
  if($LASTEXITCODE -ne 0){throw 'Compose config failed.'}
  docker compose @candidateArgs pull
  if($LASTEXITCODE -ne 0){throw 'Image pull failed.'}

  $settings=Read-EnvFile $envPath
  $imageKeys=@('POSTGRES_IMAGE','N8N_IMAGE')
  if($WithResearch){$imageKeys+=@('CHANGEDETECTION_IMAGE')}
  $locks=@()
  $runtimeText=$envText
  foreach($key in $imageKeys){
    if(-not $settings[$key]){throw "Missing $key in deploy/.env"}
    $source=$settings[$key]
    $digest=Resolve-ImageDigest $source
    $runtimeText=Replace-EnvValue $runtimeText $key $digest
    $locks += [ordered]@{environment_key=$key;source_reference=$source;repo_digest=$digest}
  }
  [IO.File]::WriteAllText($runtimeEnv,$runtimeText,(New-Object Text.UTF8Encoding($false)))
  [ordered]@{
    schema_version=1
    generated_at=(Get-Date).ToString('o')
    source_env='deploy/.env'
    runtime_env='deploy/.env.runtime'
    images=$locks
    public_ingress=false
  } | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 (Join-Path $root 'LOCKED_VERSIONS.json')

  $runtimeArgs=@('--env-file','.env.runtime','-f','docker-compose.core.yml')
  if($WithResearch){$runtimeArgs+=@('--profile','research')}
  docker compose @runtimeArgs config | Out-File -Encoding UTF8 (Join-Path $root 'reports/compose-runtime-pinned.yml')
  if($LASTEXITCODE -ne 0){throw 'Pinned Compose config failed.'}
  docker compose @runtimeArgs up -d
  if($LASTEXITCODE -ne 0){throw 'Startup failed.'}
  docker compose @runtimeArgs ps
  $locks | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $root 'reports/image-digests.json')
}finally{Pop-Location}
Write-Host 'Core services started from deploy/.env.runtime using immutable RepoDigests.'
