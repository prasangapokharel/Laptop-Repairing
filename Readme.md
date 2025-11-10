# Laptop Repair Store Management System

## Quick Start - Backend

### Easiest Way: Use start.bat

1. **Navigate to frontend folder:**
   ```bash
   cd frontend
   ```

2. **Double-click `start.bat`** or run:
   ```bash
   start.bat
   ```

That's it! The backend server will start on **http://localhost:8000**

### What start.bat does:
- Changes to backend directory
- Starts FastAPI server with auto-reload
- Server runs on: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## Prerequisites (First Time Setup)

Before running `start.bat` for the first time, ensure:

1. **Python 3.8+** is installed
   - Check: `python --version`
   - Download: https://www.python.org/downloads/

2. **MySQL** is installed and running
   - Check: MySQL service is running
   - Download: https://dev.mysql.com/downloads/mysql/

3. **Backend is set up:**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate          # Windows
   source venv/bin/activate         # Linux/Mac
   pip install -r requirements.txt
   ```

4. **Database is created:**
   ```sql
   CREATE DATABASE repair CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Environment variables are set:**
   Create `backend/.env` file:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=repair
   DB_USER=root
   DB_PASSWORD=123456
   JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-12345678
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24
   ```

6. **Migrations are run:**
   ```bash
   cd backend
   alembic upgrade head
   ```

---

## Manual Setup (Detailed Guide)

For detailed step-by-step instructions, see:
- **Backend Manual Setup:** `backend/MANUAL_SETUP.md`
- **Full API Documentation:** `backend/documentation.md`

---

## API Endpoints

All API endpoints are prefixed with `/v1`:

- **Base URL:** http://localhost:8000
- **API Version:** v1
- **Full API URL:** http://localhost:8000/v1

### Endpoints:
- **Authentication:** `/v1/auth/*`
- **Users:** `/v1/users/*`
- **Devices:** `/v1/devices/*`
- **Orders:** `/v1/orders/*`
- **Payments:** `/v1/payments/*`
- **Assigns:** `/v1/assigns/*`

---

## Testing

### Test API Endpoints:
```bash
cd backend
python test_api.py
```

### Comprehensive Tests:
```bash
python test_comprehensive.py
python test_store_operations.py
```

---

## Postman Collection

Import `LaptopRepair.json` into Postman for easy API testing.

---

## Support

- **API Documentation:** http://localhost:8000/docs
- **Backend Setup Guide:** `backend/MANUAL_SETUP.md`
- **API Documentation:** `backend/documentation.md`
- **Postman Collection:** `LaptopRepair.json`

---

## Quick Reference

```bash
# Start backend (easiest way)
cd frontend
start.bat

# Or manually
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

**That's it!** Simple and easy to get started! 🚀

