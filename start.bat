@echo off
title AI Hardware Advisor - Can I Run AI?
echo ========================================================
echo         AI Hardware Advisor - Can I Run AI?
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/2] Iniciando Backend FastAPI (Python)...
start "AI Hardware Advisor - Backend" cmd /k "cd backend && python run.py"

echo [2/2] Iniciando Frontend Vue 3 (Vite)...
start "AI Hardware Advisor - Frontend" cmd /k "cd frontend && npm.cmd run dev"

echo.
echo ========================================================
echo Tudo pronto!
echo Backend API: http://127.0.0.1:8000/docs
echo Frontend Web: http://localhost:5173
echo ========================================================
echo.
timeout /t 3 >nul
start http://localhost:5173
