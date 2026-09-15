# AI Hardware Advisor - Can I Run AI?
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "        AI Hardware Advisor - Can I Run AI?             " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "[1/2] Iniciando Backend FastAPI (Python)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$ScriptDir\backend'; python run.py"

Write-Host "[2/2] Iniciando Frontend Vue 3 (Vite)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$ScriptDir\frontend'; npm.cmd run dev"

Write-Host ""
Write-Host "Tudo pronto!" -ForegroundColor Cyan
Write-Host "Backend API: http://127.0.0.1:8000/docs"
Write-Host "Frontend Web: http://localhost:5173"
Write-Host "========================================================" -ForegroundColor Cyan

Start-Sleep -Seconds 3
Start-Process "http://localhost:5173"
