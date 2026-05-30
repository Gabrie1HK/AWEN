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

        payload = ParcelCreate(
            sender="Juan Perez",
            senderId="V-12345678",
            senderPhone="+58 414 111 2233",
            recipient="Maria Lopez",
            recipientId="V-87654321",
            recipientPhone="+58 416 999 8877",
            recipientAddress="Calle 5, Urb. Las Flores, Maracaibo",
            originLat=10.16, originLng=-68.0,
            destinationLat=10.5, destinationLng=-66.9,
            weight=2.5,
            dimensions="30x20x15 cm",
            declaredValue=50000,
            description="Documentos",
        )
        try:
            result = await svc.create(payload)
            print(f"OK: {result.guide}")
        except Exception as e:
            traceback.print_exc()
            print(f"ERROR: {type(e).__name__}: {e}")

asyncio.run(main())
