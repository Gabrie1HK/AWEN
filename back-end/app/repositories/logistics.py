from __future__ import annotations

from typing import Dict, List, Optional

from app.schemas.logistics import BatchPublic, BatchUpdate, VehiclePublic


class BatchRepository:
    def list(self) -> List[BatchPublic]:
        raise NotImplementedError

    def get(self, batch_id: str) -> Optional[BatchPublic]:
        raise NotImplementedError

    def create(self, batch: BatchPublic) -> BatchPublic:
        raise NotImplementedError

    def update(self, batch_id: str, update: BatchUpdate) -> Optional[BatchPublic]:
        raise NotImplementedError


class VehicleRepository:
    def list(self) -> List[VehiclePublic]:
        raise NotImplementedError

    def get(self, vehicle_id: int) -> Optional[VehiclePublic]:
        raise NotImplementedError

    def create(self, vehicle: VehiclePublic) -> VehiclePublic:
        raise NotImplementedError


class InMemoryBatchRepository(BatchRepository):
    def __init__(self, batches: List[BatchPublic]) -> None:
        self._batches: Dict[str, BatchPublic] = {b.id: b for b in batches}

    def list(self) -> List[BatchPublic]:
        return list(self._batches.values())

    def get(self, batch_id: str) -> Optional[BatchPublic]:
        return self._batches.get(batch_id)

    def create(self, batch: BatchPublic) -> BatchPublic:
        self._batches[batch.id] = batch
        return batch

    def update(self, batch_id: str, update: BatchUpdate) -> Optional[BatchPublic]:
        existing = self._batches.get(batch_id)
        if not existing:
            return None
        data = existing.model_dump(by_alias=True)
        for key, value in update.model_dump(by_alias=True, exclude_unset=True).items():
            data[key] = value
        if "parcels" in data:
            data["parcelCount"] = len(data.get("parcels") or [])
        updated = BatchPublic(**data)
        self._batches[batch_id] = updated
        return updated


class InMemoryVehicleRepository(VehicleRepository):
    def __init__(self, vehicles: List[VehiclePublic]) -> None:
        self._vehicles: Dict[int, VehiclePublic] = {v.id: v for v in vehicles}

    def list(self) -> List[VehiclePublic]:
        return list(self._vehicles.values())

    def get(self, vehicle_id: int) -> Optional[VehiclePublic]:
        return self._vehicles.get(vehicle_id)

    def create(self, vehicle: VehiclePublic) -> VehiclePublic:
        self._vehicles[vehicle.id] = vehicle
        return vehicle
