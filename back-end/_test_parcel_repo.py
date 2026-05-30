import asyncio, sys, traceback

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.repositories.parcels import SqlAlchemyParcelRepository
from app.database.database import AsyncSessionLocal

async def main():
    async with AsyncSessionLocal() as session:
        repo = SqlAlchemyParcelRepository(session)
        try:
            parcels = await repo.list()
            print(f"Parcels: {len(parcels)}")
        except Exception as e:
            traceback.print_exc()

asyncio.run(main())
