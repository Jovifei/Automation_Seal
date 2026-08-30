[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][string]$BundlePath,
 [Parameter(Mandatory=$true)][ValidatePattern('^[a-fA-F0-9]{64}$')][string]$ExpectedSha256,
 [Parameter(Mandatory=$true)][string]$Approver
)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$resolved=(Resolve-Path $BundlePath).Path
if((Get-Item $resolved).PSIsContainer){$packageDir=$resolved}else{$packageDir=Split-Path -Parent $resolved}
$bundle=Join-Path $packageDir 'bundle.json'
$manifestPath=Join-Path $packageDir 'manifest.sha256.json'
$packageHashPath=Join-Path $packageDir 'package.sha256.txt'
foreach($required in @($bundle,$manifestPath,$packageHashPath)){if(-not (Test-Path $required)){throw "Missing package file: $required"}}

$current=(Get-FileHash -Algorithm SHA256 $manifestPath).Hash.ToLowerInvariant()
$declared=(Get-Content $packageHashPath -Raw).Trim().ToLowerInvariant()
if($current -ne $declared){throw 'Package manifest hash does not match package.sha256.txt.'}
if($current -ne $ExpectedSha256.ToLowerInvariant()){throw 'Expected package SHA256 mismatch.'}

$manifest=Get-Content $manifestPath -Raw | ConvertFrom-Json
$listed=@()
foreach($item in $manifest.files){
  $relative=[string]$item.path
  if($relative -match '(^[\\/]|\.\.)'){throw "Unsafe manifest path: $relative"}
  $target=Join-Path $packageDir $relative
  if(-not (Test-Path $target -PathType Leaf)){throw "Manifest file missing: $relative"}
  $hash=(Get-FileHash -Algorithm SHA256 $target).Hash.ToLowerInvariant()
  if($hash -ne ([string]$item.sha256).ToLowerInvariant()){throw "Manifest file changed: $relative"}
  if((Get-Item $target).Length -ne [long]$item.size){throw "Manifest size changed: $relative"}
  $listed += (Resolve-Path $target).Path
}
$allowed=@((Resolve-Path $manifestPath).Path,(Resolve-Path $packageHashPath).Path)
$bundleHashPath=Join-Path $packageDir 'bundle.sha256.txt'
if(Test-Path $bundleHashPath){$allowed+=(Resolve-Path $bundleHashPath).Path}
$extras=Get-ChildItem -Recurse -File $packageDir | Where-Object {$_.FullName -notin ($listed+$allowed)}
if($extras){throw ('Unlisted files exist in candidate package: '+(($extras.FullName) -join ', '))}

$data=Get-Content $bundle -Raw | ConvertFrom-Json
if($data.rights.status -notin @('ORIGINAL','VERIFIED_LICENSE')){throw 'Rights status is not approvable.'}
foreach($name in @('publish','send_message','deliver','change_price','refund')){if($data.external_actions.$name -ne $false){throw "External action $name must be false."}}
if($data.approval.status -ne 'PENDING'){throw 'Approval must remain separate from the bundle.'}

$code=Read-Host 'Type first 16 package-hash characters to approve manual import package'
if($code.Trim().ToLowerInvariant() -ne $current.Substring(0,16)){throw 'Approval code mismatch.'}
$outDir=Join-Path $root 'workspace/approvals/xianyu'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$out=Join-Path $outDir "$($data.bundle_id).approval.json"
if(Test-Path $out){throw 'Approval already exists; create a new immutable candidate version instead.'}
[ordered]@{schema_version=1;bundle_id=$data.bundle_id;package_dir=$packageDir;manifest_sha256=$current;approver=$Approver;approved_at=(Get-Date).ToString('o');scope='manual_import_only'} | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $out
Write-Host "Approval written: $out"
