@echo off
echo ========================================
echo Laptop Repair Store Management System
echo Starting Backend and Frontend...
echo ========================================
echo.

REM Change to backend directory
cd ..\backend

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)
echo OK: Python found
echo.

echo [2/4] Checking virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo OK: Virtual environment created
) else (
    echo OK: Virtual environment exists
)
echo.

echo [3/4] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo OK: Dependencies installed
echo.

echo [4/4] Running database migrations...
python -m alembic upgrade head
if errorlevel 1 (
    echo WARNING: Migration failed, trying to initialize...
    python -m alembic revision --autogenerate -m "Initial migration"
    python -m alembic upgrade head
)
echo OK: Database migrations completed
echo.

echo [5/5] Seeding database (if needed)...
if exist "migration\run_seed.py" (
    python migration\run_seed.py
    echo OK: Database seeded
)
echo.

echo ========================================
echo Starting Backend Server...
echo Backend will run on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo ========================================
echo.

REM Start backend in a new window
start "Backend Server" cmd /k "venv\Scripts\activate.bat && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Change back to frontend directory
cd ..\frontend

echo ========================================
echo Starting Frontend Server...
echo Frontend will run on: http://localhost:3000
echo ========================================
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install frontend dependencies
        pause
        exit /b 1
    )
    echo OK: Frontend dependencies installed
    echo.
)

REM Start frontend
echo Starting Next.js development server...
call npm run dev

pause

