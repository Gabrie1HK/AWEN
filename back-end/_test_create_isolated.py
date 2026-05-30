import asyncio, sys, traceback

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.services.parcels import ParcelService
from app.repositories.parcels import SqlAlchemyParcelRepository, SqlAlchemyTrackingRepository
from app.database.database import AsyncSessionLocal
from app.schemas.parcel import ParcelCreate

async def main():
    async with AsyncSessionLocal() as session:
        repo = SqlAlchemyParcelRepository(session)
        trepo = SqlAlchemyTrackingRepository(session)
        svc = ParcelService(repo, trepo)

        # Test just the next_id generator
        try:
            next_id = await svc._next_parcel_id()
            print(f"Next ID: {next_id}")
            guide = await svc._next_guide_number()
            print(f"Next Guide: {guide}")
        except Exception as e:
            traceback.print_exc()
            print(f"ID/GUIDE error: {type(e).__name__}: {e}")

asyncio.run(main())
