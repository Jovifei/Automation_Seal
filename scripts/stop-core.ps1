[CmdletBinding()]
param([switch]$WithResearch)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$envName=if(Test-Path (Join-Path $root 'deploy/.env.runtime')){'.env.runtime'}else{'.env'}
Push-Location (Join-Path $root 'deploy')
try{
  $args=@('--env-file',$envName,'-f','docker-compose.core.yml')
  if($WithResearch){$args+=@('--profile','research')}
  docker compose @args stop
  if($LASTEXITCODE -ne 0){throw 'Core service stop failed.'}
}finally{Pop-Location}
