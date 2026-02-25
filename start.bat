@echo off
echo ============================================
echo   TaskMaster - Quick Start (Dependencies Already Installed)
echo ============================================
echo.

REM Check if we're in the right directory
if not exist "backend\main.py" (
    echo ERROR: Please run this script from the project root directory
    exit /b 1
)

echo [1/2] Starting backend server...
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.

REM Start backend in a new window
start "TaskMaster Backend" cmd /k "cd backend && call venv\Scripts\activate.bat && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
echo Waiting for backend to start (5 seconds)...
timeout /t 5 /nobreak >nul

echo.
echo [2/2] Starting frontend development server...
echo Frontend will be available at: http://localhost:3000
echo.

REM Start frontend in a new window
start "TaskMaster Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================
echo   Development servers starting...
echo ============================================
echo.
echo Backend:  http://localhost:8000 (in separate window)
echo Frontend: http://localhost:3000 (in separate window)
echo API Documentation: http://localhost:8000/docs
echo.
echo To stop the servers, close the separate windows
echo ============================================
