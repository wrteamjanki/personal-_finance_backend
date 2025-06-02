# init_db.py
import asyncio
from app.db.database import engine, Base

async def init_db():  # ← rename this to match your import
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
