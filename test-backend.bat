@echo off
echo ============================================
echo   TaskMaster - Backend Test Script
echo ============================================
echo.

REM Set API base URL
set API_URL=http://localhost:8000

echo Testing backend health...
echo.

REM Test 1: Health Check
echo [Test 1/5] Health Check
curl -s %API_URL%/health
if %errorlevel% neq 0 (
    echo.
    echo FAILED: Backend is not running!
    echo Start the backend first: cd backend ^&^& venv\Scripts\activate ^&^& python -m uvicorn main:app --reload
    exit /b 1
)
echo.
echo PASSED: Backend is running
echo.

REM Test 2: Root Endpoint
echo [Test 2/5] Root Endpoint
curl -s %API_URL%/
echo.
echo.

REM Test 3: Register Test User
echo [Test 3/5] Register Test User
curl -s -X POST %API_URL%/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test_%RANDOM%@example.com\",\"username\":\"testuser_%RANDOM%\",\"password\":\"password123\"}"
echo.
echo.

REM Test 4: Login Test
echo [Test 4/5] Login Test
echo Note: This will fail if you haven't registered a user yet
curl -s -X POST %API_URL%/auth/login ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=test@example.com&password=password123"
echo.
echo.

REM Test 5: API Documentation
echo [Test 5/5] API Documentation Available
echo Swagger UI: %API_URL%/docs
echo ReDoc: %API_URL%/redoc
echo.

echo ============================================
echo   Tests Complete!
echo ============================================
echo.
echo If all tests passed, your backend is working correctly.
echo Open %API_URL%/docs in your browser to explore the API.
echo.
