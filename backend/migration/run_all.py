import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from alembic.config import Config
from alembic import command
from core.config import settings
from migration.seed import seed_database
from db import engine


def run_migrations():
    print("\n[INFO] Running database migrations...")
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url_sync)
    command.upgrade(alembic_cfg, "head")
    print("[SUCCESS] Migrations applied successfully!")


async def run_seed():
    print("\n[INFO] Seeding database...")
    try:
        await seed_database()
        print("[SUCCESS] Database seeding completed!")
    except Exception as e:
        print(f"[ERROR] Error seeding database: {e}")
        raise
    finally:
        await engine.dispose()


async def main():
    print("=" * 50)
    print("Database Migration and Seeding Script")
    print("=" * 50)
    
    try:
        run_migrations()
        await run_seed()
        print("\n" + "=" * 50)
        print("[SUCCESS] All operations completed successfully!")
        print("=" * 50)
    except Exception as e:
        print("\n" + "=" * 50)
        print(f"[ERROR] Operation failed: {e}")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

