import asyncio, sys
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from app.database.database import AsyncSessionLocal
from sqlalchemy import text

async def main():
    async with AsyncSessionLocal() as session:
        r = await session.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='users'"))
        for row in r:
            print(f"{row.column_name}: {row.data_type}")

asyncio.run(main())
