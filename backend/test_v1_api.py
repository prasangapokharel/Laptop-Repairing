import asyncio
import httpx

BASE_URL = "http://localhost:8000/v1"


async def test_v1_endpoints():
    print("Testing v1 API endpoints...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/roles")
        print(f"GET /v1/users/roles: {response.status_code}")
        if response.status_code == 200:
            roles = response.json()
            print(f"Roles found: {len(roles)}")
            for role in roles:
                print(f"  - {role.get('name')}: {role.get('description')}")
        
        response = await client.get(f"{BASE_URL}/devices/types")
        print(f"\nGET /v1/devices/types: {response.status_code}")
        if response.status_code == 200:
            types = response.json()
            print(f"Device Types found: {len(types)}")
        
        response = await client.get(f"{BASE_URL}/devices/brands")
        print(f"\nGET /v1/devices/brands: {response.status_code}")
        if response.status_code == 200:
            brands = response.json()
            print(f"Brands found: {len(brands)}")


if __name__ == "__main__":
    asyncio.run(test_v1_endpoints())

