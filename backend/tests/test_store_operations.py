import asyncio
import httpx
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Get BASE_URL from environment or use default
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


class StoreOperationsTest:
    def __init__(self):
        self.base_url = BASE_URL
        self.access_token = None
        self.refresh_token = None
        self.customer_id = None
        self.technician_id = None
        self.device_ids = []
        self.order_ids = []
        self.payment_ids = []
        self.device_type_id = None
        self.brand_id = None
        self.model_id = None

    async def print_test(self, test_name: str):
        print(f"\n{'='*60}")
        print(f"TEST: {test_name}")
        print(f"{'='*60}")

    async def setup_store(self):
        """Setup: Create customer, device, and initial order"""
        await self.print_test("Store Setup - Customer & Device Registration")
        
        async with httpx.AsyncClient() as client:
            import time
            unique_id = int(time.time() * 1000) % 10000000
            
            register_data = {
                "full_name": f"Store Customer {unique_id}",
                "phone": f"999{unique_id}",
                "email": f"customer{unique_id}@store.com",
                "password": "storepass123"
            }
            response = await client.post(f"{self.base_url}/v1/auth/register", json=register_data)
            if response.status_code == 201:
                self.customer_id = response.json().get("id")
                print(f"[OK] Customer registered: ID {self.customer_id}")
            
            login_data = {"phone": register_data["phone"], "password": register_data["password"]}
            response = await client.post(f"{self.base_url}/v1/auth/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["tokens"]["access_token"]
                self.refresh_token = data["tokens"]["refresh_token"]
                if not self.customer_id:
                    self.customer_id = data["user"]["id"]
                print(f"[OK] Customer logged in: ID {self.customer_id}")
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            types_resp = await client.get(f"{self.base_url}/v1/devices/types", headers=headers)
            if types_resp.status_code == 200 and len(types_resp.json()) > 0:
                self.device_type_id = types_resp.json()[0]["id"]
            
            brands_resp = await client.get(f"{self.base_url}/v1/devices/brands", headers=headers)
            if brands_resp.status_code == 200 and len(brands_resp.json()) > 0:
                self.brand_id = brands_resp.json()[0]["id"]
            
            if self.brand_id and self.device_type_id:
                models_resp = await client.get(f"{self.base_url}/v1/devices/models", headers=headers)
                if models_resp.status_code == 200 and len(models_resp.json()) > 0:
                    self.model_id = models_resp.json()[0]["id"]
            
            if self.brand_id and self.model_id and self.device_type_id:
                device_data = {
                    "brand_id": self.brand_id,
                    "model_id": self.model_id,
                    "device_type_id": self.device_type_id,
                    "serial_number": f"STORE{unique_id}",
                    "owner_id": self.customer_id,
                    "notes": "Customer device for repair"
                }
                response = await client.post(f"{self.base_url}/v1/devices", json=device_data, headers=headers)
                if response.status_code == 201:
                    device = response.json()
                    self.device_ids.append(device["id"])
                    print(f"[OK] Device registered: ID {device['id']}, Serial: {device['serial_number']}")
            
            return self.customer_id and len(self.device_ids) > 0

    async def test_order_creation_flow(self):
        """Test: Reception creates repair order"""
        await self.print_test("Order Creation - Reception Workflow")
        
        if not self.device_ids:
            print("[ERROR] No device available")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            order_data = {
                "device_id": self.device_ids[0],
                "customer_id": self.customer_id,
                "cost": "350.00",
                "discount": "0.00",
                "note": "Initial diagnosis: Screen replacement needed",
                "status": "Pending"
            }
            response = await client.post(f"{self.base_url}/v1/orders", json=order_data, headers=headers)
            print(f"[OK] Order Created: {response.status_code}")
            if response.status_code == 201:
                order = response.json()
                self.order_ids.append(order["id"])
                print(f"  Order ID: {order['id']}")
                print(f"  Status: {order['status']}")
                print(f"  Cost: ${order['cost']}")
                print(f"  Total: ${order['total_cost']}")
                return True
            return False

    async def test_technician_assignment(self):
        """Test: Admin assigns technician"""
        await self.print_test("Technician Assignment - Admin Workflow")
        
        if not self.order_ids:
            print("[ERROR] No order available")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            assign_data = {
                "order_id": int(self.order_ids[0]),
                "user_id": int(self.customer_id)
            }
            response = await client.post(f"{self.base_url}/v1/assigns", json=assign_data, headers=headers)
            print(f"[OK] Technician Assigned: {response.status_code}")
            if response.status_code == 201:
                assign = response.json()
                self.technician_id = assign["user_id"]
                print(f"  Assignment ID: {assign['id']}")
                print(f"  Technician ID: {assign['user_id']}")
                return True
            return False

    async def test_cost_estimation_update(self):
        """Test: Technician updates cost after diagnosis"""
        await self.print_test("Cost Estimation - Technician Workflow")
        
        if not self.order_ids:
            print("[ERROR] No order available")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            update_data = {
                "cost": "450.00",
                "discount": "50.00",
                "status": "Repairing",
                "note": "Diagnosis complete: Screen + battery replacement needed. Customer approved."
            }
            response = await client.patch(f"{self.base_url}/v1/orders/{self.order_ids[0]}", json=update_data, headers=headers)
            print(f"[OK] Order Updated: {response.status_code}")
            if response.status_code == 200:
                order = response.json()
                print(f"  Updated Cost: ${order['cost']}")
                print(f"  Discount: ${order['discount']}")
                print(f"  Total Cost: ${order['total_cost']}")
                print(f"  Status: {order['status']}")
                return True
            return False

    async def test_payment_due_creation(self):
        """Test: Reception creates payment record with due amount"""
        await self.print_test("Payment Creation - Due Amount Tracking")
        
        if not self.order_ids:
            print("[ERROR] No order available")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            payment_data = {
                "order_id": self.order_ids[0],
                "due_amount": "400.00",
                "amount": "0.00",
                "status": "Due",
                "payment_method": None,
                "transaction_id": None
            }
            response = await client.post(f"{self.base_url}/v1/payments", json=payment_data, headers=headers)
            print(f"[OK] Payment Created (Due): {response.status_code}")
            if response.status_code == 201:
                payment = response.json()
                self.payment_ids.append(payment["id"])
                print(f"  Payment ID: {payment['id']}")
                print(f"  Due Amount: ${payment['due_amount']}")
                print(f"  Amount Paid: ${payment['amount']}")
                print(f"  Status: {payment['status']}")
                return True
            return False

    async def test_partial_payment(self):
        """Test: Customer makes partial payment"""
        await self.print_test("Partial Payment - Customer Payment Flow")
        
        if not self.order_ids:
            print("[ERROR] No order available")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            payment_data = {
                "order_id": self.order_ids[0],
                "due_amount": "400.00",
                "amount": "200.00",
                "status": "Partial",
                "payment_method": "Cash",
                "transaction_id": f"TXN{int(datetime.now().timestamp())}"
            }
            response = await client.post(f"{self.base_url}/v1/payments", json=payment_data, headers=headers)
            print(f"[OK] Partial Payment: {response.status_code}")
            if response.status_code == 201:
                payment = response.json()
                self.payment_ids.append(payment["id"])
                print(f"  Payment ID: {payment['id']}")
                print(f"  Amount Paid: ${payment['amount']}")
                print(f"  Remaining Due: ${float(payment['due_amount']) - float(payment['amount'])}")
                print(f"  Status: {payment['status']}")
                
                response = await client.get(f"{self.base_url}/v1/payments", headers=headers, params={"order_id": self.order_ids[0]})
                if response.status_code == 200:
                    payments = response.json()
                    total_paid = sum(float(p["amount"]) for p in payments)
                    print(f"  Total Paid So Far: ${total_paid:.2f}")
                return True
            return False

    async def test_final_payment_completion(self):
        """Test: Customer pays remaining balance"""
        await self.print_test("Final Payment - Complete Payment Flow")
        
        if not self.order_ids:
            print("[ERROR] No order available")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            payment_data = {
                "order_id": self.order_ids[0],
                "due_amount": "200.00",
                "amount": "200.00",
                "status": "Paid",
                "payment_method": "Card",
                "transaction_id": f"TXN{int(datetime.now().timestamp())}"
            }
            response = await client.post(f"{self.base_url}/v1/payments", json=payment_data, headers=headers)
            print(f"[OK] Final Payment: {response.status_code}")
            if response.status_code == 201:
                payment = response.json()
                self.payment_ids.append(payment["id"])
                print(f"  Payment ID: {payment['id']}")
                print(f"  Amount Paid: ${payment['amount']}")
                print(f"  Status: {payment['status']}")
                
                response = await client.get(f"{self.base_url}/v1/payments", headers=headers, params={"order_id": self.order_ids[0]})
                if response.status_code == 200:
                    payments = response.json()
                    total_paid = sum(float(p["amount"]) for p in payments)
                    total_due = sum(float(p["due_amount"]) for p in payments)
                    print(f"  Total Paid: ${total_paid:.2f}")
                    print(f"  Total Due: ${total_due:.2f}")
                    print(f"  Balance: ${total_due - total_paid:.2f}")
                return True
            return False

    async def test_order_completion(self):
        """Test: Technician marks order as completed"""
        await self.print_test("Order Completion - Technician Workflow")
        
        if not self.order_ids:
            print("[ERROR] No order available")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            update_data = {
                "status": "Completed",
                "note": "Repair completed successfully. Device tested and working perfectly."
            }
            response = await client.patch(f"{self.base_url}/v1/orders/{self.order_ids[0]}", json=update_data, headers=headers)
            print(f"[OK] Order Completed: {response.status_code}")
            if response.status_code == 200:
                order = response.json()
                print(f"  Final Status: {order['status']}")
                print(f"  Note: {order['note']}")
                return True
            return False

    async def test_payment_status_tracking(self):
        """Test: Accountant tracks payment statuses"""
        await self.print_test("Payment Status Tracking - Accountant Workflow")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            statuses = ["Paid", "Due", "Unpaid", "Partial"]
            for status in statuses:
                response = await client.get(f"{self.base_url}/v1/payments", headers=headers, params={"status": status})
                if response.status_code == 200:
                    payments = response.json()
                    total = sum(float(p["amount"]) for p in payments)
                    print(f"[OK] {status} Payments: {len(payments)} records, Total: ${total:.2f}")

    async def test_order_status_filtering(self):
        """Test: Reception filters orders by status"""
        await self.print_test("Order Status Filtering - Reception Workflow")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            statuses = ["Pending", "Repairing", "Completed", "Cancelled"]
            for status in statuses:
                response = await client.get(f"{self.base_url}/v1/orders", headers=headers, params={"status": status})
                if response.status_code == 200:
                    orders = response.json()
                    print(f"[OK] {status} Orders: {len(orders)}")

    async def test_multiple_orders_same_customer(self):
        """Test: Same customer brings multiple devices"""
        await self.print_test("Multiple Orders - Same Customer")
        
        if not self.brand_id or not self.model_id or not self.device_type_id:
            print("[ERROR] Missing device data")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            import time
            unique_id = int(time.time() * 1000) % 100000
            
            device2 = {
                "brand_id": self.brand_id,
                "model_id": self.model_id,
                "device_type_id": self.device_type_id,
                "serial_number": f"STORE2{unique_id}",
                "owner_id": self.customer_id,
                "notes": "Second device from same customer"
            }
            response = await client.post(f"{self.base_url}/v1/devices", json=device2, headers=headers)
            if response.status_code == 201:
                device = response.json()
                self.device_ids.append(device["id"])
                print(f"[OK] Device 2 Created: ID {device['id']}")
            
            if len(self.device_ids) > 1:
                order2 = {
                    "device_id": self.device_ids[1],
                    "customer_id": self.customer_id,
                    "cost": "150.00",
                    "discount": "10.00",
                    "status": "Pending"
                }
                response = await client.post(f"{self.base_url}/v1/orders", json=order2, headers=headers)
                if response.status_code == 201:
                    order = response.json()
                    self.order_ids.append(order["id"])
                    print(f"[OK] Order 2 Created: ID {order['id']}, Total: ${order['total_cost']}")
            
            response = await client.get(f"{self.base_url}/v1/orders", headers=headers, params={"customer_id": self.customer_id})
            if response.status_code == 200:
                orders = response.json()
                print(f"[OK] Customer has {len(orders)} orders")
                for order in orders:
                    print(f"  Order {order['id']}: {order['status']} - ${order['total_cost']}")
            return True

    async def test_payment_flexibility(self):
        """Test: Payment flexibility - multiple payment methods and scenarios"""
        await self.print_test("Payment Flexibility - Multiple Scenarios")
        
        if len(self.order_ids) < 2:
            print("[ERROR] Need at least 2 orders")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            order_id = self.order_ids[1]
            
            scenarios = [
                {
                    "name": "Full Payment - Cash",
                    "data": {
                        "order_id": order_id,
                        "due_amount": "140.00",
                        "amount": "140.00",
                        "status": "Paid",
                        "payment_method": "Cash",
                        "transaction_id": f"CASH{int(datetime.now().timestamp())}"
                    }
                },
                {
                    "name": "Full Payment - Card",
                    "data": {
                        "order_id": order_id,
                        "due_amount": "0.00",
                        "amount": "0.00",
                        "status": "Paid",
                        "payment_method": "Card",
                        "transaction_id": f"CARD{int(datetime.now().timestamp())}"
                    }
                }
            ]
            
            for scenario in scenarios:
                response = await client.post(f"{self.base_url}/v1/payments", json=scenario["data"], headers=headers)
                print(f"[OK] {scenario['name']}: {response.status_code}")
                if response.status_code == 201:
                    payment = response.json()
                    print(f"  Payment ID: {payment['id']}, Method: {payment['payment_method']}, Status: {payment['status']}")

    async def run_all_tests(self):
        print("\n" + "="*60)
        print("STORE OPERATIONS COMPREHENSIVE TEST")
        print("="*60)
        
        tests = [
            self.setup_store,
            self.test_order_creation_flow,
            self.test_technician_assignment,
            self.test_cost_estimation_update,
            self.test_payment_due_creation,
            self.test_partial_payment,
            self.test_final_payment_completion,
            self.test_order_completion,
            self.test_payment_status_tracking,
            self.test_order_status_filtering,
            self.test_multiple_orders_same_customer,
            self.test_payment_flexibility,
        ]
        
        results = []
        for test in tests:
            try:
                result = await test()
                results.append(result if result is not None else True)
            except Exception as e:
                print(f"[ERROR] Test failed: {e}")
                results.append(False)
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        passed = sum(results)
        total = len(results)
        print(f"Passed: {passed}/{total} tests")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print("="*60)
        
        return passed == total


async def main():
    tester = StoreOperationsTest()
    success = await tester.run_all_tests()
    exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())

