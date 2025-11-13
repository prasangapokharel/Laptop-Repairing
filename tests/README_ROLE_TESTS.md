# Role-Based API Test Suite

Complete test suite for Receptionist, Technician, and Accountant roles with full CRUD operations.

## Test Files

1. **test_roles_complete.py** - Main role-based test suite
2. **run_role_tests.py** - Quick test runner
3. **test_all_api_complete.py** - Complete API coverage test

## Features

### ✅ Receptionist Tests (Order Management)
- ✅ Create Order
- ✅ Create Multiple Orders (different scenarios)
- ✅ List All Orders
- ✅ Filter Orders by Status (Pending, Repairing, Completed, Cancelled)
- ✅ Get Order Details
- ✅ Update Order Status
- ✅ Delete Order

### ✅ Technician Tests (Assignment Management)
- ✅ Assign Order to Technician
- ✅ Create Assignment
- ✅ List All Assignments
- ✅ Get My Assignments (filter by user_id)
- ✅ Get Order Assignments
- ✅ Get Assignment Details
- ✅ Delete Assignment

### ✅ Accountant Tests (Payment Management)
- ✅ Create Payment
- ✅ Create Multiple Payments (Paid, Partial, Unpaid)
- ✅ List All Payments
- ✅ Filter Payments by Status (Paid, Due, Unpaid, Partial)
- ✅ Filter Payments by Order
- ✅ Get Payment Details
- ✅ Update Payment
- ✅ Delete Payment

### ✅ Complete Workflow Test
- ✅ Order Creation → Assignment → Payment → Completion

## How to Run

### Prerequisites

1. **Start Backend Server:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Ensure Database is Seeded:**
```bash
cd backend
python migration/run_seed.py
```

### Run Role-Based Tests

```bash
cd backend
python tests/test_roles_complete.py
```

Or use the quick runner:

```bash
cd backend
python tests/run_role_tests.py
```

### Run All API Tests

```bash
cd backend
python tests/test_all_api_complete.py
```

## Test Output

The tests will show:
- ✅ PASS: Test name - Status code
- ❌ FAIL: Test name - Expected vs Got
- 📊 Summary with pass/fail counts and success rate

## Expected Results

All tests should pass with **100% success rate** when:
- ✅ Backend server is running
- ✅ Database is properly seeded
- ✅ All migrations are applied
- ✅ Test user exists (phone: 9876543210, password: password123)

## Test Scenarios

### Receptionist Scenarios
1. Create single order
2. Create multiple orders with different costs and statuses
3. List and filter orders
4. Update order status through workflow
5. Delete orders

### Technician Scenarios
1. Assign orders to technicians
2. View assigned orders
3. Filter assignments by order and user
4. Manage assignments (create, view, delete)

### Accountant Scenarios
1. Create payments with different statuses
2. Track payment history
3. Filter payments by status and order
4. Update payment status
5. Manage payment records

### Complete Workflow
1. Receptionist creates order
2. Technician assigns order
3. Order status updated to Repairing
4. Accountant creates payment
5. Order status updated to Completed

## Troubleshooting

### Connection Errors
- Ensure backend server is running on http://localhost:8000
- Check server logs for errors

### Variable Errors in Postman
- Run requests in sequence (Login first to set tokens)
- Ensure variables are set in collection/environment
- Check that test scripts save variables correctly

### Test Failures
- Verify database is seeded
- Check that test user exists
- Ensure all migrations are applied
- Review error messages in test output

## Test Coverage

- **Total Tests:** 30+ role-based tests
- **Coverage:** 100% of role-specific endpoints
- **CRUD Operations:** All Create, Read, Update, Delete operations tested
- **Status Codes:** All tests verify 200/201/204 status codes
- **Error Handling:** Tests handle existing data gracefully

## Notes

- Tests automatically handle existing data (won't fail on duplicates)
- Tests clean up created resources where possible
- All tests use proper authentication tokens
- Tests are flexible and handle edge cases

