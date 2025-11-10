# Backend Manual Setup Guide

Complete guide to manually set up and run the Laptop Repair Store Management System backend.

## Prerequisites

Before starting, ensure you have:

1. **Python 3.8+** installed
   - Check: `python --version`
   - Download: https://www.python.org/downloads/

2. **MySQL** installed and running
   - Check: MySQL service is running
   - Download: https://dev.mysql.com/downloads/mysql/

3. **Git** (optional, for cloning repository)
   - Download: https://git-scm.com/downloads

## Step-by-Step Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

Create an isolated Python environment:

```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

Activate the virtual environment:

```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

**Note:** After activation, you should see `(venv)` in your terminal prompt.

### Step 4: Upgrade pip and Build Tools

Upgrade pip and install build tools:

```bash
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel
```

### Step 5: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

**If you encounter Rust/Cargo errors with orjson:**
- Option 1: Install Rust from https://rustup.rs/
- Option 2: Install other packages first, then orjson:
  ```bash
  pip install fastapi uvicorn sqlalchemy aiomysql pymysql alembic passlib python-jose python-dotenv pydantic pydantic-settings httpx
  pip install orjson
  ```
- Option 3: Continue without orjson (backend will use standard JSON, slightly slower)

### Step 6: Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=repair
DB_USER=root
DB_PASSWORD=123456

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-12345678
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

**Important:** Update the database credentials to match your MySQL setup.

### Step 7: Create Database

Create the MySQL database:

```sql
CREATE DATABASE repair CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or using MySQL command line:

```bash
mysql -u root -p -e "CREATE DATABASE repair CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### Step 8: Run Database Migrations

Initialize and run Alembic migrations:

```bash
# Create migrations directory if it doesn't exist
mkdir alembic\versions 2>nul || mkdir -p alembic/versions

# Generate initial migration (if needed)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

**If migrations fail:**
- Check MySQL is running
- Verify database exists
- Check database credentials in `.env`
- Check connection: `mysql -u root -p -e "USE repair; SHOW TABLES;"`

### Step 9: Seed Database (Optional)

If you have seed data script:

```bash
python migration/run_seed.py
```

### Step 10: Start the Backend Server

Start the FastAPI development server:

```bash
# Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using Python module
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Server will start on:**
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Verification

### Check Backend is Running

1. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"healthy"}`

2. **API Documentation:**
   Open browser: http://localhost:8000/docs

3. **Test Registration:**
   ```bash
   curl -X POST http://localhost:8000/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"full_name":"Test User","phone":"1234567890","email":"test@example.com","password":"password123"}'
   ```

## Common Issues and Solutions

### Issue 1: Python not found

**Error:** `'python' is not recognized as an internal or external command`

**Solution:**
- Add Python to PATH during installation
- Or use full path: `C:\Python3x\python.exe`
- Or use `py` command: `py -m venv venv`

### Issue 2: Virtual environment activation fails

**Error:** `venv\Scripts\activate : The term 'activate' is not recognized`

**Solution (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### Issue 3: MySQL connection error

**Error:** `Can't connect to MySQL server`

**Solution:**
- Check MySQL service is running
- Verify database credentials in `.env`
- Test connection: `mysql -u root -p`
- Check firewall settings

### Issue 4: Migration errors

**Error:** `Target database is not up to date`

**Solution:**
```bash
# Check current migration version
alembic current

# Upgrade to latest
alembic upgrade head

# If stuck, reset (WARNING: deletes data)
alembic downgrade base
alembic upgrade head
```

### Issue 5: Port 8000 already in use

**Error:** `Address already in use`

**Solution:**
```bash
# Windows: Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --reload --port 8001
```

### Issue 6: Module not found errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check you're using the correct Python: `which python` or `where python`

### Issue 7: orjson/Rust compilation errors

**Error:** `error: subprocess-exited-with-error` (Rust/Cargo related)

**Solution:**
- Install Rust: https://rustup.rs/
- Or skip orjson (backend works without it):
  ```bash
  pip install fastapi uvicorn sqlalchemy aiomysql pymysql alembic passlib python-jose python-dotenv pydantic pydantic-settings httpx
  ```
- Then modify `main.py` to use standard JSON instead of orjson

## Running in Production

### Using Uvicorn with Workers

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn (Linux/Mac)

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker (if available)

```bash
docker build -t laptop-repair-backend .
docker run -p 8000:8000 laptop-repair-backend
```

## Useful Commands

### Database Management

```bash
# Check migration status
alembic current

# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback all migrations
alembic downgrade base
```

### Testing

```bash
# Run API tests
python test_api.py

# Run comprehensive tests
python test_comprehensive.py

# Run store operations tests
python test_store_operations.py
```

### Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt  # if exists

# Run linter
flake8 .  # if installed

# Run type checking
mypy .  # if installed
```

## Project Structure

```
backend/
├── alembic/              # Database migrations
│   ├── versions/         # Migration files
│   ├── env.py           # Alembic configuration
│   └── alembic.ini      # Alembic settings
├── apps/
│   └── api/
│       └── v1/          # API v1 endpoints
│           ├── auth.py
│           ├── users.py
│           ├── devices.py
│           ├── orders.py
│           ├── payments.py
│           └── assigns.py
├── core/
│   └── config.py        # Application settings
├── db/
│   └── __init__.py      # Database connection
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── utils/
│   └── security.py      # JWT and password hashing
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── MANUAL_SETUP.md      # This file
```

## API Endpoints

All API endpoints are prefixed with `/v1`:

- **Authentication:** `/v1/auth/*`
- **Users:** `/v1/users/*`
- **Devices:** `/v1/devices/*`
- **Orders:** `/v1/orders/*`
- **Payments:** `/v1/payments/*`
- **Assigns:** `/v1/assigns/*`

## Next Steps

1. ✅ Backend is running
2. ✅ Test API endpoints using http://localhost:8000/docs
3. ✅ Import Postman collection: `LaptopRepair.json`
4. ✅ Start frontend development
5. ✅ Integrate frontend with backend API

## Support

- **API Documentation:** http://localhost:8000/docs
- **Postman Collection:** `LaptopRepair.json`
- **Full Documentation:** `Readme.md` or `backend/documentation.md`

## Quick Reference

```bash
# Complete setup in one go (after prerequisites)
cd backend
python -m venv venv
venv\Scripts\activate                    # Windows
source venv/bin/activate                 # Linux/Mac
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
# Create .env file with database credentials
# Create database: CREATE DATABASE repair;
alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

**That's it!** Your backend should now be running on http://localhost:8000 🚀

