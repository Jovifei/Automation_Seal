[CmdletBinding()]
param()
$ErrorActionPreference='Continue'
$root=Split-Path -Parent $PSScriptRoot
$envPath=Join-Path $root 'deploy/.env.runtime'
if(-not (Test-Path $envPath)){$envPath=Join-Path $root 'deploy/.env'}
$settings=@{}
if(Test-Path $envPath){
  Get-Content $envPath | Where-Object {$_ -match '^[A-Z0-9_]+='} | ForEach-Object {$k,$v=$_.Split('=',2);$settings[$k]=$v}
}
$n8nPort=if($settings.N8N_PORT){[int]$settings.N8N_PORT}else{5678}
$changePort=if($settings.CHANGEDETECTION_PORT){[int]$settings.CHANGEDETECTION_PORT}else{5000}
$failed=0
$checks=@(
  @{name='n8n';url="http://127.0.0.1:$n8nPort/healthz";required=$true},
  @{name='changedetection';url="http://127.0.0.1:$changePort";required=$false}
)
foreach($item in $checks){
  try{
    $response=Invoke-WebRequest -UseBasicParsing -TimeoutSec 10 -Uri $item.url
    Write-Host "[PASS] $($item.name) HTTP $($response.StatusCode)"
  } catch {
    if($item.required){Write-Host "[FAIL] $($item.name) $($_.Exception.Message)";$failed++}
    else{Write-Host "[INFO] optional $($item.name) unavailable"}
  }
}
try{
  docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
  $public=docker ps --format '{{.Names}}|{{.Ports}}' | Select-String '0\.0\.0\.0:|\[::\]:'
  if($public){Write-Host '[FAIL] Public binding detected:';$public;$failed++}
  else{Write-Host '[PASS] No public Docker port binding detected'}
}catch{Write-Host '[FAIL] Docker status unavailable';$failed++}
if($failed){exit 2}
