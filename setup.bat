@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Laptop Repair Store - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Navigate to backend directory
if not exist "backend" (
    echo [ERROR] Backend directory not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip, setuptools, and wheel
echo [INFO] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel --quiet
echo [OK] Build tools upgraded
echo.

REM Install requirements
echo [INFO] Installing requirements...
echo [NOTE] This may take a few minutes...
echo [NOTE] FastAPI will install pydantic automatically...
pip install -r requirements.txt --no-cache-dir
if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    pause
    exit /b 1
)
echo [OK] Requirements installed successfully
echo.

REM Create .env.development file
echo [INFO] Creating .env.development file...
(
echo BASE_URL=http://localhost:8000
echo.
echo # =================================================================
echo # Database Configuration
echo # =================================================================
echo DB_HOST=localhost
echo DB_PORT=3306
echo DB_NAME=repair
echo DB_USER=root
echo DB_PASSWORD=123456
echo.
echo # =================================================================
echo # JWT Configuration
echo # =================================================================
echo JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-12345678
echo JWT_ALGORITHM=HS256
echo JWT_EXPIRATION_HOURS=24
) > .env.development

echo [OK] .env.development file created
echo.

REM Check if .env exists, if not copy from .env.development
if not exist ".env" (
    echo [INFO] Creating .env file from .env.development...
    copy ".env.development" ".env" >nul
    echo [OK] .env file created
    echo.
)

echo ========================================
echo Setup Completed Successfully!
echo ========================================
echo.
echo Next steps:
echo   1. Update .env file with your database credentials
echo   2. Create database: CREATE DATABASE repair;
echo   3. Run migrations: python migration\run_all.py
echo   4. Start server: uvicorn main:app --reload
echo   5. Or use: frontend\start.bat
echo.

pause

