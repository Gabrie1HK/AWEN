from app.schemas.delivery import DeliveryPublic, DeliveryStatus, PodType


def seed_deliveries() -> list[DeliveryPublic]:
    return [
        DeliveryPublic(
            id="DEL-001",
            guide="AWEN-2026-0002",
            recipient="Carmen Flores",
            driver="Conductor Ana",
            deliveryDate="2026-05-12",
            podType=PodType.SIGNATURE,
            status=DeliveryStatus.COMPLETED,
            signatureData=None,
            photoUrl=None,
            gps="-36.8269, -73.0499",
        ),
        DeliveryPublic(
            id="DEL-002",
            guide="AWEN-2026-0001",
            recipient="Roberto Garcia",
            driver="Conductor Pedro",
            deliveryDate=None,
            podType=PodType.PHOTO,
            status=DeliveryStatus.PENDING,
            signatureData=None,
            photoUrl=None,
            gps="-23.6509, -70.3975",
        ),
        DeliveryPublic(
            id="DEL-003",
            guide="AWEN-2026-0004",
            recipient="Laura Martinez",
            driver="Conductor Ana",
            deliveryDate=None,
            podType=PodType.SIGNATURE,
            status=DeliveryStatus.PENDING,
            signatureData=None,
            photoUrl=None,
            gps="-33.0472, -71.6127",
        ),
    ]
