"""Fix user password hash - re-hash password for user"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, text
from db import engine
from models.user import User
from utils.security import hash_password


async def fix_user_password(phone: str, new_password: str):
    """Re-hash password for a user"""
    async with engine.begin() as conn:
        # Get user ID
        result = await conn.execute(
            text("SELECT id FROM users WHERE phone = :phone"),
            {"phone": phone}
        )
        user_row = result.fetchone()
        
        if not user_row:
            print(f"User with phone {phone} not found")
            return False
        
        user_id = user_row[0]
        
        # Re-hash password
        new_hash = hash_password(new_password)
        
        # Update in database
        await conn.execute(
            text("UPDATE users SET password_hash = :hash WHERE id = :id"),
            {"hash": new_hash, "id": user_id}
        )
        
        print(f"Password updated for user {phone} (ID: {user_id})")
        return True


async def main():
    if len(sys.argv) < 3:
        print("Usage: python fix_user_password.py <phone> <password>")
        print("Example: python fix_user_password.py 9876543210 password123")
        sys.exit(1)
    
    phone = sys.argv[1]
    password = sys.argv[2]
    
    await fix_user_password(phone, password)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

