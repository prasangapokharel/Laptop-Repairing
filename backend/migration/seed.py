import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from db import engine
from core.config import settings


async def seed_database():
    async with engine.begin() as conn:
        roles_data = [
            ("Admin", "System administrator with full access"),
            ("Technician", "Repair technician who handles device repairs"),
            ("Reception", "Reception staff who handles customer service"),
            ("Accountant", "Accountant who manages financial transactions"),
            ("Customer", "Customer who uses the service")
        ]
        
        device_types_data = [
            ("Laptop", "Laptop computers"),
            ("Desktop", "Desktop computers"),
            ("Tablet", "Tablet devices"),
            ("Smartphone", "Smartphone devices")
        ]
        
        brands_data = [
            "Apple", "Dell", "HP", "Lenovo", "Asus", 
            "Acer", "Samsung", "Microsoft", "Toshiba", "Sony"
        ]
        
        print("Seeding roles...")
        for name, description in roles_data:
            await conn.execute(
                text("""
                    INSERT INTO roles (name, description) 
                    VALUES (:name, :description)
                    ON DUPLICATE KEY UPDATE description = VALUES(description)
                """),
                {"name": name, "description": description}
            )
        
        print("Seeding device types...")
        for name, description in device_types_data:
            await conn.execute(
                text("""
                    INSERT INTO device_types (name, description) 
                    VALUES (:name, :description)
                    ON DUPLICATE KEY UPDATE description = VALUES(description)
                """),
                {"name": name, "description": description}
            )
        
        print("Seeding brands...")
        for name in brands_data:
            await conn.execute(
                text("""
                    INSERT INTO brands (name) 
                    VALUES (:name)
                    ON DUPLICATE KEY UPDATE name = VALUES(name)
                """),
                {"name": name}
            )
        
        await conn.commit()
        print("[SUCCESS] Seed data inserted successfully!")


async def main():
    try:
        await seed_database()
        print("\n[SUCCESS] Database seeding completed!")
    except Exception as e:
        print(f"\n[ERROR] Error seeding database: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

