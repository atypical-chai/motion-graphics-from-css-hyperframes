<#
  render-batch.ps1 — render ONE parameterized composition many times, once per
  row in a project's JSON file. Same design, different text. Each output is
  alpha-verified.

  USAGE (from project root):
    tools\render-batch.ps1 podcast chapter-break chapter-breaks
    tools\render-batch.ps1 podcast chapter-break chapter-breaks.json   (.json optional)

  Reads : projects\<Project>\compositions\<Name>.html
          projects\<Project>\batch\<Batch>.json
  Writes: projects\<Project>\renders\<row.out>.mov  (one per row)

  JSON shape: an array of rows. Each row needs an "out" (output file name, no
  extension) plus one key per variable declared in the composition. Example:
    [ { "out": "ch-03", "num": "03", "title": "PAYING THE VENDOR" }, ... ]
#>
param(
  [Parameter(Mandatory=$true, Position=0)][string]$Project,
  [Parameter(Mandatory=$true, Position=1)][string]$Name,
  [Parameter(Mandatory=$true, Position=2)][string]$Batch,
  [int]$Fps = 30
)
$ErrorActionPreference = "Stop"
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

if ($Batch -notlike "*.json") { $Batch = "$Batch.json" }
$comp     = "projects\$Project\compositions\$Name.html"
$batchPath= "projects\$Project\batch\$Batch"
$rendDir  = "projects\$Project\renders"
if (-not (Test-Path $comp))      { Write-Host "ERROR: $comp not found." -ForegroundColor Red; exit 1 }
if (-not (Test-Path $batchPath)) { Write-Host "ERROR: $batchPath not found." -ForegroundColor Red; exit 1 }
New-Item -ItemType Directory -Force -Path $rendDir | Out-Null

$rows = Get-Content $batchPath -Raw | ConvertFrom-Json
$pass = 0; $fail = 0; $i = 0
$tmp = Join-Path $env:TEMP "_hf_vars.json"
foreach ($row in $rows) {
  $i++
  $out = "$rendDir\$($row.out).mov"
  # Everything except "out" becomes the variables object. Write it to a temp
  # file (BOM-less) and pass --variables-file: PowerShell mangles inline JSON
  # quotes for native commands, and Set-Content's UTF-8 BOM breaks the parser.
  $vars = $row | Select-Object -Property * -ExcludeProperty out
  $json = $vars | ConvertTo-Json -Compress
  [System.IO.File]::WriteAllText($tmp, $json, (New-Object System.Text.UTF8Encoding $false))

  Write-Host "`n[$i/$($rows.Count)] Rendering '$($row.out)'  vars=$json" -ForegroundColor Cyan
  npx hyperframes render -c $comp --format mov --fps $Fps --variables-file $tmp --output $out

  python3 tools\verify_alpha.py $out
  if ($LASTEXITCODE -eq 0) { $pass++ } else { $fail++; Write-Host "  ^ check FAILED for $out" -ForegroundColor Yellow }
}
Write-Host "`n==== Batch done: $pass passed, $fail failed (of $($rows.Count)) ====" -ForegroundColor Green
Write-Host "Outputs in $rendDir - drag the .mov files into Premiere."
