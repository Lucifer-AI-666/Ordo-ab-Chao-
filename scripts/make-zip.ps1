# Crea un archivio zip della cartella del progetto, escludendo artefatti e cache.
# Uso:
#   powershell -ExecutionPolicy Bypass -File scripts\make-zip.ps1
# Output:
#   priv-cyber-agents-YYYYmmddHHMM.zip (nella directory superiore)

$ErrorActionPreference = "Stop"

# Root repo (script in scripts/)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Resolve-Path (Join-Path $scriptDir "..")
Set-Location $root

$stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddHHmm")
$out = Join-Path (Split-Path $root -Parent) ("priv-cyber-agents-$stamp.zip")

# Pattern da escludere
$excludeRegex = [regex]'\\\.git\\|\\logs\\|\\\.venv\\|\\venv\\|\\dist\\|\\build\\|\\\.gradle\\|android-app\\app\\build\\|\\\.DS_Store$|\\Thumbs\.db$'

# Raccoglie i file da includere
$files = Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch $excludeRegex }

# Crea zip
if (Test-Path $out) { Remove-Item $out -Force }
Compress-Archive -Path $files.FullName -DestinationPath $out
Write-Host "[ok] Creato: $out"