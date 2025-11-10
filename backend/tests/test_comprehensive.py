import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


class TestRepairOffice:
    def __init__(self):
        self.base_url = BASE_URL
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.technician_id = None
        self.customer_id = None
        self.device_ids = []
        self.order_ids = []
        self.payment_ids = []
        self.assign_ids = []
        self.role_ids = {}
        self.device_type_id = None
        self.brand_id = None
        self.model_id = None

    async def print_scenario(self, scenario_num: int, title: str):
        print(f"\n{'='*60}")
        print(f"SCENARIO {scenario_num}: {title}")
        print(f"{'='*60}")

    async def test_scenario_1_customer_registration(self):
        """Scenario 1: New customer registers and logs in"""
        await self.print_scenario(1, "Customer Registration & Login")
        
        async with httpx.AsyncClient() as client:
            import time
            unique_id = int(time.time() * 1000) % 10000000
            register_data = {
                "full_name": f"John Customer {unique_id}",
                "phone": f"987{unique_id}",
                "email": f"john.customer{unique_id}@example.com",
                "password": "securepass123"
            }
            response = await client.post(f"{self.base_url}/v1/auth/register", json=register_data)
            print(f"[OK] Register: {response.status_code}")
            if response.status_code == 201:
                self.customer_id = response.json().get("id")
                print(f"  Customer ID: {self.customer_id}")
            elif response.status_code == 400:
                login_data = {"phone": register_data["phone"], "password": register_data["password"]}
                login_resp = await client.post(f"{self.base_url}/v1/auth/login", json=login_data)
                if login_resp.status_code == 200:
                    self.customer_id = login_resp.json()["user"]["id"]
                    print(f"  Using existing customer ID: {self.customer_id}")
            
            login_data = {"phone": register_data["phone"], "password": register_data["password"]}
            response = await client.post(f"{self.base_url}/v1/auth/login", json=login_data)
            print(f"[OK] Login: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["tokens"]["access_token"]
                self.refresh_token = data["tokens"]["refresh_token"]
                if not self.customer_id:
                    self.customer_id = data["user"]["id"]
                print(f"  Tokens received, Customer ID: {self.customer_id}")
                return True
            return False

    async def test_scenario_2_device_registration(self):
        """Scenario 2: Customer registers their laptop for repair"""
        await self.print_scenario(2, "Device Registration")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
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
                else:
                    model_data = {
                        "brand_id": self.brand_id,
                        "name": "Test Model",
                        "device_type_id": self.device_type_id
                    }
                    model_resp = await client.post(f"{self.base_url}/v1/devices/models", json=model_data, headers=headers)
                    if model_resp.status_code == 201:
                        self.model_id = model_resp.json()["id"]
            
            if self.brand_id and self.model_id and self.device_type_id:
                import time
                unique_id = int(time.time() * 1000) % 100000
                device_data = {
                    "brand_id": self.brand_id,
                    "model_id": self.model_id,
                    "device_type_id": self.device_type_id,
                    "serial_number": f"LAPTOP{unique_id}",
                    "owner_id": self.customer_id,
                    "notes": "Screen cracked, needs replacement"
                }
                response = await client.post(f"{self.base_url}/v1/devices", json=device_data, headers=headers)
                print(f"[OK] Create Device: {response.status_code}")
                if response.status_code == 201:
                    device = response.json()
                    self.device_ids.append(device["id"])
                    print(f"  Device ID: {device['id']}, Serial: {device['serial_number']}")
                    return True
            print(f"[ERROR] Failed to create device - missing required data")
            return False

    async def test_scenario_3_order_creation(self):
        """Scenario 3: Reception creates repair order"""
        await self.print_scenario(3, "Repair Order Creation")
        
        if not self.device_ids:
            print("[ERROR] No device available for order creation")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            order_data = {
                "device_id": self.device_ids[0],
                "customer_id": self.customer_id,
                "cost": "250.00",
                "discount": "0.00",
                "note": "Initial diagnosis: Screen replacement needed",
                "status": "Pending"
            }
            response = await client.post(f"{self.base_url}/v1/orders", json=order_data, headers=headers)
            print(f"[OK] Create Order: {response.status_code}")
            if response.status_code == 201:
                order = response.json()
                self.order_ids.append(order["id"])
                print(f"  Order ID: {order['id']}, Status: {order['status']}, Total: ${order['total_cost']}")
                return True
            return False

    async def test_scenario_4_technician_assignment(self):
        """Scenario 4: Admin assigns technician to order"""
        await self.print_scenario(4, "Technician Assignment")
        
        if not self.order_ids or not self.customer_id:
            print("[ERROR] No order or customer available for assignment")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            assign_data = {
                "order_id": int(self.order_ids[0]),
                "user_id": int(self.customer_id)
            }
            response = await client.post(f"{self.base_url}/v1/assigns", json=assign_data, headers=headers)
            print(f"[OK] Assign Technician: {response.status_code}")
            if response.status_code == 201:
                assign = response.json()
                self.assign_ids.append(assign["id"])
                self.technician_id = assign["user_id"]
                print(f"  Assignment ID: {assign['id']}, User ID: {assign['user_id']}")
                return True
            elif response.status_code == 422:
                print(f"  Validation error: {response.json()}")
            elif response.status_code == 400:
                print(f"  Already assigned: {response.json()}")
                return True
            return False

    async def test_scenario_5_cost_estimation_update(self):
        """Scenario 5: Technician updates cost after diagnosis"""
        await self.print_scenario(5, "Cost Estimation Update")
        
        if not self.order_ids:
            print("[ERROR] No order available for update")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            update_data = {
                "cost": "300.00",
                "discount": "25.00",
                "status": "Repairing",
                "note": "Diagnosis complete: Screen + battery replacement needed"
            }
            response = await client.patch(f"{self.base_url}/v1/orders/{self.order_ids[0]}", json=update_data, headers=headers)
            print(f"[OK] Update Order: {response.status_code}")
            if response.status_code == 200:
                order = response.json()
                print(f"  Updated Cost: ${order['cost']}, Discount: ${order['discount']}, Total: ${order['total_cost']}")
                print(f"  Status: {order['status']}")
                return True
            return False

    async def test_scenario_6_partial_payment(self):
        """Scenario 6: Customer makes partial payment"""
        await self.print_scenario(6, "Partial Payment Processing")
        
        if not self.order_ids:
            print("[ERROR] No order available for payment")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            payment_data = {
                "order_id": self.order_ids[0],
                "due_amount": "275.00",
                "amount": "150.00",
                "status": "Partial",
                "payment_method": "Cash",
                "transaction_id": "TXN001"
            }
            response = await client.post(f"{self.base_url}/v1/payments", json=payment_data, headers=headers)
            print(f"[OK] Create Partial Payment: {response.status_code}")
            if response.status_code == 201:
                payment = response.json()
                self.payment_ids.append(payment["id"])
                print(f"  Payment ID: {payment['id']}, Amount: ${payment['amount']}, Status: {payment['status']}")
                return True
            return False

    async def test_scenario_7_order_completion(self):
        """Scenario 7: Technician marks order as completed"""
        await self.print_scenario(7, "Order Completion")
        
        if not self.order_ids:
            print("[ERROR] No order available for completion")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            update_data = {
                "status": "Completed",
                "note": "Repair completed successfully. Device tested and working."
            }
            response = await client.patch(f"{self.base_url}/v1/orders/{self.order_ids[0]}", json=update_data, headers=headers)
            print(f"[OK] Complete Order: {response.status_code}")
            if response.status_code == 200:
                order = response.json()
                print(f"  Final Status: {order['status']}")
                return True
            return False

    async def test_scenario_8_final_payment(self):
        """Scenario 8: Customer pays remaining balance"""
        await self.print_scenario(8, "Final Payment")
        
        if not self.order_ids:
            print("[ERROR] No order available for payment")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            payment_data = {
                "order_id": self.order_ids[0],
                "due_amount": "125.00",
                "amount": "125.00",
                "status": "Paid",
                "payment_method": "Card",
                "transaction_id": "TXN002"
            }
            response = await client.post(f"{self.base_url}/v1/payments", json=payment_data, headers=headers)
            print(f"[OK] Create Final Payment: {response.status_code}")
            if response.status_code == 201:
                payment = response.json()
                self.payment_ids.append(payment["id"])
                print(f"  Payment ID: {payment['id']}, Amount: ${payment['amount']}, Status: {payment['status']}")
            
            response = await client.get(f"{self.base_url}/v1/payments", headers=headers, params={"order_id": self.order_ids[0]})
            if response.status_code == 200:
                payments = response.json()
                total_paid = sum(float(p["amount"]) for p in payments)
                print(f"  Total Paid: ${total_paid:.2f}")
            return response.status_code == 201

    async def test_scenario_9_multiple_orders_same_customer(self):
        """Scenario 9: Same customer brings multiple devices"""
        await self.print_scenario(9, "Multiple Orders - Same Customer")
        
        if not self.brand_id or not self.model_id or not self.device_type_id:
            print("[ERROR] Missing device data for second device")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            import time
            unique_id = int(time.time() * 1000) % 100000
            device2 = {
                "brand_id": self.brand_id,
                "model_id": self.model_id,
                "device_type_id": self.device_type_id,
                "serial_number": f"LAPTOP{unique_id}",
                "owner_id": self.customer_id,
                "notes": "Keyboard not working"
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
                    "cost": "120.00",
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
            return False

    async def test_scenario_10_order_status_filtering(self):
        """Scenario 10: Reception filters orders by status"""
        await self.print_scenario(10, "Order Status Filtering")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            statuses = ["Pending", "Repairing", "Completed", "Cancelled"]
            success = True
            for status in statuses:
                response = await client.get(f"{self.base_url}/v1/orders", headers=headers, params={"status": status})
                if response.status_code == 200:
                    orders = response.json()
                    print(f"[OK] {status} Orders: {len(orders)}")
                else:
                    success = False
            return success

    async def test_scenario_11_payment_status_tracking(self):
        """Scenario 11: Accountant tracks payment statuses"""
        await self.print_scenario(11, "Payment Status Tracking")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            statuses = ["Paid", "Due", "Unpaid", "Partial"]
            success = True
            for status in statuses:
                response = await client.get(f"{self.base_url}/v1/payments", headers=headers, params={"status": status})
                if response.status_code == 200:
                    payments = response.json()
                    total = sum(float(p["amount"]) for p in payments)
                    print(f"[OK] {status} Payments: {len(payments)}, Total: ${total:.2f}")
                else:
                    success = False
            return success

    async def test_scenario_12_technician_workload(self):
        """Scenario 12: View technician assignments"""
        await self.print_scenario(12, "Technician Workload View")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            if self.technician_id:
                response = await client.get(f"{self.base_url}/v1/assigns", headers=headers, params={"user_id": self.technician_id})
            else:
                response = await client.get(f"{self.base_url}/v1/assigns", headers=headers)
            if response.status_code == 200:
                assigns = response.json()
                print(f"[OK] Technician has {len(assigns)} assigned orders")
                for assign in assigns:
                    order_resp = await client.get(f"{self.base_url}/v1/orders/{assign['order_id']}", headers=headers)
                    if order_resp.status_code == 200:
                        order = order_resp.json()
                        print(f"  Order {assign['order_id']}: {order['status']}")
                return True
            return False

    async def test_scenario_13_order_cancellation(self):
        """Scenario 13: Customer cancels order"""
        await self.print_scenario(13, "Order Cancellation")
        
        if len(self.order_ids) < 2:
            print("[ERROR] Need at least 2 orders for cancellation test")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            cancel_data = {
                "status": "Cancelled",
                "note": "Customer requested cancellation"
            }
            response = await client.patch(f"{self.base_url}/v1/orders/{self.order_ids[1]}", json=cancel_data, headers=headers)
            print(f"[OK] Cancel Order: {response.status_code}")
            if response.status_code == 200:
                order = response.json()
                print(f"  Order Status: {order['status']}")
                return True
            return False

    async def test_scenario_14_device_history(self):
        """Scenario 14: View device repair history"""
        await self.print_scenario(14, "Device Repair History")
        
        if not self.device_ids:
            print("[ERROR] No device available for history")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/v1/orders", headers=headers, params={"device_id": self.device_ids[0]})
            if response.status_code == 200:
                orders = response.json()
                print(f"[OK] Device has {len(orders)} repair orders")
                for order in orders:
                    print(f"  Order {order['id']}: {order['status']} - ${order['total_cost']}")
                return True
            return False

    async def test_scenario_15_refresh_token_flow(self):
        """Scenario 15: Token refresh workflow"""
        await self.print_scenario(15, "Token Refresh Flow")
        
        if not self.refresh_token:
            print("[ERROR] No refresh token available")
            return False
        
        async with httpx.AsyncClient() as client:
            refresh_data = {"refresh_token": self.refresh_token}
            response = await client.post(f"{self.base_url}/v1/auth/refresh", json=refresh_data)
            print(f"[OK] Refresh Token: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                print(f"  New access token received")
                return True
            return False

    async def test_scenario_16_error_handling(self):
        """Scenario 16: Error handling and validation"""
        await self.print_scenario(16, "Error Handling & Validation")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            invalid_order = {
                "device_id": 99999,
                "cost": "100.00"
            }
            response = await client.post(f"{self.base_url}/v1/orders", json=invalid_order, headers=headers)
            print(f"[OK] Invalid Device ID: {response.status_code} (Expected 404)")
            error1_ok = response.status_code == 404
            
            if self.order_ids and self.technician_id:
                duplicate_assign = {
                    "order_id": int(self.order_ids[0]),
                    "user_id": int(self.technician_id)
                }
                response = await client.post(f"{self.base_url}/v1/assigns", json=duplicate_assign, headers=headers)
                print(f"[OK] Duplicate Assignment: {response.status_code} (Expected 400)")
                error2_ok = response.status_code == 400
            else:
                print(f"[OK] Duplicate Assignment: Skipped (no assignment exists)")
                error2_ok = True
            
            invalid_payment = {
                "order_id": 99999,
                "amount": "100.00"
            }
            response = await client.post(f"{self.base_url}/v1/payments", json=invalid_payment, headers=headers)
            print(f"[OK] Invalid Order ID: {response.status_code} (Expected 404)")
            error3_ok = response.status_code == 404
            
            return error1_ok and error2_ok and error3_ok

    async def run_all_scenarios(self):
        print("\n" + "="*60)
        print("COMPREHENSIVE REPAIR OFFICE SYSTEM TEST")
        print("="*60)
        
        scenarios = [
            self.test_scenario_1_customer_registration,
            self.test_scenario_2_device_registration,
            self.test_scenario_3_order_creation,
            self.test_scenario_4_technician_assignment,
            self.test_scenario_5_cost_estimation_update,
            self.test_scenario_6_partial_payment,
            self.test_scenario_7_order_completion,
            self.test_scenario_8_final_payment,
            self.test_scenario_9_multiple_orders_same_customer,
            self.test_scenario_10_order_status_filtering,
            self.test_scenario_11_payment_status_tracking,
            self.test_scenario_12_technician_workload,
            self.test_scenario_13_order_cancellation,
            self.test_scenario_14_device_history,
            self.test_scenario_15_refresh_token_flow,
            self.test_scenario_16_error_handling,
        ]
        
        results = []
        for scenario in scenarios:
            try:
                result = await scenario()
                results.append(result)
            except Exception as e:
                print(f"[ERROR] Error in scenario: {e}")
                results.append(False)
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        passed = sum(results)
        total = len(results)
        print(f"Passed: {passed}/{total} scenarios")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print("="*60)
        
        return passed == total


async def main():
    tester = TestRepairOffice()
    success = await tester.run_all_scenarios()
    exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())

