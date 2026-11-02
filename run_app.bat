@echo off
setlocal
echo ============================================================
echo Starting Student Placement Prediction System (Full-Stack)
echo SRM Institute of Science and Technology
echo ============================================================

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PY_CMD=py -3.12
) else (
    set PY_CMD=python
)

where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] npm is not found in PATH. Please install Node.js (v18+) to run the frontend.
    pause
    exit /b 1
)

echo.
echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "Placement Backend (FastAPI)" cmd /k "%PY_CMD% -m uvicorn api.app:app --host 127.0.0.1 --port 8000"

echo.
echo [2/2] Starting React Frontend on http://127.0.0.1:5173 ...
cd frontend
start "Placement Frontend (Vite)" cmd /k "npm run dev -- --host 127.0.0.1 --port 5173"
cd ..

echo.
echo Waiting 3 seconds for servers to initialize...
timeout /t 3 /nobreak >nul

echo.
echo Opening browser at http://127.0.0.1:5173 ...
start http://127.0.0.1:5173

echo.
echo ============================================================
echo Application is running!
echo - Frontend UI:  http://127.0.0.1:5173
echo - Backend API:  http://127.0.0.1:8000
echo - Swagger Docs: http://127.0.0.1:8000/docs
echo Close the respective server terminal windows to stop.
echo ============================================================

