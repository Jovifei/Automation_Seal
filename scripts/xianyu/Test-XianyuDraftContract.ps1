[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$out=Join-Path $root 'reports/xianyu/x2/synthetic-bundle'
if(Test-Path $out){Remove-Item -Recurse -Force $out}
python (Join-Path $PSScriptRoot 'new_xianyu_draft_bundle.py') --input (Join-Path $root 'deploy/xianyu/synthetic_product_input.example.json') --output-dir $out
python (Join-Path $PSScriptRoot 'validate_xianyu_bundle.py') --bundle (Join-Path $out 'bundle.json')
if($LASTEXITCODE -ne 0){throw 'Synthetic bundle validation failed.'}
$packageHash=(Get-Content (Join-Path $out 'package.sha256.txt') -Raw).Trim()
Write-Host "Synthetic X2 contract passed: $out"
Write-Host "Package manifest SHA256: $packageHash"
