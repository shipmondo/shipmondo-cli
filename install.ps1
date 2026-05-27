Write-Host "📦 Starting Shipmondo CLI Installation for Windows..." -ForegroundColor Green

# 1. Ensure Python is installed
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Python is required but was not found." -ForegroundColor Red
    Write-Host "Please install Python from python.org or the Microsoft Store." -ForegroundColor Yellow
    exit 1
}

# 2. Check and provision pipx
if (-not (Get-Command "pipx" -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️ pipx not found. Installing pipx globally via Python..." -ForegroundColor Yellow
    python -m pip install --user pipx
    
    Write-Host "⚙️ Ensuring pipx environment PATH hooks are configured..." -ForegroundColor Green
    python -m pipx ensurepath
    
    # Reload Path environment variable for the current session so pipx works immediately
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 3. Perform the isolated app installation
Write-Host "🚀 Installing shipmondo-cli in an isolated environment via pipx..." -ForegroundColor Green
pipx install "git+https://github.com/shipmondo/shipmondo-cli.git" --force

Write-Host "✅ Shipmondo CLI successfully installed!" -ForegroundColor Green
Write-Host "Note: You may need to restart your PowerShell window if the 'shipmondo' command is not recognized immediately."
Write-Host "Try running: shipmondo commands --json" -ForegroundColor Yellow
