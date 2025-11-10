# Laptop Repair Store Management API Documentation

## Base URL
```
http://localhost:8000/v1
```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Authentication Flow

1. **Register** - Create a new user account
2. **Login** - Get access and refresh tokens
3. **Refresh** - Get a new access token using refresh token
4. **Logout** - Revoke refresh token

---

## Endpoints

### Authentication Endpoints

#### 1. Register User
**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "full_name": "John Doe",
  "phone": "1234567890",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "full_name": "John Doe",
  "phone": "1234567890",
  "email": "john@example.com",
  "profile_picture": null,
  "is_active": true,
  "is_staff": false,
  "created_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Phone already registered

---

#### 2. Login
**POST** `/auth/login`

Authenticate user and get tokens.

**Request Body:**
```json
{
  "phone": "1234567890",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "full_name": "John Doe",
    "phone": "1234567890",
    "email": "john@example.com",
    "profile_picture": null,
    "is_active": true,
    "is_staff": false,
    "created_at": "2025-01-10T10:00:00"
  },
  "tokens": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials
- `403 Forbidden` - User is inactive

---

#### 3. Refresh Token
**POST** `/auth/refresh`

Get a new access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or expired refresh token

---

#### 4. Logout
**POST** `/auth/logout`

Revoke refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** `200 OK`
```json
{
  "message": "Logged out successfully"
}
```

---

### User Endpoints

#### 1. List Users
**GET** `/users`

Get list of users with pagination.

**Query Parameters:**
- `limit` (optional, default: 10, min: 1, max: 100) - Number of results per page
- `offset` (optional, default: 0, min: 0) - Number of results to skip

**Headers:**
```
Authorization: Bearer <access_token>
```

**Example:**
```
GET /users?limit=20&offset=0
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "full_name": "John Doe",
    "phone": "1234567890",
    "email": "john@example.com",
    "profile_picture": null,
    "is_active": true,
    "is_staff": false,
    "created_at": "2025-01-10T10:00:00"
  }
]
```

---

#### 2. Get User
**GET** `/users/{user_id}`

Get user by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "full_name": "John Doe",
  "phone": "1234567890",
  "email": "john@example.com",
  "profile_picture": null,
  "is_active": true,
  "is_staff": false,
  "created_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `404 Not Found` - User not found

---

#### 3. Create User
**POST** `/users`

Create a new user (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "full_name": "Jane Doe",
  "phone": "9876543210",
  "email": "jane@example.com",
  "password": "password123",
  "is_staff": false
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "full_name": "Jane Doe",
  "phone": "9876543210",
  "email": "jane@example.com",
  "profile_picture": null,
  "is_active": true,
  "is_staff": false,
  "created_at": "2025-01-10T10:00:00"
}
```

---

#### 4. Update User
**PATCH** `/users/{user_id}`

Update user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "full_name": "John Updated",
  "email": "john.updated@example.com",
  "profile_picture": "https://example.com/avatar.jpg"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "full_name": "John Updated",
  "phone": "1234567890",
  "email": "john.updated@example.com",
  "profile_picture": "https://example.com/avatar.jpg",
  "is_active": true,
  "is_staff": false,
  "created_at": "2025-01-10T10:00:00"
}
```

---

#### 5. Delete User
**DELETE** `/users/{user_id}`

Delete user by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

---

### Device Endpoints

#### 1. Create Device Type
**POST** `/devices/types`

Create a new device type.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Laptop",
  "description": "Laptop computers"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Laptop computers",
  "created_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Device type already exists

---

#### 2. List Device Types
**GET** `/devices/types`

Get all device types.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "Laptop computers",
    "created_at": "2025-01-10T10:00:00"
  }
]
```

---

#### 3. Create Brand
**POST** `/devices/brands`

Create a new brand.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Dell",
  "description": "Dell Inc."
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Dell",
  "description": "Dell Inc.",
  "created_at": "2025-01-10T10:00:00"
}
```

---

#### 4. List Brands
**GET** `/devices/brands`

Get all brands.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Dell",
    "description": "Dell Inc.",
    "created_at": "2025-01-10T10:00:00"
  }
]
```

---

#### 5. Create Model
**POST** `/devices/models`

