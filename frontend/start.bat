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

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install build tools for packages that need compilation
echo Installing build tools...
python -m pip install --upgrade setuptools wheel --quiet

REM Install dependencies (orjson may require Rust, but has pre-built wheels for Windows)
echo Installing dependencies...
python -m pip install -r requirements.txt --quiet --only-binary :all:
if errorlevel 1 (
    echo WARNING: Failed with binary-only, trying with source builds...
    python -m pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo WARNING: Some packages failed, trying orjson separately...
        python -m pip install fastapi uvicorn sqlalchemy aiomysql pymysql alembic passlib python-jose python-dotenv pydantic pydantic-settings httpx --quiet
        python -m pip install orjson --quiet || echo WARNING: orjson failed, will use standard json
        if errorlevel 1 (
            echo ERROR: Critical dependencies failed to install
            echo.
            echo TIP: If you see Rust/Cargo errors for orjson:
            echo 1. Install Rust from https://rustup.rs/
            echo 2. Or use standard JSON (orjson is optional for performance)
            echo 3. Or install manually: pip install -r requirements.txt
            pause
            exit /b 1
        )
    )
)
echo OK: Dependencies installed
echo.

echo [4/4] Running database migrations...
python -m alembic upgrade head
if errorlevel 1 (
    echo WARNING: Migration failed, checking database connection...
    echo Trying to initialize migrations...
    if not exist "alembic\versions" (
        mkdir alembic\versions
    )
    python -m alembic revision --autogenerate -m "Initial migration" 2>nul
    python -m alembic upgrade head
    if errorlevel 1 (
        echo ERROR: Database migration failed
        echo Please check:
        echo 1. MySQL is running
        echo 2. Database 'repair' exists
        echo 3. Database credentials in .env file are correct
        echo.
        echo You can skip migrations and start the server anyway
        echo Press any key to continue anyway, or Ctrl+C to exit...
        pause
    ) else (
        echo OK: Database migrations completed
    )
) else (
    echo OK: Database migrations completed
)
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

