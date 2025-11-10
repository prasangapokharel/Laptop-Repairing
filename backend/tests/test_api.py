import asyncio
import httpx
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Get BASE_URL from environment or use default
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
# Remove trailing slash and /v1 if present
BASE_URL = BASE_URL.rstrip('/')
if BASE_URL.endswith('/v1'):
    BASE_URL = BASE_URL[:-3]
API_URL = f"{API_URL}/v1"  # API URL with /v1 prefix


async def test_auth():
    print("\n=== Testing Auth APIs ===")
    async with httpx.AsyncClient() as client:
        register_data = {
            "full_name": "Test User",
            "phone": "1234567890",
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = await client.post(f"{API_URL}/auth/register", json=register_data)
        print(f"Register: {response.status_code} - {response.json()}")
        
        login_data = {"phone": "1234567890", "password": "testpass123"}
        response = await client.post(f"{API_URL}/auth/login", json=login_data)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            tokens = data.get("tokens", {})
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")
            
            refresh_data = {"refresh_token": refresh_token}
            response = await client.post(f"{API_URL}/auth/refresh", json=refresh_data)
            print(f"Refresh: {response.status_code} - {response.json()}")
            
            return access_token
    return None


async def test_users(access_token):
    print("\n=== Testing Users APIs ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/users", headers=headers)
        print(f"List Users: {response.status_code} - Count: {len(response.json())}")
        
        response = await client.get(f"{API_URL}/users/1", headers=headers)
        print(f"Get User: {response.status_code} - {response.json().get('full_name')}")


async def test_devices(access_token):
    print("\n=== Testing Devices APIs ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    device_type_id = None
    brand_id = None
    model_id = None
    device_id = None
    
    async with httpx.AsyncClient() as client:
        import time
        unique_id = int(time.time() * 1000) % 10000
        
        device_type = {"name": f"Laptop_{unique_id}", "description": "Laptop computers"}
        response = await client.post(f"{API_URL}/devices/types", json=device_type, headers=headers)
        print(f"Create Device Type: {response.status_code}")
        if response.status_code == 201:
            device_type_id = response.json().get("id")
        elif response.status_code == 400:
            response = await client.get(f"{API_URL}/devices/types", headers=headers)
            if response.status_code == 200 and len(response.json()) > 0:
                device_type_id = response.json()[0].get("id")
        
        brand = {"name": f"Dell_{unique_id}"}
        response = await client.post(f"{API_URL}/devices/brands", json=brand, headers=headers)
        print(f"Create Brand: {response.status_code}")
        if response.status_code == 201:
            brand_id = response.json().get("id")
        elif response.status_code == 400:
            response = await client.get(f"{API_URL}/devices/brands", headers=headers)
            if response.status_code == 200 and len(response.json()) > 0:
                brand_id = response.json()[0].get("id")
        
        if device_type_id and brand_id:
            import time
            unique_id = int(time.time() * 1000) % 10000
            model = {"brand_id": brand_id, "name": f"XPS 13_{unique_id}", "device_type_id": device_type_id}
            response = await client.post(f"{API_URL}/devices/models", json=model, headers=headers)
            print(f"Create Model: {response.status_code}")
            if response.status_code == 201:
                model_id = response.json().get("id")
            elif response.status_code == 400:
                response = await client.get(f"{API_URL}/devices/models", headers=headers)
                if response.status_code == 200 and len(response.json()) > 0:
                    model_id = response.json()[0].get("id")
        
        if brand_id and model_id and device_type_id:
            import time
            unique_id = int(time.time() * 1000) % 10000
            device = {
                "brand_id": brand_id,
                "model_id": model_id,
                "device_type_id": device_type_id,
                "serial_number": f"SN{unique_id}",
                "owner_id": 1
            }
            response = await client.post(f"{API_URL}/devices", json=device, headers=headers)
            print(f"Create Device: {response.status_code}")
            if response.status_code == 201:
                device_id = response.json().get("id")
            elif response.status_code == 400:
                response = await client.get(f"{API_URL}/devices", headers=headers)
                if response.status_code == 200 and len(response.json()) > 0:
                    device_id = response.json()[0].get("id")
        
        response = await client.get(f"{API_URL}/devices", headers=headers)
        print(f"List Devices: {response.status_code} - Count: {len(response.json())}")
        
        return device_id


async def test_orders(access_token, device_id):
    print("\n=== Testing Orders APIs ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    order_id = None
    
    async with httpx.AsyncClient() as client:
        if not device_id:
            print("Skipping order creation - no device available")
            return None
        
        order_data = {
            "device_id": device_id,
            "cost": "100.00",
            "discount": "10.00",
            "status": "Pending"
        }
        response = await client.post(f"{API_URL}/orders", json=order_data, headers=headers)
        print(f"Create Order: {response.status_code}")
        if response.status_code == 201:
            order_id = response.json().get("id")
            print(f"Order created with ID: {order_id}")
        
        response = await client.get(f"{API_URL}/orders", headers=headers)
        print(f"List Orders: {response.status_code} - Count: {len(response.json())}")
        
        response = await client.get(f"{API_URL}/orders?status=Pending", headers=headers)
        print(f"Filter Orders by Status: {response.status_code} - Count: {len(response.json())}")
        
        if order_id:
            response = await client.get(f"{API_URL}/orders/{order_id}", headers=headers)
            print(f"Get Order: {response.status_code}")
        
        return order_id


async def test_payments(access_token, order_id):
    print("\n=== Testing Payments APIs ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    payment_id = None
    
    async with httpx.AsyncClient() as client:
        if not order_id:
            print("Skipping payment creation - no order available")
            return None
        
        payment_data = {
            "order_id": order_id,
            "due_amount": "90.00",
            "amount": "90.00",
            "status": "Paid"
        }
        response = await client.post(f"{API_URL}/payments", json=payment_data, headers=headers)
        print(f"Create Payment: {response.status_code}")
        if response.status_code == 201:
            payment_id = response.json().get("id")
            print(f"Payment created with ID: {payment_id}")
        
        response = await client.get(f"{API_URL}/payments", headers=headers)
        print(f"List Payments: {response.status_code} - Count: {len(response.json())}")
        
        if payment_id:
            response = await client.get(f"{API_URL}/payments/{payment_id}", headers=headers)
            print(f"Get Payment: {response.status_code}")
        
        return payment_id


async def test_assigns(access_token, order_id):
    print("\n=== Testing Assigns APIs ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    assign_id = None
    
    async with httpx.AsyncClient() as client:
        if not order_id:
            print("Skipping assign creation - no order available")
            return None
        
        assign_data = {"order_id": order_id, "user_id": 1}
        response = await client.post(f"{API_URL}/assigns", json=assign_data, headers=headers)
        print(f"Create Assign: {response.status_code}")
        if response.status_code == 201:
            assign_id = response.json().get("id")
            print(f"Assign created with ID: {assign_id}")
        
        response = await client.get(f"{API_URL}/assigns", headers=headers)
        print(f"List Assigns: {response.status_code} - Count: {len(response.json())}")
        
        if assign_id:
            response = await client.get(f"{API_URL}/assigns/{assign_id}", headers=headers)
            print(f"Get Assign: {response.status_code}")


async def main():
    print("Starting API Tests...")
    access_token = await test_auth()
    if access_token:
        await test_users(access_token)
        device_id = await test_devices(access_token)
        order_id = await test_orders(access_token, device_id)
        payment_id = await test_payments(access_token, order_id)
        await test_assigns(access_token, order_id)
    print("\n=== Tests Complete ===")


if __name__ == "__main__":
    asyncio.run(main())

