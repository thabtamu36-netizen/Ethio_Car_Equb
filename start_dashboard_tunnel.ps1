# start_dashboard_tunnel.ps1
# Script to run the Ethio Car Equb admin dashboard and expose it publicly via Localtunnel.

# Clear screen
Clear-Host

# Resolve absolute paths
$scriptDir = $PSScriptRoot
if ([string]::IsNullOrEmpty($scriptDir)) {
    $scriptDir = Get-Location
}

$pythonPath = Join-Path $scriptDir "venv\Scripts\python.exe"
$workingDir = Join-Path $scriptDir "ethio-car-equb\ethio-car-equb"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "Starting Ethio Car Equb Admin Dashboard & Localtunnel" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# 1. Start the Admin Dashboard
Write-Host "Launching local Admin Dashboard..." -ForegroundColor Yellow
Start-Process -FilePath $pythonPath -ArgumentList "run_dashboard.py" -WorkingDirectory $workingDir -WindowStyle Normal

# 2. Start the Localtunnel
Write-Host "Launching Localtunnel for subdomain 'ethio-car-equb'..." -ForegroundColor Yellow
Start-Process -FilePath "cmd.exe" -ArgumentList "/c npx localtunnel --port 8000 --subdomain ethio-car-equb" -WorkingDirectory $scriptDir -WindowStyle Normal

Write-Host "`nSuccessfully started!" -ForegroundColor Green
Write-Host "Your dashboard is published at: https://ethio-car-equb.loca.lt" -ForegroundColor Green
Write-Host "Please keep both terminal windows open to keep the service online." -ForegroundColor White
Write-Host "====================================================" -ForegroundColor Cyan
