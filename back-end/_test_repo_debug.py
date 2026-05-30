import asyncio, sys, traceback

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.repositories.parcels import SqlAlchemyParcelRepository
from app.database.database import AsyncSessionLocal

async def main():
    try:
        async with AsyncSessionLocal() as session:
            repo = SqlAlchemyParcelRepository(session)
            print("Executing list...")
            parcels = await asyncio.wait_for(repo.list(), timeout=5)
            print(f"Parcels: {len(parcels)}")
    except asyncio.TimeoutError:
        print("TIMEOUT: repo.list() hung")
    except Exception as e:
        traceback.print_exc()

asyncio.run(main())
