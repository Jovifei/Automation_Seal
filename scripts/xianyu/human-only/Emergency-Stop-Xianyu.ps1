[CmdletBinding(SupportsShouldProcess=$true,ConfirmImpact='High')]
param([string]$LocalRepoPath='E:\project\xianyu-auto-reply')
$ErrorActionPreference='Stop'
if(-not (Test-Path $LocalRepoPath)){throw 'Local Xianyu repo not found.'}
if($PSCmdlet.ShouldProcess($LocalRepoPath,'Stop Xianyu Docker Compose services without deleting volumes')){
  Push-Location $LocalRepoPath
  try{docker compose stop;if($LASTEXITCODE -ne 0){throw 'docker compose stop failed.'}}
  finally{Pop-Location}
}
