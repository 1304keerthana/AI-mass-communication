import asyncio
import sys
from pathlib import Path

# Ensure project root is on sys.path so `import app` works when running this script
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from app.database.session import engine
from app.database.base import Base
import app.models  # ensure model modules are imported so Base.metadata is populated

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Schema created via SQLAlchemy metadata.create_all")

if __name__ == '__main__':
    asyncio.run(main())
