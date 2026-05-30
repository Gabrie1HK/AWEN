import asyncio, sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.database import AsyncSessionLocal
from app.models.user import User
from sqlalchemy import select

async def main():
    print("Connecting...")
    async with AsyncSessionLocal() as session:
        print("Querying...")
        r = await session.execute(select(User))
        users = r.scalars().all()
        print(f"Users: {len(users)}")

asyncio.run(main())
print("Done")
