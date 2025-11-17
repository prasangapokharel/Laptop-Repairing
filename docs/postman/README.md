# Postman API Collection

## Location
`docs/postman/v1postman.json`

## Quick Start

1. **Import into Postman:**
   - Open Postman
   - Click "Import" → Select `docs/postman/v1postman.json`
   - Collection will be imported with all endpoints and tests

2. **Set Base URL:**
   - Collection variable `base_url` is set to `http://localhost:8000`
   - Update if your API runs on a different port/host

3. **Authentication:**
   - Start with "1. Authentication" → "Register" or "Login"
   - Access token is automatically saved to `access_token` variable
   - All protected endpoints use this token automatically

## Collection Structure

```
1. Authentication
   - Register
   - Login
   - Refresh Token
   - Logout

2. Admin - Users
   - Create User
   - List Users
   - Get User
   - Update User
   - Delete User

3. Admin - Roles
   - Create Role
   - List Roles
   - Assign Role to User

4. Admin - Devices
   - Device Types (CRUD)
   - Brands (CRUD)
   - Models (CRUD)
   - Devices (CRUD)

5. Reception - Orders
   - Create Order
   - List Orders
   - Get Order
   - Update Order
   - Delete Order

6. Technician - Assignments
   - Assign Order
   - List Assignments
   - Get Assignment
   - Update Assignment
   - Delete Assignment

7. Accountant - Payments
   - Create Payment
   - List Payments
   - Get Payment
   - Update Payment
   - Delete Payment

8. Customer - My Orders
   - List My Orders
   - Get My Order
```

## Features

- **Auto-generated Random Data:** All "Create" endpoints use Postman's dynamic variables (`{{$randomPhoneNumber}}`, `{{$randomInt}}`, etc.) for unique test data
- **Auto-fetch IDs:** Collection-level pre-request script automatically fetches `device_type_id`, `brand_id`, `model_id`, `device_id` if not set
- **Automatic Tests:** Each request includes tests to verify status codes (200, 201, 204) and response structure
- **Variable Management:** IDs and tokens are automatically saved from responses for use in subsequent requests

## Variables

Collection variables (auto-set from responses):
- `access_token` - JWT access token
- `refresh_token` - JWT refresh token
- `user_id` - Current user ID
- `created_user_id` - ID of newly created user
- `role_id` - Role ID
- `device_type_id` - Device type ID
- `brand_id` - Brand ID
- `model_id` - Model ID
- `device_id` - Device ID
- `order_id` - Order ID
- `assign_id` - Assignment ID
- `payment_id` - Payment ID

## Updating the Collection

1. **Edit in Postman:**
   - Make changes in Postman UI
   - Export collection: Collection → "..." → Export
   - Save as `docs/postman/v1postman.json`

2. **Edit JSON directly:**
   - Edit `docs/postman/v1postman.json`
   - Import back into Postman to verify

## Testing

- All requests include automated tests
- Run entire collection: Collection → "Run" → "Run Laptop Repair Store API v1"
- Tests verify:
  - Status codes (200, 201, 204, etc.)
  - Response structure
  - Required fields presence

## Test User

Default test user (from seed data):
- Phone: `9876543210`
- Password: `password123`
- Roles: Customer, Reception

## Notes

- Base URL: `http://localhost:8000` (update `base_url` variable if different)
- All endpoints use `/v1` prefix
- Protected endpoints require `Authorization: Bearer {access_token}` header (auto-added)
- Random data ensures no conflicts when running tests multiple times

