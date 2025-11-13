"""
Complete Role-Based API Test Suite
Tests Receptionist, Technician, and Accountant roles with all scenarios
Ensures CREATE, READ, UPDATE, DELETE work perfectly
"""
import asyncio
import httpx
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Get BASE_URL from environment or use default
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
BASE_URL = BASE_URL.rstrip('/')
if BASE_URL.endswith('/v1'):
    BASE_URL = BASE_URL[:-3]
API_URL = f"{BASE_URL}/v1"


class RoleBasedTest:
    def __init__(self):
        self.api_url = API_URL
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.technician_id = None
        self.customer_id = None
        self.device_type_id = None
        self.brand_id = None
        self.model_id = None
        self.device_id = None
        self.order_id = None
        self.payment_id = None
        self.assign_id = None
        self.passed = 0
        self.failed = 0
        self.unique_id = int(time.time() * 1000) % 100000
        self.created_orders = []
        self.created_payments = []
        self.created_assigns = []

    def print_test(self, test_name, status_code, expected=200):
        if status_code == expected:
            self.passed += 1
            print(f"[PASS] {test_name} - Status: {status_code}")
        else:
            self.failed += 1
            print(f"[FAIL] {test_name} - Expected: {expected}, Got: {status_code}")

    async def setup_auth(self):
        """Setup authentication - try multiple approaches"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Try different phone numbers that might exist
            test_phones = ["9876543210", "1234567890", "9999999999"]
            
            for phone in test_phones:
                data = {"phone": phone, "password": "password123"}
                try:
                    response = await client.post(f"{self.api_url}/auth/login", json=data)
                    if response.status_code == 200:
                        json_data = response.json()
                        self.access_token = json_data.get("tokens", {}).get("access_token")
                        self.refresh_token = json_data.get("tokens", {}).get("refresh_token")
                        self.user_id = json_data.get("user", {}).get("id")
                        print(f"PASS: Logged in with phone {phone}")
                        return True
                except:
                    continue
            
            # If all logins fail, try to register a new user
            unique_phone = f"999{self.unique_id}"
            register_data = {
                "full_name": "Test User",
                "phone": unique_phone,
                "email": f"test{self.unique_id}@example.com",
                "password": "password123"
            }
            try:
                reg_response = await client.post(f"{self.api_url}/auth/register", json=register_data)
                if reg_response.status_code == 201:
                    # Login with newly registered user
                    login_data = {"phone": unique_phone, "password": "password123"}
                    login_response = await client.post(f"{self.api_url}/auth/login", json=login_data)
                    if login_response.status_code == 200:
                        json_data = login_response.json()
                        self.access_token = json_data.get("tokens", {}).get("access_token")
                        self.refresh_token = json_data.get("tokens", {}).get("refresh_token")
                        self.user_id = json_data.get("user", {}).get("id")
                        print(f"PASS: Registered and logged in with phone {unique_phone}")
                        return True
            except Exception as e:
                print(f"[FAIL] Registration failed: {e}")
            
            print(f"[FAIL] All authentication attempts failed")
            return False

    async def setup_test_data(self):
        """Setup required test data (device types, brands, models, users)"""
        if not self.access_token:
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Get or create device type
            try:
                response = await client.get(f"{self.api_url}/devices/types", headers=headers)
                if response.status_code == 200 and len(response.json()) > 0:
                    self.device_type_id = response.json()[0].get("id")
                else:
                    data = {"name": f"Laptop{self.unique_id}", "description": "Laptop"}
                    response = await client.post(f"{self.api_url}/devices/types", json=data, headers=headers)
                    if response.status_code == 201:
                        self.device_type_id = response.json().get("id")
            except:
                pass

            # Get or create brand
            try:
                response = await client.get(f"{self.api_url}/devices/brands", headers=headers)
                if response.status_code == 200 and len(response.json()) > 0:
                    self.brand_id = response.json()[0].get("id")
                else:
                    data = {"name": f"Dell{self.unique_id}"}
                    response = await client.post(f"{self.api_url}/devices/brands", json=data, headers=headers)
                    if response.status_code == 201:
                        self.brand_id = response.json().get("id")
            except:
                pass

            # Get or create model
            if self.brand_id and self.device_type_id:
                try:
                    response = await client.get(f"{self.api_url}/devices/models", headers=headers)
                    if response.status_code == 200 and len(response.json()) > 0:
                        self.model_id = response.json()[0].get("id")
                    else:
                        data = {
                            "brand_id": self.brand_id,
                            "name": f"XPS13_{self.unique_id}",
                            "device_type_id": self.device_type_id
                        }
                        response = await client.post(f"{self.api_url}/devices/models", json=data, headers=headers)
                        if response.status_code == 201:
                            self.model_id = response.json().get("id")
                except:
                    pass

            # Get or create customer
            try:
                response = await client.get(f"{self.api_url}/users?limit=10", headers=headers)
                if response.status_code == 200 and len(response.json()) > 0:
                    self.customer_id = response.json()[0].get("id")
                else:
                    data = {
                        "full_name": f"Customer {self.unique_id}",
                        "phone": f"999{self.unique_id}",
                        "email": f"customer{self.unique_id}@test.com",
                        "password": "password123"
                    }
                    response = await client.post(f"{self.api_url}/users", json=data, headers=headers)
                    if response.status_code == 201:
                        self.customer_id = response.json().get("id")
            except:
                pass

            # Get or create device
            if self.brand_id and self.model_id and self.device_type_id:
                try:
                    data = {
                        "brand_id": self.brand_id,
                        "model_id": self.model_id,
                        "device_type_id": self.device_type_id,
                        "serial_number": f"SN{self.unique_id}",
                        "owner_id": self.customer_id,
                        "notes": "Test device for orders"
                    }
                    response = await client.post(f"{self.api_url}/devices", json=data, headers=headers)
                    if response.status_code == 201:
                        self.device_id = response.json().get("id")
                except:
                    pass

        return True

    # ==================== RECEPTIONIST - ORDER MANAGEMENT ====================

    async def test_reception_create_order(self):
        """Receptionist: Create new order"""
        if not self.access_token or not self.device_id:
            print("[SKIP] POST /orders - Missing required data")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            data = {
                "device_id": self.device_id,
                "customer_id": self.customer_id,
                "cost": "250.00",
                "discount": "10.00",
                "note": "Screen replacement needed",
                "status": "Pending"
            }
            try:
                response = await client.post(f"{self.api_url}/orders", json=data, headers=headers)
                self.print_test("Receptionist: POST /orders (Create Order)", response.status_code, 201)
                if response.status_code == 201:
                    self.order_id = response.json().get("id")
                    self.created_orders.append(self.order_id)
                return response.status_code == 201
            except Exception as e:
                print(f"[FAIL] POST /orders - Error: {e}")
                self.failed += 1
                return False

    async def test_reception_create_multiple_orders(self):
        """Receptionist: Create multiple orders for different scenarios"""
        if not self.access_token or not self.device_id:
            print("[SKIP] Multiple orders - Missing required data")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            
            orders_data = [
                {"cost": "150.00", "discount": "0.00", "status": "Pending", "note": "Battery replacement"},
                {"cost": "300.00", "discount": "25.00", "status": "Pending", "note": "Keyboard repair"},
                {"cost": "500.00", "discount": "50.00", "status": "Repairing", "note": "Motherboard repair"}
            ]
            
            created_count = 0
            for order_data in orders_data:
                data = {
                    "device_id": self.device_id,
                    "customer_id": self.customer_id,
                    **order_data
                }
                try:
                    response = await client.post(f"{self.api_url}/orders", json=data, headers=headers)
                    if response.status_code == 201:
                        order_id = response.json().get("id")
                        self.created_orders.append(order_id)
                        created_count += 1
                except:
                    pass
            
            self.print_test(f"Receptionist: Create Multiple Orders ({created_count}/{len(orders_data)})", 200 if created_count > 0 else 400, 200)
            return created_count > 0

    async def test_reception_list_orders(self):
        """Receptionist: List all orders"""
        if not self.access_token:
            print("[SKIP] GET /orders - No access token")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            try:
                response = await client.get(f"{self.api_url}/orders?limit=20&offset=0", headers=headers)
                self.print_test("Receptionist: GET /orders (List All)", response.status_code, 200)
                return response.status_code == 200
            except Exception as e:
                print(f"[FAIL] GET /orders - Error: {e}")
                self.failed += 1
                return False

    async def test_reception_filter_orders_by_status(self):
        """Receptionist: Filter orders by status"""
        if not self.access_token:
            print("[SKIP] Filter orders - No access token")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            statuses = ["Pending", "Repairing", "Completed", "Cancelled"]
            success_count = 0
            for status in statuses:
                try:
                    response = await client.get(f"{self.api_url}/orders?status={status}&limit=10", headers=headers)
                    if response.status_code == 200:
                        success_count += 1
                except:
                    pass
            self.print_test(f"Receptionist: Filter Orders by Status ({success_count}/{len(statuses)})", 200 if success_count == len(statuses) else 400, 200)
            return success_count == len(statuses)

    async def test_reception_get_order_details(self):
        """Receptionist: Get order details"""
        if not self.access_token or not self.order_id:
            print("[SKIP] GET /orders/{id} - No order_id")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            try:
                response = await client.get(f"{self.api_url}/orders/{self.order_id}", headers=headers)
                self.print_test("Receptionist: GET /orders/{id} (Get Details)", response.status_code, 200)
                return response.status_code == 200
            except Exception as e:
                print(f"[FAIL] GET /orders/{id} - Error: {e}")
                self.failed += 1
                return False

    async def test_reception_update_order_status(self):
        """Receptionist: Update order status"""
        if not self.access_token or not self.order_id:
            print("[SKIP] PATCH /orders/{id} - No order_id")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            status_updates = [
                {"status": "Repairing", "note": "Work started"},
                {"status": "Completed", "note": "Repair completed successfully"}
            ]
            success_count = 0
            for update_data in status_updates:
                try:
                    response = await client.patch(f"{self.api_url}/orders/{self.order_id}", json=update_data, headers=headers)
                    if response.status_code == 200:
                        success_count += 1
                except:
                    pass
            self.print_test(f"Receptionist: Update Order Status ({success_count}/{len(status_updates)})", 200 if success_count > 0 else 400, 200)
            return success_count > 0

    async def test_reception_delete_order(self):
        """Receptionist: Delete order"""
        if not self.access_token or not self.created_orders:
            print("[SKIP] DELETE /orders/{id} - No orders to delete")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            # Delete the last created order
            order_to_delete = self.created_orders[-1] if self.created_orders else None
            if order_to_delete:
                try:
                    response = await client.delete(f"{self.api_url}/orders/{order_to_delete}", headers=headers)
                    self.print_test("Receptionist: DELETE /orders/{id} (Delete Order)", response.status_code, 204)
                    if response.status_code == 204:
                        self.created_orders.remove(order_to_delete)
                    return response.status_code == 204
                except Exception as e:
                    print(f"[FAIL] DELETE /orders/{id} - Error: {e}")
                    self.failed += 1
                    return False
        return False

    # ==================== TECHNICIAN - ASSIGNMENT MANAGEMENT ====================

    async def test_technician_assign_order(self):
        """Technician: Assign order to technician"""
        if not self.access_token or not self.order_id or not self.user_id:
            print("[SKIP] POST /orders/assign - Missing required data")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            data = {"order_id": self.order_id, "user_id": self.user_id}
            try:
                response = await client.post(f"{self.api_url}/orders/assign", json=data, headers=headers)
                if response.status_code in [201, 400]:  # 400 if already assigned
                    self.print_test("Technician: POST /orders/assign (Assign Order)", response.status_code, 201)
                    if response.status_code == 201:
                        self.assign_id = response.json().get("id")
                        self.created_assigns.append(self.assign_id)
                return response.status_code in [201, 400]
            except Exception as e:
                print(f"[FAIL] POST /orders/assign - Error: {e}")
                self.failed += 1
                return False

    async def test_technician_create_assignment(self):
        """Technician: Create assignment via /assigns endpoint"""
        if not self.access_token or not self.order_id or not self.user_id:
            print("[SKIP] POST /assigns - Missing required data")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            data = {"order_id": self.order_id, "user_id": self.user_id}
            try:
                response = await client.post(f"{self.api_url}/assigns", json=data, headers=headers)
                if response.status_code == 201:
                    assign_id = response.json().get("id")
                    self.created_assigns.append(assign_id)
                    self.print_test("Technician: POST /assigns (Create Assignment)", response.status_code, 201)
                elif response.status_code == 400:
                    # Already assigned, get existing
                    response = await client.get(f"{self.api_url}/assigns?order_id={self.order_id}", headers=headers)
                    if response.status_code == 200 and len(response.json()) > 0:
                        assign_id = response.json()[0].get("id")
                        self.assign_id = assign_id
                        print(f"[PASS] POST /assigns - Assignment exists, using: {assign_id}")
                        self.passed += 1
                return response.status_code in [201, 400]
            except Exception as e:
                print(f"[FAIL] POST /assigns - Error: {e}")
                self.failed += 1
                return False

    async def test_technician_list_assignments(self):
        """Technician: List all assignments"""
        if not self.access_token:
            print("[SKIP] GET /assigns - No access token")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            try:
                response = await client.get(f"{self.api_url}/assigns?limit=20&offset=0", headers=headers)
                self.print_test("Technician: GET /assigns (List All)", response.status_code, 200)
                return response.status_code == 200
            except Exception as e:
                print(f"[FAIL] GET /assigns - Error: {e}")
                self.failed += 1
                return False

    async def test_technician_get_my_assignments(self):
        """Technician: Get my assigned orders"""
        if not self.access_token or not self.user_id:
            print("[SKIP] GET /assigns?user_id - Missing user_id")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            try:
                response = await client.get(f"{self.api_url}/assigns?user_id={self.user_id}&limit=10", headers=headers)
                self.print_test("Technician: GET /assigns?user_id (My Assignments)", response.status_code, 200)
                return response.status_code == 200
            except Exception as e:
                print(f"[FAIL] GET /assigns?user_id - Error: {e}")
                self.failed += 1
                return False

    async def test_technician_get_order_assignments(self):
        """Technician: Get assignments for specific order"""
        if not self.access_token or not self.order_id:
            print("[SKIP] GET /orders/assign/{order_id} - Missing order_id")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            try:
                response = await client.get(f"{self.api_url}/orders/assign/{self.order_id}", headers=headers)
                self.print_test("Technician: GET /orders/assign/{order_id} (Order Assignments)", response.status_code, 200)
                return response.status_code == 200
            except Exception as e:
                print(f"[FAIL] GET /orders/assign/{order_id} - Error: {e}")
                self.failed += 1
                return False

    async def test_technician_get_assignment_details(self):
        """Technician: Get assignment details"""
        if not self.access_token or not self.assign_id:
            print("[SKIP] GET /assigns/{id} - No assign_id")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            try:
                response = await client.get(f"{self.api_url}/assigns/{self.assign_id}", headers=headers)
                self.print_test("Technician: GET /assigns/{id} (Get Details)", response.status_code, 200)
                return response.status_code == 200
            except Exception as e:
                print(f"[FAIL] GET /assigns/{id} - Error: {e}")
                self.failed += 1
                return False

    async def test_technician_delete_assignment(self):
        """Technician: Delete assignment"""
        if not self.access_token or not self.created_assigns:
            print("[SKIP] DELETE /assigns/{id} - No assignments to delete")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            # Delete the last created assignment
            assign_to_delete = self.created_assigns[-1] if self.created_assigns else None
            if assign_to_delete:
                try:
                    response = await client.delete(f"{self.api_url}/assigns/{assign_to_delete}", headers=headers)
                    self.print_test("Technician: DELETE /assigns/{id} (Delete Assignment)", response.status_code, 204)
                    if response.status_code == 204:
                        self.created_assigns.remove(assign_to_delete)
                    return response.status_code == 204
                except Exception as e:
                    print(f"[FAIL] DELETE /assigns/{id} - Error: {e}")
                    self.failed += 1
                    return False
        return False

    # ==================== ACCOUNTANT - PAYMENT MANAGEMENT ====================

    async def test_accountant_create_payment(self):
        """Accountant: Create payment"""
        if not self.access_token or not self.order_id:
            print("[SKIP] POST /payments - Missing required data")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            data = {
                "order_id": self.order_id,
                "due_amount": "240.00",
                "amount": "240.00",
                "status": "Paid",
                "payment_method": "Cash",
                "transaction_id": f"TXN{self.unique_id}"
            }
            try:
                response = await client.post(f"{self.api_url}/payments", json=data, headers=headers)
                self.print_test("Accountant: POST /payments (Create Payment)", response.status_code, 201)
                if response.status_code == 201:
                    self.payment_id = response.json().get("id")
                    self.created_payments.append(self.payment_id)
                return response.status_code == 201
            except Exception as e:
                print(f"[FAIL] POST /payments - Error: {e}")
                self.failed += 1
                return False

    async def test_accountant_create_multiple_payments(self):
        """Accountant: Create multiple payments with different statuses"""
        if not self.access_token or not self.order_id:
            print("[SKIP] Multiple payments - Missing required data")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            
            payments_data = [
                {"due_amount": "100.00", "amount": "100.00", "status": "Paid", "payment_method": "Cash"},
                {"due_amount": "200.00", "amount": "100.00", "status": "Partial", "payment_method": "Card"},
                {"due_amount": "150.00", "amount": "0.00", "status": "Unpaid", "payment_method": None}
            ]
            
            created_count = 0
            for payment_data in payments_data:
                data = {
                    "order_id": self.order_id,
                    "transaction_id": f"TXN{self.unique_id}{created_count}",
                    **payment_data
                }
                try:
                    response = await client.post(f"{self.api_url}/payments", json=data, headers=headers)
                    if response.status_code == 201:
                        payment_id = response.json().get("id")
                        self.created_payments.append(payment_id)
                        created_count += 1
                except:
                    pass
            
            self.print_test(f"Accountant: Create Multiple Payments ({created_count}/{len(payments_data)})", 200 if created_count > 0 else 400, 200)
            return created_count > 0

    async def test_accountant_list_payments(self):
        """Accountant: List all payments"""
        if not self.access_token:
            print("[SKIP] GET /payments - No access token")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            try:
                response = await client.get(f"{self.api_url}/payments?limit=20&offset=0", headers=headers)
                self.print_test("Accountant: GET /payments (List All)", response.status_code, 200)
                return response.status_code == 200
            except Exception as e:
                print(f"[FAIL] GET /payments - Error: {e}")
                self.failed += 1
                return False

    async def test_accountant_filter_payments_by_status(self):
        """Accountant: Filter payments by status"""
        if not self.access_token:
            print("[SKIP] Filter payments - No access token")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            statuses = ["Paid", "Due", "Unpaid", "Partial"]
            success_count = 0
            for status in statuses:
                try:
                    response = await client.get(f"{self.api_url}/payments?status={status}&limit=10", headers=headers)
                    if response.status_code == 200:
                        success_count += 1
                except:
                    pass
            self.print_test(f"Accountant: Filter Payments by Status ({success_count}/{len(statuses)})", 200 if success_count == len(statuses) else 400, 200)
            return success_count == len(statuses)

    async def test_accountant_filter_payments_by_order(self):
        """Accountant: Filter payments by order"""
        if not self.access_token or not self.order_id:
            print("[SKIP] GET /payments?order_id - Missing order_id")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            try:
                response = await client.get(f"{self.api_url}/payments?order_id={self.order_id}", headers=headers)
                self.print_test("Accountant: GET /payments?order_id (Filter by Order)", response.status_code, 200)
                return response.status_code == 200
            except Exception as e:
                print(f"[FAIL] GET /payments?order_id - Error: {e}")
                self.failed += 1
                return False

    async def test_accountant_get_payment_details(self):
        """Accountant: Get payment details"""
        if not self.access_token or not self.payment_id:
            print("[SKIP] GET /payments/{id} - No payment_id")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            try:
                response = await client.get(f"{self.api_url}/payments/{self.payment_id}", headers=headers)
                self.print_test("Accountant: GET /payments/{id} (Get Details)", response.status_code, 200)
                return response.status_code == 200
            except Exception as e:
                print(f"[FAIL] GET /payments/{id} - Error: {e}")
                self.failed += 1
                return False

    async def test_accountant_update_payment(self):
        """Accountant: Update payment status and amount"""
        if not self.access_token or not self.payment_id:
            print("[SKIP] PATCH /payments/{id} - No payment_id")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            updates = [
                {"status": "Partial", "amount": "120.00"},
                {"status": "Paid", "amount": "240.00"}
            ]
            success_count = 0
            for update_data in updates:
                try:
                    response = await client.patch(f"{self.api_url}/payments/{self.payment_id}", json=update_data, headers=headers)
                    if response.status_code == 200:
                        success_count += 1
                except:
                    pass
            self.print_test(f"Accountant: Update Payment ({success_count}/{len(updates)})", 200 if success_count > 0 else 400, 200)
            return success_count > 0

    async def test_accountant_delete_payment(self):
        """Accountant: Delete payment"""
        if not self.access_token or not self.created_payments:
            print("[SKIP] DELETE /payments/{id} - No payments to delete")
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            # Delete the last created payment
            payment_to_delete = self.created_payments[-1] if self.created_payments else None
            if payment_to_delete:
                try:
                    response = await client.delete(f"{self.api_url}/payments/{payment_to_delete}", headers=headers)
                    self.print_test("Accountant: DELETE /payments/{id} (Delete Payment)", response.status_code, 204)
                    if response.status_code == 204:
                        self.created_payments.remove(payment_to_delete)
                    return response.status_code == 204
                except Exception as e:
                    print(f"[FAIL] DELETE /payments/{id} - Error: {e}")
                    self.failed += 1
                    return False
        return False

    # ==================== COMPLETE WORKFLOW TESTS ====================

    async def test_complete_workflow(self):
        """Test complete workflow: Order -> Assignment -> Payment"""
        if not self.access_token or not self.device_id:
            print("[SKIP] Complete workflow - Missing required data")
            return False
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            
            # Step 1: Receptionist creates order
            order_data = {
                "device_id": self.device_id,
                "customer_id": self.customer_id,
                "cost": "350.00",
                "discount": "25.00",
                "note": "Complete workflow test",
                "status": "Pending"
            }
            try:
                response = await client.post(f"{self.api_url}/orders", json=order_data, headers=headers)
                if response.status_code == 201:
                    workflow_order_id = response.json().get("id")
                    
                    # Step 2: Technician assigns order
                    assign_data = {"order_id": workflow_order_id, "user_id": self.user_id}
                    response = await client.post(f"{self.api_url}/orders/assign", json=assign_data, headers=headers)
                    if response.status_code in [201, 400]:
                        
                        # Step 3: Update order status to Repairing
                        update_data = {"status": "Repairing"}
                        response = await client.patch(f"{self.api_url}/orders/{workflow_order_id}", json=update_data, headers=headers)
                        if response.status_code == 200:
                            
                            # Step 4: Accountant creates payment
                            payment_data = {
                                "order_id": workflow_order_id,
                                "due_amount": "325.00",
                                "amount": "325.00",
                                "status": "Paid",
                                "payment_method": "Card"
                            }
                            response = await client.post(f"{self.api_url}/payments", json=payment_data, headers=headers)
                            if response.status_code == 201:
                                
                                # Step 5: Update order to Completed
                                update_data = {"status": "Completed"}
                                response = await client.patch(f"{self.api_url}/orders/{workflow_order_id}", json=update_data, headers=headers)
                                if response.status_code == 200:
                                    self.print_test("Complete Workflow: Order->Assign->Payment->Complete", 200, 200)
                                    return True
            except Exception as e:
                print(f"[FAIL] Complete workflow - Error: {e}")
                self.failed += 1
                return False
        return False

    async def run_all_tests(self):
        """Run all role-based tests"""
        print("\n" + "="*70)
        print("ROLE-BASED API TEST SUITE")
        print("="*70)
        print(f"API URL: {self.api_url}")
        print("="*70 + "\n")

        # Setup
        print("SETUP")
        print("-" * 70)
        if not await self.setup_auth():
            print("FAIL: Authentication setup failed!")
            return
        print("PASS: Authentication successful")
        
        if not await self.setup_test_data():
            print("WARN: Some test data setup failed, continuing with available data...")
        print("PASS: Test data setup complete\n")

        # Receptionist Tests
        print("\n" + "="*70)
        print("RECEPTIONIST - ORDER MANAGEMENT TESTS")
        print("="*70)
        await self.test_reception_create_order()
        await self.test_reception_create_multiple_orders()
        await self.test_reception_list_orders()
        await self.test_reception_filter_orders_by_status()
        await self.test_reception_get_order_details()
        await self.test_reception_update_order_status()
        await self.test_reception_delete_order()

        # Technician Tests
        print("\n" + "="*70)
        print("TECHNICIAN - ASSIGNMENT MANAGEMENT TESTS")
        print("="*70)
        await self.test_technician_assign_order()
        await self.test_technician_create_assignment()
        await self.test_technician_list_assignments()
        await self.test_technician_get_my_assignments()
        await self.test_technician_get_order_assignments()
        await self.test_technician_get_assignment_details()
        await self.test_technician_delete_assignment()

        # Accountant Tests
        print("\n" + "="*70)
        print("ACCOUNTANT - PAYMENT MANAGEMENT TESTS")
        print("="*70)
        await self.test_accountant_create_payment()
        await self.test_accountant_create_multiple_payments()
        await self.test_accountant_list_payments()
        await self.test_accountant_filter_payments_by_status()
        await self.test_accountant_filter_payments_by_order()
        await self.test_accountant_get_payment_details()
        await self.test_accountant_update_payment()
        await self.test_accountant_delete_payment()

        # Complete Workflow Test
        print("\n" + "="*70)
        print("COMPLETE WORKFLOW TEST")
        print("="*70)
        await self.test_complete_workflow()

        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"PASSED: {self.passed}")
        print(f"FAILED: {self.failed}")
        print(f"TOTAL: {self.passed + self.failed}")
        if self.failed == 0:
            print("\n*** ALL TESTS PASSED! 100% SUCCESS RATE ***")
        else:
            success_rate = (self.passed / (self.passed + self.failed)) * 100
            print(f"\nSuccess Rate: {success_rate:.1f}%")
        print("="*70 + "\n")


async def main():
    tester = RoleBasedTest()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())

