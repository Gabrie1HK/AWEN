from __future__ import annotations

from typing import Optional

from typing import Any, Dict

from app.core.errors import NotFoundError
from app.core.pagination import paginate_with_meta
from app.repositories.logistics import BatchRepository, VehicleRepository
from app.repositories.users import UserRepository
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
    def __init__(
        self,
        batches: BatchRepository,
        vehicles: VehicleRepository,
        user_repo: UserRepository,
        notifications: Optional[NotificationService] = None,
    ) -> None:
        self._batches = batches
        self._vehicles = vehicles
        self._user_repo = user_repo
        self._notifications = notifications

    async def list_batches(
        self,
        page: int | None = None,
        page_size: int | None = None,
        user_branch: Optional[str] = None,
        user_role: Optional[str] = None,
    ) -> Dict[str, Any]:
        items = await self._batches.list()
        # Filtrado por branch del usuario (branch scoping - Fase 3)
        if user_branch and user_role != "Admin":
            filtered = []
            for batch in items:
                driver = await self._user_repo.get_by_name(batch.driver) if batch.driver else None
                if driver and driver.branch == user_branch:
                    filtered.append(batch)
            items = filtered
        return paginate_with_meta(items, page, page_size)

    async def get_batch(self, batch_id: str, user_branch: Optional[str] = None, user_role: Optional[str] = None) -> BatchPublic:
        batch = await self._batches.get(batch_id)
        if not batch:
            raise NotFoundError("Lote no encontrado")
        # Branch scoping: verificar ownership para roles no-Admin
        if user_branch and user_role != "Admin":
            driver = await self._user_repo.get_by_name(batch.driver) if batch.driver else None
            if not driver or driver.branch != user_branch:
                raise NotFoundError("Lote no encontrado")
        return batch

    async def list_vehicles(
        self,
        page: int | None = None,
        page_size: int | None = None,
        user_branch: Optional[str] = None,
        user_role: Optional[str] = None,
    ) -> Dict[str, Any]:
        items = await self._vehicles.list()
        # Filtrado por branch del usuario (branch scoping - Fase 3)
        if user_branch and user_role != "Admin":
            filtered = []
            for vehicle in items:
                driver = await self._user_repo.get_by_name(vehicle.driver) if vehicle.driver else None
                if driver and driver.branch == user_branch:
                    filtered.append(vehicle)
            items = filtered
        return paginate_with_meta(items, page, page_size)

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
