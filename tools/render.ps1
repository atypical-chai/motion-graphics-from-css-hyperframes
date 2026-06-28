<#
  render.ps1 — render ONE composition from a project to ProRes 4444 MOV
  (+ optional WebM), then AUTO-VERIFY the alpha channel with real pixels.

  USAGE (from the project root):
    tools\render.ps1 podcast chapter-break-b           # MOV only (60fps default)
    tools\render.ps1 podcast chapter-break-b -WebM     # MOV + WebM
    tools\render.ps1 podcast chapter-break-b -Fps 30   # override to 30fps if ever needed

  Renders: projects\<Project>\compositions\<Name>.html
        -> projects\<Project>\renders\<Name>.mov
#>
param(
  [Parameter(Mandatory=$true, Position=0)][string]$Project,
  [Parameter(Mandatory=$true, Position=1)][string]$Name,
  [switch]$WebM,
  [int]$Fps = 60,   # default: every render is 60fps unless overridden
  [string]$OutDir = ""    # optional: override the output folder (e.g. a 60fps subfolder)
)
$ErrorActionPreference = "Stop"
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

$comp    = "projects\$Project\compositions\$Name.html"
$rendDir = if ($OutDir) { $OutDir } else { "projects\$Project\renders" }
if (-not (Test-Path $comp)) {
  Write-Host "ERROR: $comp not found. Available in this project:" -ForegroundColor Red
  Get-ChildItem "projects\$Project\compositions\*.html" -ErrorAction SilentlyContinue | Select-Object Name
  exit 1
}
New-Item -ItemType Directory -Force -Path $rendDir | Out-Null
$mov = "$rendDir\$Name.mov"

Write-Host "`n=== Rendering MOV (ProRes 4444 + alpha) -> $mov ===" -ForegroundColor Cyan
npx hyperframes render -c $comp --format mov --fps $Fps --output $mov

if ($WebM) {
  $webm = "$rendDir\$Name.webm"
  Write-Host "`n=== Rendering WebM (VP9 + alpha) -> $webm ===" -ForegroundColor Cyan
  npx hyperframes render -c $comp --format webm --fps $Fps --output $webm
}

Write-Host "`n=== Verifying alpha (real pixels, not exit code) ===" -ForegroundColor Cyan
python3 tools\verify_alpha.py $mov
$movOk = $LASTEXITCODE
if ($WebM) { python3 tools\verify_alpha.py "$rendDir\$Name.webm" }

if ($movOk -eq 0) { Write-Host "`nDONE. Open $mov to gut-check, then drag into Premiere." -ForegroundColor Green }
else { Write-Host "`nALPHA CHECK FAILED - inspect the composition before using this file." -ForegroundColor Yellow }
