import asyncio, sys, traceback

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.database import AsyncSessionLocal
from app.models.parcel import Parcel
from app.repositories.parcels import SqlAlchemyParcelRepository
from sqlalchemy import select

async def main():
    async with AsyncSessionLocal() as session:
        r = await session.execute(select(Parcel))
        items = r.scalars().all()
        repo = SqlAlchemyParcelRepository(session)
        for p in items:
            try:
                pub = repo._to_public(p)
                print(f"OK: {p.id}")
            except Exception as e:
                print(f"FAIL: {p.id}: {e}")

asyncio.run(main())
