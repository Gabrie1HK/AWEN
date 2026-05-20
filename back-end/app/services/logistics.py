from __future__ import annotations

from typing import Optional

from typing import Any, Dict

from app.core.errors import NotFoundError
from app.core.pagination import paginate_with_meta
from app.repositories.logistics import BatchRepository, VehicleRepository
from app.schemas.logistics import (
    BatchAssign,
    BatchCreate,
    BatchPublic,
    BatchStatus,
    BatchUpdate,
    VehicleCreate,
    VehiclePublic,
)
from app.services.notifications import NotificationService


class LogisticsService:
    def __init__(self, batches: BatchRepository, vehicles: VehicleRepository, notifications: Optional[NotificationService] = None) -> None:
        self._batches = batches
        self._vehicles = vehicles
        self._notifications = notifications

    async def list_batches(self, page: int | None = None, page_size: int | None = None) -> Dict[str, Any]:
        return paginate_with_meta(await self._batches.list(), page, page_size)

    async def get_batch(self, batch_id: str) -> BatchPublic:
        batch = await self._batches.get(batch_id)
        if not batch:
            raise NotFoundError("Lote no encontrado")
        return batch

    async def create_batch(self, payload: BatchCreate) -> BatchPublic:
        batch_id = await self._next_batch_id()
        status = payload.status or BatchStatus.PENDING
        parcels = payload.parcels or []
        batch = BatchPublic(
            id=batch_id,
            parcels=parcels,
            status=status,
            vehicle=payload.vehicle,
            driver=payload.driver,
            driverId=payload.driver_id,
            parcelCount=len(parcels),
        )
        result = await self._batches.create(batch)
        if self._notifications:
            await self._notifications.create(
                text=f"Lote {batch_id} creado con {len(parcels)} encomiendas",
                action_type="batch_created",
                related_id=batch_id,
            )
        return result

    async def update_batch(self, batch_id: str, payload: BatchUpdate) -> BatchPublic:
        updated = await self._batches.update(batch_id, payload)
        if not updated:
            raise NotFoundError("Lote no encontrado")
        return updated

    async def assign_batch(self, batch_id: str, payload: BatchAssign) -> BatchPublic:
        update = BatchUpdate(
            vehicle=payload.vehicle,
            driver=payload.driver,
            driver_id=payload.driver_id,
            status=payload.status or BatchStatus.ASSIGNED,
        )
        result = await self.update_batch(batch_id, update)
        if self._notifications:
            await self._notifications.create(
                text=f"Lote {batch_id} asignado a {payload.driver}",
                action_type="batch_assigned",
                related_id=batch_id,
            )
        return result

    async def list_vehicles(self, page: int | None = None, page_size: int | None = None) -> Dict[str, Any]:
        return paginate_with_meta(await self._vehicles.list(), page, page_size)

    async def create_vehicle(self, payload: VehicleCreate) -> VehiclePublic:
        vehicle_id = await self._next_vehicle_id()
        vehicle = VehiclePublic(id=vehicle_id, **payload.model_dump())
        return await self._vehicles.create(vehicle)

    async def _next_batch_id(self) -> str:
        existing = await self._batches.list()
        if not existing:
            return "LOT-001"
        last = max(int(b.id.split("-")[-1]) for b in existing)
        return f"LOT-{last + 1:03d}"

    async def _next_vehicle_id(self) -> int:
        existing = await self._vehicles.list()
        if not existing:
            return 1
        return max(v.id for v in existing) + 1
