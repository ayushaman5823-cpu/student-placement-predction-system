Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting Student Placement Prediction System (Full-Stack)" -ForegroundColor Green
Write-Host "SRM Institute of Science and Technology" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$pyCmd = "python"
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pyCmd = "py -3.12"
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] npm is not installed or not in PATH. Please install Node.js (v18+)." -ForegroundColor Red
    exit 1
}

Write-Host "`n[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k $pyCmd -m uvicorn api.app:app --host 127.0.0.1 --port 8000" -WindowStyle Normal

Write-Host "`n[2/2] Starting React Frontend on http://127.0.0.1:5173 ..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"
Start-Process cmd -ArgumentList "/k cd /d `"$frontendPath`" && npm run dev -- --host 127.0.0.1 --port 5173" -WindowStyle Normal

Start-Sleep -Seconds 3
Start-Process "http://127.0.0.1:5173"

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "Full-Stack System Launched Successfully!" -ForegroundColor Green
Write-Host "- Frontend UI:  http://127.0.0.1:5173" -ForegroundColor White
Write-Host "- Backend API:  http://127.0.0.1:8000" -ForegroundColor White
Write-Host "- Swagger Docs: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan

