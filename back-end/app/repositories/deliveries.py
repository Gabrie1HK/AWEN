from __future__ import annotations

from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.delivery import Delivery
from app.schemas.delivery import DeliveryPublic, DeliveryStatus, DeliveryUpdate, PodType


class DeliveryRepository:
    async def list(self) -> List[DeliveryPublic]:
        raise NotImplementedError

    async def get(self, delivery_id: str) -> Optional[DeliveryPublic]:
        raise NotImplementedError

    async def create(self, delivery: DeliveryPublic) -> DeliveryPublic:
        raise NotImplementedError

    async def update(self, delivery_id: str, update: DeliveryUpdate) -> Optional[DeliveryPublic]:
        raise NotImplementedError


class InMemoryDeliveryRepository(DeliveryRepository):
    def __init__(self, deliveries: List[DeliveryPublic]) -> None:
        self._deliveries: Dict[str, DeliveryPublic] = {d.id: d for d in deliveries}

    async def list(self) -> List[DeliveryPublic]:
        return list(self._deliveries.values())

    async def get(self, delivery_id: str) -> Optional[DeliveryPublic]:
        return self._deliveries.get(delivery_id)

    async def create(self, delivery: DeliveryPublic) -> DeliveryPublic:
        self._deliveries[delivery.id] = delivery
        return delivery

    async def update(self, delivery_id: str, update: DeliveryUpdate) -> Optional[DeliveryPublic]:
        existing = self._deliveries.get(delivery_id)
        if not existing:
            return None
        data = existing.model_dump(by_alias=True)
        for key, value in update.model_dump(by_alias=True, exclude_unset=True).items():
            data[key] = value
        updated = DeliveryPublic(**data)
        self._deliveries[delivery_id] = updated
        return updated


class SqlAlchemyDeliveryRepository(DeliveryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self) -> List[DeliveryPublic]:
        result = await self._session.execute(select(Delivery))
        items = result.scalars().all()
        return [self._to_public(item) for item in items]

    async def get(self, delivery_id: str) -> Optional[DeliveryPublic]:
        delivery = await self._session.get(Delivery, delivery_id)
        if not delivery:
            return None
        return self._to_public(delivery)

    async def create(self, delivery: DeliveryPublic) -> DeliveryPublic:
        record = Delivery(
            id=delivery.id,
            guide=delivery.guide,
            recipient=delivery.recipient,
            driver=delivery.driver,
            delivery_date=delivery.delivery_date,
            pod_type=delivery.pod_type.value,
            status=delivery.status.value,
            signature_data=delivery.signature_data,
            photo_url=delivery.photo_url,
            gps=delivery.gps,
        )
        self._session.add(record)
        await self._session.commit()
        return delivery

    async def update(self, delivery_id: str, update: DeliveryUpdate) -> Optional[DeliveryPublic]:
        delivery = await self._session.get(Delivery, delivery_id)
        if not delivery:
            return None
        data = update.model_dump(by_alias=True, exclude_unset=True)
        if "deliveryDate" in data:
            delivery.delivery_date = data.pop("deliveryDate")
        if "podType" in data:
            value = data.pop("podType")
            delivery.pod_type = value.value if value is not None else None
        if "signatureData" in data:
            delivery.signature_data = data.pop("signatureData")
        if "photoUrl" in data:
            delivery.photo_url = data.pop("photoUrl")
        for key, value in data.items():
            if key == "status" and value is not None:
                delivery.status = value.value
            else:
                setattr(delivery, key, value)
        await self._session.commit()
        return self._to_public(delivery)

    @staticmethod
    def _to_public(delivery: Delivery) -> DeliveryPublic:
        return DeliveryPublic(
            id=delivery.id,
            guide=delivery.guide,
            recipient=delivery.recipient,
            driver=delivery.driver,
            deliveryDate=delivery.delivery_date,
            podType=PodType(delivery.pod_type),
            status=DeliveryStatus(delivery.status),
            signatureData=delivery.signature_data,
            photoUrl=delivery.photo_url,
            gps=delivery.gps,
        )
