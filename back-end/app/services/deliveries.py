from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from typing import Any, Dict

from app.core.errors import NotFoundError
from app.core.pagination import paginate_with_meta
from app.repositories.deliveries import DeliveryRepository
from app.repositories.users import UserRepository
from app.schemas.delivery import DeliveryPOD, DeliveryPublic, DeliveryStatus, DeliveryUpdate
from app.services.notifications import NotificationService


class DeliveryService:
    def __init__(
        self,
        repo: DeliveryRepository,
        user_repo: UserRepository,
        notifications: Optional[NotificationService] = None,
    ) -> None:
        self._repo = repo
        self._user_repo = user_repo
        self._notifications = notifications

    async def list(
        self,
        page: int | None = None,
        page_size: int | None = None,
        user_branch: Optional[str] = None,
        user_role: Optional[str] = None,
    ) -> Dict[str, Any]:
        items = await self._repo.list()
        # Filtrado por branch del usuario (branch scoping - Fase 3)
        if user_branch and user_role != "Admin":
            # Obtener branches de los drivers para filtrar
            filtered = []
            for delivery in items:
                driver = await self._user_repo.get_by_name(delivery.driver)
                if driver and driver.branch == user_branch:
                    filtered.append(delivery)
            items = filtered
        return paginate_with_meta(items, page, page_size)

    async def get(
        self, delivery_id: str, user_branch: Optional[str] = None, user_role: Optional[str] = None
    ) -> DeliveryPublic:
        delivery = await self._repo.get(delivery_id)
        if not delivery:
            raise NotFoundError("Entrega no encontrada")
        # Branch scoping: verificar ownership para roles no-Admin
        if user_branch and user_role != "Admin":
            driver = await self._user_repo.get_by_name(delivery.driver)
            if not driver or driver.branch != user_branch:
                raise NotFoundError("Entrega no encontrada")
        return delivery

    async def update(self, delivery_id: str, payload: DeliveryUpdate) -> DeliveryPublic:
        updated = await self._repo.update(delivery_id, payload)
        if not updated:
            raise NotFoundError("Entrega no encontrada")
        return updated

    async def add_pod(self, delivery_id: str, payload: DeliveryPOD) -> DeliveryPublic:
        delivery = await self._repo.get(delivery_id)
        if not delivery:
            raise NotFoundError("Entrega no encontrada")
        update = DeliveryUpdate(
            podType=payload.pod_type,
            signatureData=payload.signature_data,
            photoUrl=payload.photo_url,
            gps=payload.gps,
            deliveryDate=payload.delivery_date or datetime.now(timezone.utc).date().isoformat(),
            status=DeliveryStatus.COMPLETED,
        )
        result = await self.update(delivery_id, update)
        if self._notifications:
            await self._notifications.create(
                text=f"Entrega {delivery_id} completada con POD",
                action_type="delivery_completed",
                related_id=delivery_id,
            )
        return result