Create a new device model.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "brand_id": 1,
  "name": "XPS 13",
  "device_type_id": 1
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "brand_id": 1,
  "name": "XPS 13",
  "device_type_id": 1,
  "created_at": "2025-01-10T10:00:00"
}
```

---

#### 6. List Models
**GET** `/devices/models`

Get all models.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "brand_id": 1,
    "name": "XPS 13",
    "device_type_id": 1,
    "created_at": "2025-01-10T10:00:00"
  }
]
```

---

#### 7. Create Device
**POST** `/devices`

Register a new device.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "brand_id": 1,
  "model_id": 1,
  "device_type_id": 1,
  "serial_number": "SN123456789",
  "owner_id": 1,
  "notes": "Screen cracked"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "brand_id": 1,
  "model_id": 1,
  "device_type_id": 1,
  "serial_number": "SN123456789",
  "owner_id": 1,
  "notes": "Screen cracked",
  "created_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `404 Not Found` - Brand, model, device type, or owner not found

---

#### 8. List Devices
**GET** `/devices`

Get all devices with pagination.

**Query Parameters:**
- `limit` (optional, default: 10, min: 1, max: 100) - Number of results per page
- `offset` (optional, default: 0, min: 0) - Number of results to skip
- `owner_id` (optional) - Filter by owner ID

**Headers:**
```
Authorization: Bearer <access_token>
```

**Example:**
```
GET /devices?limit=20&offset=0&owner_id=1
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "brand_id": 1,
    "model_id": 1,
    "device_type_id": 1,
    "serial_number": "SN123456789",
    "owner_id": 1,
    "notes": "Screen cracked",
    "created_at": "2025-01-10T10:00:00"
  }
]
```

---

#### 9. Get Device
**GET** `/devices/{device_id}`

Get device by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "brand_id": 1,
  "model_id": 1,
  "device_type_id": 1,
  "serial_number": "SN123456789",
  "owner_id": 1,
  "notes": "Screen cracked",
  "created_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `404 Not Found` - Device not found

---

#### 10. Update Device
**PATCH** `/devices/{device_id}`

Update device information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "notes": "Screen replaced, working fine now"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "brand_id": 1,
  "model_id": 1,
  "device_type_id": 1,
  "serial_number": "SN123456789",
  "owner_id": 1,
  "notes": "Screen replaced, working fine now",
  "created_at": "2025-01-10T10:00:00"
}
```

---

#### 11. Delete Device
**DELETE** `/devices/{device_id}`

Delete device by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

---

### Order Endpoints

#### 1. Create Order
**POST** `/orders`

Create a new repair order.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "device_id": 1,
  "customer_id": 1,
  "problem_id": null,
  "cost": "250.00",
  "discount": "0.00",
  "note": "Screen replacement needed",
  "status": "Pending",
  "estimated_completion_date": null
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "device_id": 1,
  "customer_id": 1,
  "problem_id": null,
  "cost": "250.00",
  "discount": "0.00",
  "total_cost": "250.00",
  "note": "Screen replacement needed",
  "status": "Pending",
  "estimated_completion_date": null,
  "completed_at": null,
  "created_at": "2025-01-10T10:00:00",
  "updated_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `404 Not Found` - Device not found

**Status Values:**
- `Pending` - Order created, waiting for technician
- `Repairing` - Order is being repaired
- `Completed` - Order completed
- `Cancelled` - Order cancelled

---

#### 2. List Orders
**GET** `/orders`

Get all orders with filtering and pagination.

**Query Parameters:**
- `status` (optional) - Filter by status (Pending, Repairing, Completed, Cancelled)
- `customer_id` (optional) - Filter by customer ID
- `device_id` (optional) - Filter by device ID
- `limit` (optional, default: 10, min: 1, max: 100) - Number of results per page
- `offset` (optional, default: 0, min: 0) - Number of results to skip

**Headers:**
```
Authorization: Bearer <access_token>
```

**Examples:**
```
GET /orders?status=Pending
GET /orders?customer_id=1&limit=20
GET /orders?device_id=1&status=Completed
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "device_id": 1,
    "customer_id": 1,
    "problem_id": null,
    "cost": "250.00",
    "discount": "0.00",
    "total_cost": "250.00",
    "note": "Screen replacement needed",
    "status": "Pending",
    "estimated_completion_date": null,
    "completed_at": null,
    "created_at": "2025-01-10T10:00:00",
    "updated_at": "2025-01-10T10:00:00"
  }
]
```

---

#### 3. Get Order
**GET** `/orders/{order_id}`

Get order by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "device_id": 1,
  "customer_id": 1,
  "problem_id": null,
  "cost": "250.00",
  "discount": "0.00",
  "total_cost": "250.00",
  "note": "Screen replacement needed",
  "status": "Pending",
  "estimated_completion_date": null,
  "completed_at": null,
  "created_at": "2025-01-10T10:00:00",
  "updated_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `404 Not Found` - Order not found

---

#### 4. Update Order
**PATCH** `/orders/{order_id}`

Update order information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "cost": "300.00",
  "discount": "25.00",
  "status": "Repairing",
  "note": "Diagnosis complete: Screen + battery replacement needed"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "device_id": 1,
  "customer_id": 1,
  "problem_id": null,
  "cost": "300.00",
  "discount": "25.00",
  "total_cost": "275.00",
  "note": "Diagnosis complete: Screen + battery replacement needed",
  "status": "Repairing",
  "estimated_completion_date": null,
  "completed_at": null,
  "created_at": "2025-01-10T10:00:00",
  "updated_at": "2025-01-10T10:30:00"
}
```

