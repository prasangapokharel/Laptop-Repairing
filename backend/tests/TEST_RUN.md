# Test Run Guide

## Environment Setup

### 1. Create `.env` file in `backend/` directory:

```env
# API Configuration (NO /v1 here!)
BASE_URL=http://localhost:8000

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
```

**Important:** `BASE_URL` should NOT include `/v1` - it will be added automatically in the code.

## Running All Tests

### Step 1: Start Backend Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Run All Tests

In a new terminal:

```bash
cd backend

# Run 45+ customer test (Real-world scenario)
python tests/test_45_customers.py

# Run all tables test
python tests/test_all_tables.py

# Run comprehensive test
python tests/test_comprehensive.py

# Run store operations test
python tests/test_store_operations.py

# Run basic API test
python tests/test_api.py
```

## Test Files Summary

1. **test_45_customers.py** - 45+ customers with different device issues
2. **test_all_tables.py** - Tests all 14 database tables
3. **test_comprehensive.py** - 16 repair office scenarios
4. **test_store_operations.py** - 12 store operation scenarios
5. **test_api.py** - Basic API endpoint tests

## How Tests Work

All tests:
- Load `BASE_URL` from `.env` file (without `/v1`)
- Automatically add `/v1` prefix to all API calls
- Use `api_url` variable: `f"{self.api_url}/auth/login"`
- Handle connection timeouts (10 seconds)
- Provide clear error messages

## Expected Results

All tests should pass with **100% success rate** when:
- ✅ Backend server is running on http://localhost:8000
- ✅ Database is properly seeded
- ✅ All migrations are applied
- ✅ `.env` file is configured correctly

## Troubleshooting

### Connection Timeout
- Ensure backend server is running
- Check `BASE_URL` in `.env` file
- Verify server is accessible: `curl http://localhost:8000/health`

### Environment Variable Not Found
- Ensure `.env` file exists in `backend/` directory
- Check file name is exactly `.env` (not `.env.local` or `.env.example`)
- Verify `BASE_URL` is set without `/v1`

### Import Errors
- Ensure you're in `backend/` directory when running tests
- Install dependencies: `pip install -r requirements.txt`
- Check `python-dotenv` is installed

