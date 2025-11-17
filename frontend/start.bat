@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Starting Backend Server
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Change to backend directory
cd /d "%~dp0..\backend"
if not exist "main.py" (
    echo [ERROR] Backend directory not found or invalid
    echo Please run this script from frontend directory
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first from the root directory.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if .env exists, create from .env.development if needed
if not exist ".env" (
    echo [WARNING] .env file not found!
    if exist ".env.development" (
        echo [INFO] Creating .env from .env.development...
        copy ".env.development" ".env" >nul
        if errorlevel 1 (
            echo [ERROR] Failed to create .env file
            pause
            exit /b 1
        )
        echo [OK] .env file created
    ) else (
        echo [ERROR] .env.development not found!
        echo Please create .env file with database credentials
        pause
        exit /b 1
    )
)

REM Run migrations and seeding if needed
echo [INFO] Checking database migrations...
python migration\run_all.py
if errorlevel 1 (
    echo.
    echo [ERROR] Migration or seeding failed!
    echo.
    echo Troubleshooting:
    echo   1. Check if MySQL is running
    echo   2. Verify database credentials in .env file
    echo   3. Ensure database 'repair' exists
    echo   4. Check database connection: mysql -u root -p
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting FastAPI Server
echo ========================================
echo.
echo Server: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start server
    echo Please check if port 8000 is available
    pause
    exit /b 1
)

pause
