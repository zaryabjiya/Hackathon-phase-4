@echo off
echo ============================================
echo   TaskMaster - Development Startup Script
echo ============================================
echo.

REM Check if we're in the right directory
if not exist "backend\main.py" (
    echo ERROR: Please run this script from the project root directory
    echo Current directory: %CD%
    exit /b 1
)

echo [1/4] Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install backend dependencies
echo Installing backend dependencies...
pip install -r requirements.txt -q

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: backend\.env file not found!
    echo Creating from .env.example...
    if exist ".env.example" (
        copy .env.example .env
        echo Please edit backend\.env with your database credentials
        echo.
        pause
    ) else (
        echo ERROR: backend\.env.example not found either!
        exit /b 1
    )
)

cd ..

echo.
echo [2/4] Setting up frontend...
cd frontend

REM Install frontend dependencies
echo Installing frontend dependencies...
call npm install

REM Check if .env.local exists
if not exist ".env.local" (
    echo.
    echo WARNING: frontend\.env.local file not found!
    echo Creating from .env.example...
    if exist "..\.env.example" (
        copy ..\.env.example .env.local
    )
)

cd ..

echo.
echo [3/4] Starting backend server...
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.

REM Start backend in a new window
start "TaskMaster Backend" cmd /k "cd backend && call venv\Scripts\activate.bat && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
echo Waiting for backend to start (10 seconds)...
timeout /t 10 /nobreak >nul

echo.
echo [4/4] Starting frontend development server...
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
echo.
echo API Documentation: http://localhost:8000/docs
echo.
echo To stop the servers, close the separate windows
echo ============================================
echo.
