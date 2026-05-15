from app.schemas.logistics import BatchPublic, BatchStatus, VehiclePublic


def seed_batches() -> list[BatchPublic]:
    return [
        BatchPublic(
            id="LOT-001",
            parcels=["ENV-001", "ENV-006"],
            status=BatchStatus.ASSIGNED,
            vehicle="ABC-123",
            driver="Conductor Pedro",
            driverId=4,
            parcelCount=2,
        ),
        BatchPublic(
            id="LOT-002",
            parcels=["ENV-003", "ENV-007"],
            status=BatchStatus.PENDING,
            vehicle=None,
            driver=None,
            driverId=None,
            parcelCount=2,
        ),
        BatchPublic(
            id="LOT-003",
            parcels=["ENV-004"],
            status=BatchStatus.ASSIGNED,
            vehicle="XYZ-789",
            driver="Conductor Ana",
            driverId=5,
            parcelCount=1,
        ),
        BatchPublic(
            id="LOT-004",
            parcels=[],
            status=BatchStatus.COMPLETED,
            vehicle="DEF-456",
            driver="Conductor Pedro",
            driverId=4,
            parcelCount=3,
        ),
    ]


def seed_vehicles() -> list[VehiclePublic]:
    return [
        VehiclePublic(id=1, plate="ABC-123", model="Foton Aumark", capacity="1500 kg", driver="Conductor Pedro"),
        VehiclePublic(id=2, plate="XYZ-789", model="JMC Carrying", capacity="1200 kg", driver="Conductor Ana"),
        VehiclePublic(id=3, plate="DEF-456", model="Chevrolet NPR", capacity="3000 kg", driver="Conductor Luis"),
    ]
