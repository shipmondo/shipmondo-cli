# Shipmondo CLI installer (Windows PowerShell).
# Downloads a single self-contained .exe from GitHub Releases.
# Zero runtime dependencies.

$ErrorActionPreference = "Stop"
$repo = "shipmondo/shipmondo-cli"

Write-Host "📦 Installing the Shipmondo CLI..." -ForegroundColor Green

# Detect architecture.
$arch = if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") { "arm64" } else { "amd64" }
$asset = "shipmondo-windows-$arch.exe"
$url = "https://github.com/$repo/releases/latest/download/$asset"

# Install into a per-user directory and ensure it is on PATH.
$installDir = Join-Path $env:LOCALAPPDATA "Shipmondo"
New-Item -ItemType Directory -Force -Path $installDir | Out-Null
$target = Join-Path $installDir "shipmondo.exe"

Write-Host "⬇️  Downloading $asset..." -ForegroundColor Green
Invoke-WebRequest -Uri $url -OutFile $target -UseBasicParsing

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$installDir", "User")
    $env:Path = "$env:Path;$installDir"
    Write-Host "⚙️  Added $installDir to your user PATH." -ForegroundColor Green
}

Write-Host "✅ Shipmondo CLI installed to $target" -ForegroundColor Green
Write-Host "Note: restart your PowerShell window if 'shipmondo' is not recognized immediately."
Write-Host "Try running: shipmondo commands" -ForegroundColor Yellow
