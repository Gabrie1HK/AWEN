from __future__ import annotations

from typing import Dict, List, Optional

from app.schemas.delivery import DeliveryPublic, DeliveryUpdate


class DeliveryRepository:
    def list(self) -> List[DeliveryPublic]:
        raise NotImplementedError

    def get(self, delivery_id: str) -> Optional[DeliveryPublic]:
        raise NotImplementedError

    def create(self, delivery: DeliveryPublic) -> DeliveryPublic:
        raise NotImplementedError

    def update(self, delivery_id: str, update: DeliveryUpdate) -> Optional[DeliveryPublic]:
        raise NotImplementedError


class InMemoryDeliveryRepository(DeliveryRepository):
    def __init__(self, deliveries: List[DeliveryPublic]) -> None:
        self._deliveries: Dict[str, DeliveryPublic] = {d.id: d for d in deliveries}

    def list(self) -> List[DeliveryPublic]:
        return list(self._deliveries.values())

    def get(self, delivery_id: str) -> Optional[DeliveryPublic]:
        return self._deliveries.get(delivery_id)

    def create(self, delivery: DeliveryPublic) -> DeliveryPublic:
        self._deliveries[delivery.id] = delivery
        return delivery

    def update(self, delivery_id: str, update: DeliveryUpdate) -> Optional[DeliveryPublic]:
        existing = self._deliveries.get(delivery_id)
        if not existing:
            return None
        data = existing.model_dump(by_alias=True)
        for key, value in update.model_dump(by_alias=True, exclude_unset=True).items():
            data[key] = value
        updated = DeliveryPublic(**data)
        self._deliveries[delivery_id] = updated
        return updated
