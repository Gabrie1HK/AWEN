from __future__ import annotations

from app.core.errors import NotFoundError
from app.core.pagination import paginate
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


class LogisticsService:
    def __init__(self, batches: BatchRepository, vehicles: VehicleRepository) -> None:
        self._batches = batches
        self._vehicles = vehicles

    def list_batches(self, page: int | None = None, page_size: int | None = None) -> list[BatchPublic]:
        return paginate(self._batches.list(), page, page_size)

    def get_batch(self, batch_id: str) -> BatchPublic:
        batch = self._batches.get(batch_id)
        if not batch:
            raise NotFoundError("Lote no encontrado")
        return batch

    def create_batch(self, payload: BatchCreate) -> BatchPublic:
        batch_id = self._next_batch_id()
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
        return self._batches.create(batch)

    def update_batch(self, batch_id: str, payload: BatchUpdate) -> BatchPublic:
        updated = self._batches.update(batch_id, payload)
        if not updated:
            raise NotFoundError("Lote no encontrado")
        return updated

    def assign_batch(self, batch_id: str, payload: BatchAssign) -> BatchPublic:
        update = BatchUpdate(
            vehicle=payload.vehicle,
            driver=payload.driver,
            driver_id=payload.driver_id,
            status=payload.status or BatchStatus.ASSIGNED,
        )
        return self.update_batch(batch_id, update)

    def list_vehicles(self, page: int | None = None, page_size: int | None = None) -> list[VehiclePublic]:
        return paginate(self._vehicles.list(), page, page_size)

    def create_vehicle(self, payload: VehicleCreate) -> VehiclePublic:
        vehicle_id = self._next_vehicle_id()
        vehicle = VehiclePublic(id=vehicle_id, **payload.model_dump())
        return self._vehicles.create(vehicle)

    def _next_batch_id(self) -> str:
        existing = self._batches.list()
        if not existing:
            return "LOT-001"
        last = max(int(b.id.split("-")[-1]) for b in existing)
        return f"LOT-{last + 1:03d}"

    def _next_vehicle_id(self) -> int:
        existing = self._vehicles.list()
        if not existing:
            return 1
        return max(v.id for v in existing) + 1