---

#### 5. Delete Order
**DELETE** `/orders/{order_id}`

Delete order by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

---

#### 6. Assign Order
**POST** `/orders/assign`

Assign an order to a technician.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "order_id": 1,
  "user_id": 2
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "order_id": 1,
  "user_id": 2,
  "assigned_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `404 Not Found` - Order or user not found
- `400 Bad Request` - Assignment already exists

---

#### 7. Get Order Assignments
**GET** `/orders/assign/{order_id}`

Get all assignments for an order.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "order_id": 1,
    "user_id": 2,
    "assigned_at": "2025-01-10T10:00:00"
  }
]
```

---

### Payment Endpoints

#### 1. Create Payment
**POST** `/payments`

Create a new payment record.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "order_id": 1,
  "due_amount": "275.00",
  "amount": "150.00",
  "status": "Partial",
  "payment_method": "Cash",
  "transaction_id": "TXN001"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "order_id": 1,
  "due_amount": "275.00",
  "amount": "150.00",
  "status": "Partial",
  "payment_method": "Cash",
  "transaction_id": "TXN001",
  "created_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `404 Not Found` - Order not found

**Status Values:**
- `Paid` - Payment completed
- `Due` - Payment due
- `Unpaid` - Payment not made
- `Partial` - Partial payment made

---

#### 2. List Payments
**GET** `/payments`

Get all payments with filtering and pagination.

**Query Parameters:**
- `status` (optional) - Filter by status (Paid, Due, Unpaid, Partial)
- `order_id` (optional) - Filter by order ID
- `limit` (optional, default: 10, min: 1, max: 100) - Number of results per page
- `offset` (optional, default: 0, min: 0) - Number of results to skip

**Headers:**
```
Authorization: Bearer <access_token>
```

**Examples:**
```
GET /payments?status=Paid
GET /payments?order_id=1
GET /payments?status=Partial&limit=20
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "order_id": 1,
    "due_amount": "275.00",
    "amount": "150.00",
    "status": "Partial",
    "payment_method": "Cash",
    "transaction_id": "TXN001",
    "created_at": "2025-01-10T10:00:00"
  }
]
```

---

#### 3. Get Payment
**GET** `/payments/{payment_id}`

Get payment by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "order_id": 1,
  "due_amount": "275.00",
  "amount": "150.00",
  "status": "Partial",
  "payment_method": "Cash",
  "transaction_id": "TXN001",
  "created_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `404 Not Found` - Payment not found

---

#### 4. Update Payment
**PATCH** `/payments/{payment_id}`

Update payment information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "amount": "275.00",
  "status": "Paid",
  "payment_method": "Card"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "order_id": 1,
  "due_amount": "275.00",
  "amount": "275.00",
  "status": "Paid",
  "payment_method": "Card",
  "transaction_id": "TXN001",
  "created_at": "2025-01-10T10:00:00"
}
```

---

#### 5. Delete Payment
**DELETE** `/payments/{payment_id}`

Delete payment by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

---

### Assignment Endpoints

#### 1. Create Assignment
**POST** `/assigns`

Assign an order to a technician.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "order_id": 1,
  "user_id": 2
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "order_id": 1,
  "user_id": 2,
  "assigned_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `404 Not Found` - Order or user not found
- `400 Bad Request` - Assignment already exists

---

#### 2. List Assignments
**GET** `/assigns`

Get all assignments with filtering and pagination.

**Query Parameters:**
- `order_id` (optional) - Filter by order ID
- `user_id` (optional) - Filter by user ID
- `limit` (optional, default: 10, min: 1, max: 100) - Number of results per page
- `offset` (optional, default: 0, min: 0) - Number of results to skip

**Headers:**
```
Authorization: Bearer <access_token>
```

**Examples:**
```
GET /assigns?user_id=2
GET /assigns?order_id=1
GET /assigns?user_id=2&limit=20
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "order_id": 1,
    "user_id": 2,
    "assigned_at": "2025-01-10T10:00:00"
  }
]
```

---

#### 3. Get Assignment
**GET** `/assigns/{assign_id}`

Get assignment by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "order_id": 1,
  "user_id": 2,
  "assigned_at": "2025-01-10T10:00:00"
}
```

**Error Responses:**
- `404 Not Found` - Assignment not found

---

#### 4. Delete Assignment
**DELETE** `/assigns/{assign_id}`

Delete assignment by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

---

## Error Responses

### Standard Error Format
```json
{
  "detail": "Error message here"
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content to return
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or invalid token
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

### Validation Error Format
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "phone"],
      "msg": "Field required"
    }
  ]
}
```

---

## Data Types

### Decimal
All monetary values (cost, discount, total_cost, amount, due_amount) are returned as strings to preserve precision.

Example: `"250.00"` instead of `250.00`

### DateTime
All datetime fields are returned in ISO 8601 format with timezone.

Example: `"2025-01-10T10:00:00"`

### Status Enums

**Order Status:**
- `Pending`
- `Repairing`
- `Completed`
- `Cancelled`

**Payment Status:**
- `Paid`
- `Due`
- `Unpaid`
- `Partial`

---

## Best Practices

### 1. Token Management
- Store access token securely (e.g., in memory or secure storage)
- Refresh access token before it expires (24 hours)
- Handle 401 errors by refreshing token or redirecting to login

### 2. Error Handling
- Always check response status codes
- Display user-friendly error messages
- Handle network errors gracefully

### 3. Pagination
- Use appropriate `limit` values (10-50 for lists)
- Implement infinite scroll or pagination controls
- Track `offset` for next page requests

### 4. Filtering
- Use query parameters for filtering lists
- Combine multiple filters when needed
- Validate filter values on frontend

### 5. Request Headers
- Always include `Authorization` header for protected endpoints
- Set `Content-Type: application/json` for POST/PATCH requests

---

## Example Frontend Integration

### JavaScript/TypeScript Example

```typescript
const API_BASE_URL = 'http://localhost:8000/v1';

// Login function
async function login(phone: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ phone, password }),
  });
  
  if (!response.ok) {
    throw new Error('Login failed');
  }
  
  const data = await response.json();
  // Store tokens
  localStorage.setItem('access_token', data.tokens.access_token);
  localStorage.setItem('refresh_token', data.tokens.refresh_token);
  
  return data;
}

// Authenticated request helper
async function authenticatedFetch(url: string, options: RequestInit = {}) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  
  if (response.status === 401) {
    // Try to refresh token
    await refreshToken();
    // Retry request
    return authenticatedFetch(url, options);
  }
  
  return response;
}

// Refresh token function
async function refreshToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  
  const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
  
  if (!response.ok) {
    // Redirect to login
    window.location.href = '/login';
    return;
  }
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
}

// Get orders example
async function getOrders(filters?: { status?: string; customer_id?: number }) {
  const params = new URLSearchParams();
  if (filters?.status) params.append('status', filters.status);
  if (filters?.customer_id) params.append('customer_id', filters.customer_id.toString());
  
  const response = await authenticatedFetch(`/orders?${params.toString()}`);
  return response.json();
}
```

---

## Support

For API issues or questions, contact the backend development team.

**API Version:** 1.0.0  
**Last Updated:** January 2025

