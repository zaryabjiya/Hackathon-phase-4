@echo off
REM Database Setup Script for Windows
REM This script helps you set up a local PostgreSQL database

echo ============================================
echo TaskMaster Database Setup Script
echo ============================================
echo.

REM Check if PostgreSQL is installed
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PostgreSQL is not installed or not in PATH.
    echo.
    echo Please install PostgreSQL from:
    echo https://www.postgresql.org/download/windows/
    echo.
    echo OR use a cloud database service like:
    echo - Neon: https://neon.tech
    echo - Supabase: https://supabase.com
    echo.
    echo After getting a database connection string, update backend\.env
    echo with your DATABASE_URL.
    echo.
    pause
    exit /b 1
)

echo PostgreSQL found. Setting up database...
echo.

REM Create database
echo Creating database 'todo_app'...
psql -U postgres -c "CREATE DATABASE todo_app;" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Database created successfully!
) else (
    echo Database may already exist or there was an error.
    echo Continuing...
)

echo.
echo Setting up password for postgres user...
psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'password';" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Password set successfully!
) else (
    echo Password may already be set or there was an error.
)

echo.
echo ============================================
echo Database setup complete!
echo ============================================
echo.
echo Your database connection string is:
echo postgresql+asyncpg://postgres:password@localhost:5432/todo_app
echo.
echo This is already configured in backend\.env
echo.
echo Next steps:
echo 1. cd backend
echo 2. python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo 3. In another terminal: cd frontend
echo 4. npm run dev
echo.
pause
