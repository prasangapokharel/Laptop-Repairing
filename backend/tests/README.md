# Test Suite

All test files are organized in this directory for better project structure.

## Test Files

1. **test_all_tables.py** - Comprehensive test suite that tests ALL 14 database tables
2. **test_api.py** - Basic API endpoint tests
3. **test_comprehensive.py** - Comprehensive repair office scenarios (16 scenarios)
4. **test_store_operations.py** - Store operations focused tests (12 scenarios)
5. **test_v1_api.py** - API v1 specific tests

## Running Tests

### Prerequisites

1. **Backend server must be running:**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Database must be seeded:**
   ```bash
   cd backend
   python migration/run_seed.py
   ```

### Run All Table Tests (Recommended)

Tests all 14 database tables with 100% coverage:

```bash
cd backend
python tests/test_all_tables.py
```

### Run Comprehensive Tests

Tests 16 real-world repair office scenarios:

```bash
cd backend
python tests/test_comprehensive.py
```

### Run Store Operations Tests

Tests 12 store operation scenarios:

```bash
cd backend
python tests/test_store_operations.py
```

### Run Basic API Tests

Basic API endpoint tests:

```bash
cd backend
python tests/test_api.py
```

### Run All Tests

Run all test suites:

```bash
cd backend
python tests/test_all_tables.py
python tests/test_comprehensive.py
python tests/test_store_operations.py
python tests/test_api.py
```

## Test Coverage

### Tables Tested (14 total)

1. ✅ **roles** - Role management
2. ✅ **device_types** - Device type management
3. ✅ **brands** - Brand management
4. ✅ **models** - Model management
5. ✅ **problems** - Problem definitions
6. ✅ **cost_settings** - Cost configuration
7. ✅ **users** - User management
8. ✅ **role_enroll** - Role assignments
9. ✅ **devices** - Device management
10. ✅ **orders** - Order management
11. ✅ **order_assign** - Order assignments
12. ✅ **order_status_history** - Status tracking
13. ✅ **payments** - Payment processing
14. ✅ **refresh_tokens** - Token management

### Workflows Tested

- ✅ User registration and authentication
- ✅ Device registration and management
- ✅ Order creation and tracking
- ✅ Technician assignment
- ✅ Cost estimation and updates
- ✅ Payment processing (Due, Partial, Paid)
- ✅ Order status updates
- ✅ Complete repair workflow
- ✅ Multiple orders per customer
- ✅ Payment flexibility
- ✅ Error handling and validation

## Expected Results

All tests should pass with **100% success rate** when:
- Backend server is running
- Database is properly seeded
- All migrations are applied

## Troubleshooting

### Connection Error

If you see `ConnectionError: All connection attempts failed`:
- Ensure backend server is running on http://localhost:8000
- Check server logs for errors

### Database Errors

If you see database-related errors:
- Run migrations: `alembic upgrade head`
- Run seed script: `python migration/run_seed.py`
- Check database credentials in `.env` file

### Import Errors

If you see import errors:
- Ensure you're running tests from the `backend` directory
- Check that all dependencies are installed: `pip install -r requirements.txt`

