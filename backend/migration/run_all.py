import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from alembic.config import Config
from alembic import command
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError
from core.config import settings
from migration.seed import seed_database
from db import engine


def check_migrations_needed():
    """Check if migrations are already applied"""
    sync_engine = None
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url_sync)
        
        sync_engine = create_engine(settings.database_url_sync)
        
        inspector = inspect(sync_engine)
        tables = inspector.get_table_names()
        
        if "alembic_version" not in tables:
            print("[INFO] Database not initialized, migrations needed")
            return True
        
        script = ScriptDirectory.from_config(alembic_cfg)
        head_revision = script.get_current_head()
        
        with sync_engine.connect() as conn:
            context = MigrationContext.configure(conn)
            current_revision = context.get_current_revision()
        
        if current_revision != head_revision:
            print(f"[INFO] Migrations needed: current={current_revision}, head={head_revision}")
            return True
        else:
            print(f"[OK] Migrations already applied (revision: {current_revision})")
            return False
            
    except OperationalError as e:
        print(f"[ERROR] Database connection failed: {e}")
        print("[INFO] Please check database credentials in .env file")
        raise
    except Exception as e:
        print(f"[WARNING] Could not check migration status: {e}")
        print("[INFO] Will attempt to run migrations...")
        return True
    finally:
        if sync_engine:
            sync_engine.dispose()


def run_migrations():
    """Run database migrations if needed"""
    if not check_migrations_needed():
        return
    
    print("\n[INFO] Running database migrations...")
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url_sync)
        command.upgrade(alembic_cfg, "head")
        print("[SUCCESS] Migrations applied successfully!")
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        raise


async def check_seed_needed():
    """Check if database already has seed data"""
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT COUNT(*) as count FROM roles"))
            row = result.fetchone()
            if row and row[0] > 0:
                print("[OK] Database already seeded")
                return False
            return True
    except OperationalError as e:
        print(f"[ERROR] Database connection failed: {e}")
        raise
    except Exception as e:
        print(f"[WARNING] Could not check seed status: {e}")
        return True


async def run_seed():
    """Seed database if needed"""
    if not await check_seed_needed():
        return
    
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
    """Main function to run migrations and seeding"""
    print("=" * 50)
    print("Database Migration and Seeding Script")
    print("=" * 50)
    
    try:
        run_migrations()
        await run_seed()
        print("\n" + "=" * 50)
        print("[SUCCESS] All operations completed successfully!")
        print("=" * 50)
        return 0
    except Exception as e:
        print("\n" + "=" * 50)
        print(f"[ERROR] Operation failed: {e}")
        print("=" * 50)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

