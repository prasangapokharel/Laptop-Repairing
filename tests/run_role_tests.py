"""
Quick test runner for role-based tests
"""
import asyncio
from test_roles_complete import RoleBasedTest

async def main():
    print("Starting Role-Based API Tests...")
    tester = RoleBasedTest()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())

