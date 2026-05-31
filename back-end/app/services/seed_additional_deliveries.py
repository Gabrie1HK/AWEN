from app.schemas.delivery import DeliveryPublic, DeliveryStatus, PodType


def seed_additional_deliveries() -> list[DeliveryPublic]:
    return [
        DeliveryPublic(
            id="DEL-004",
            guide="AWEN-2026-0011",
            recipient="Marta Cliente",
            driver="Conductor Ana",
            deliveryDate="2026-05-23",
            podType=PodType.PHOTO,
            status=DeliveryStatus.COMPLETED,
            signatureData=None,
            photoUrl=None,
            gps="8.5983, -71.1476",
        ),
        DeliveryPublic(
            id="DEL-005",
            guide="AWEN-2026-0022",
            recipient="Isabella Ferrer",
            driver="Conductor Pedro",
            deliveryDate="2026-05-19",
            podType=PodType.SIGNATURE,
            status=DeliveryStatus.COMPLETED,
            signatureData=None,
            photoUrl=None,
            gps="10.1620, -68.0077",
        ),
        DeliveryPublic(
            id="DEL-006",
            guide="AWEN-2026-0033",
            recipient="Daniela Silva",
            driver="Conductor Ana",
            deliveryDate="2026-05-24",
            podType=PodType.PHOTO,
            status=DeliveryStatus.COMPLETED,
            signatureData=None,
            photoUrl=None,
            gps="10.1620, -68.0077",
        ),
        DeliveryPublic(
            id="DEL-007",
            guide="AWEN-2026-0037",
            recipient="Marta Cliente",
            driver="Conductor Pedro",
            deliveryDate="2026-05-14",
            podType=PodType.SIGNATURE,
            status=DeliveryStatus.COMPLETED,
            signatureData=None,
            photoUrl=None,
            gps="8.5983, -71.1476",
        ),
    ]
