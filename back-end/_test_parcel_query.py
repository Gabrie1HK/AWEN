import asyncio, sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.database import AsyncSessionLocal
from app.models.parcel import Parcel
from sqlalchemy import select

async def main():
    async with AsyncSessionLocal() as session:
        r = await session.execute(select(Parcel))
        items = r.scalars().all()
        print(f"Count: {len(items)}")
        for p in items:
            print(f"ID={p.id} guide={p.guide} status={p.status} origin_branch={p.origin_branch}")

asyncio.run(main())
