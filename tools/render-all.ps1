<#
  render-all.ps1 — render EVERY composition (.html) in a project, each to its
  own verified MOV. Use for "a folder of different clips, each with its own text".

  USAGE (from project root):
    tools\render-all.ps1 podcast
    tools\render-all.ps1 podcast -Fps 30

  Renders every projects\<Project>\compositions\*.html -> projects\<Project>\renders\<name>.mov
#>
param(
  [Parameter(Mandatory=$true, Position=0)][string]$Project,
  [int]$Fps = 30
)
$ErrorActionPreference = "Stop"
$compDir = "projects\$Project\compositions"
if (-not (Test-Path $compDir)) { Write-Host "ERROR: $compDir not found." -ForegroundColor Red; exit 1 }

$files = Get-ChildItem "$compDir\*.html" | Where-Object { $_.Name -notlike "_*" }
if (-not $files) { Write-Host "No compositions found in $compDir." -ForegroundColor Yellow; exit 0 }

Write-Host "Rendering $($files.Count) composition(s) in project '$Project'..." -ForegroundColor Cyan
foreach ($f in $files) {
  $name = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
  Write-Host "`n----- $name -----" -ForegroundColor Cyan
  & "$PSScriptRoot\render.ps1" $Project $name -Fps $Fps
}
Write-Host "`nAll done. Outputs in projects\$Project\renders\" -ForegroundColor Green
