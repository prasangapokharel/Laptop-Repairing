# API Version 1 (v1)

This directory contains all API endpoints for version 1 of the Laptop Repair Store Management API.

## Structure

```
apps/api/v1/
├── __init__.py      # Main router that combines all v1 endpoints
├── auth.py          # Authentication endpoints (register, login, refresh, logout)
├── users.py         # User management endpoints (CRUD + roles)
├── devices.py       # Device management endpoints (types, brands, models, devices)
├── orders.py        # Order management endpoints (CRUD + assignments)
├── payments.py      # Payment management endpoints (CRUD)
└── assigns.py       # Assignment management endpoints (CRUD)
```

## Usage

All v1 endpoints are automatically included via the `api_router` in `__init__.py`:

```python
from apps.api.v1 import api_router
app.include_router(api_router)
```

## Endpoints

All endpoints are prefixed with `/v1`:

- `/v1/auth/*` - Authentication
- `/v1/users/*` - User management
- `/v1/devices/*` - Device management
- `/v1/orders/*` - Order management
- `/v1/payments/*` - Payment management
- `/v1/assigns/*` - Assignment management

## Adding New Endpoints

To add new endpoints to v1:

1. Add the endpoint to the appropriate module (e.g., `orders.py`)
2. The router is automatically included via `__init__.py`

## Creating Version 2 (v2)

When you need to create v2:

1. Create `apps/api/v2/` directory
2. Copy v1 structure as a starting point
3. Modify endpoints as needed
4. Create `apps/api/v2/__init__.py` with v2 router
5. Update `main.py` to include both versions:

```python
from apps.api.v1 import api_router as v1_router
from apps.api.v2 import api_router as v2_router

app.include_router(v1_router)
app.include_router(v2_router)
```

This allows both versions to coexist, ensuring backward compatibility.

