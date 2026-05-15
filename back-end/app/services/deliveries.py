from __future__ import annotations

from datetime import datetime

from app.core.errors import NotFoundError
from app.core.pagination import paginate
from app.repositories.deliveries import DeliveryRepository
from app.schemas.delivery import DeliveryPOD, DeliveryPublic, DeliveryStatus, DeliveryUpdate


class DeliveryService:
    def __init__(self, repo: DeliveryRepository) -> None:
        self._repo = repo

    def list(self, page: int | None = None, page_size: int | None = None) -> list[DeliveryPublic]:
        return paginate(self._repo.list(), page, page_size)

    def get(self, delivery_id: str) -> DeliveryPublic:
        delivery = self._repo.get(delivery_id)
        if not delivery:
            raise NotFoundError("Entrega no encontrada")
        return delivery

    def update(self, delivery_id: str, payload: DeliveryUpdate) -> DeliveryPublic:
        updated = self._repo.update(delivery_id, payload)
        if not updated:
            raise NotFoundError("Entrega no encontrada")
        return updated

    def add_pod(self, delivery_id: str, payload: DeliveryPOD) -> DeliveryPublic:
        delivery = self._repo.get(delivery_id)
        if not delivery:
            raise NotFoundError("Entrega no encontrada")
        update = DeliveryUpdate(
            podType=payload.pod_type,
            signatureData=payload.signature_data,
            photoUrl=payload.photo_url,
            gps=payload.gps,
            deliveryDate=payload.delivery_date or datetime.utcnow().date().isoformat(),
            status=DeliveryStatus.COMPLETED,
        )
        return self.update(delivery_id, update)
