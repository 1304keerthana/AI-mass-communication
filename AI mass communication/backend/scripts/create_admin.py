import asyncio
import sys
from pathlib import Path

# Add project root to path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from app.repositories.users import get_user_by_email, create_user
from app.auth.auth import get_password_hash
from app.schemas import RoleName

async def main():
    email = "admin@example.com"
    existing = await get_user_by_email(email)
    if existing:
        print("Admin user already exists:", existing.email)
        return
    hashed = get_password_hash("ChangeMe123!")
    user = await create_user("Admin", email, hashed, RoleName.admin)
    print("Created admin user:", user.email, user.id)

if __name__ == '__main__':
    asyncio.run(main())
