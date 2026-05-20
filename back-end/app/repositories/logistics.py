from __future__ import annotations

from typing import Dict, List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.batch import Batch
from app.models.batch_parcel import BatchParcel
from app.models.vehicle import Vehicle
from app.schemas.logistics import BatchPublic, BatchStatus, BatchUpdate, VehiclePublic


class BatchRepository:
    async def list(self) -> List[BatchPublic]:
        raise NotImplementedError

    async def get(self, batch_id: str) -> Optional[BatchPublic]:
        raise NotImplementedError

    async def create(self, batch: BatchPublic) -> BatchPublic:
        raise NotImplementedError

    async def update(self, batch_id: str, update: BatchUpdate) -> Optional[BatchPublic]:
        raise NotImplementedError


class VehicleRepository:
    async def list(self) -> List[VehiclePublic]:
        raise NotImplementedError

    async def get(self, vehicle_id: int) -> Optional[VehiclePublic]:
        raise NotImplementedError

    async def create(self, vehicle: VehiclePublic) -> VehiclePublic:
        raise NotImplementedError


class InMemoryBatchRepository(BatchRepository):
    def __init__(self, batches: List[BatchPublic]) -> None:
        self._batches: Dict[str, BatchPublic] = {b.id: b for b in batches}

    async def list(self) -> List[BatchPublic]:
        return list(self._batches.values())

    async def get(self, batch_id: str) -> Optional[BatchPublic]:
        return self._batches.get(batch_id)

    async def create(self, batch: BatchPublic) -> BatchPublic:
        self._batches[batch.id] = batch
        return batch

    async def update(self, batch_id: str, update: BatchUpdate) -> Optional[BatchPublic]:
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

    async def list(self) -> List[VehiclePublic]:
        return list(self._vehicles.values())

    async def get(self, vehicle_id: int) -> Optional[VehiclePublic]:
        return self._vehicles.get(vehicle_id)

    async def create(self, vehicle: VehiclePublic) -> VehiclePublic:
        self._vehicles[vehicle.id] = vehicle
        return vehicle


class SqlAlchemyBatchRepository(BatchRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self) -> List[BatchPublic]:
        result = await self._session.execute(select(Batch))
        batches = result.scalars().all()
        return [await self._to_public(batch) for batch in batches]

    async def get(self, batch_id: str) -> Optional[BatchPublic]:
        batch = await self._session.get(Batch, batch_id)
        if not batch:
            return None
        return await self._to_public(batch)

    async def create(self, batch: BatchPublic) -> BatchPublic:
        record = Batch(
            id=batch.id,
            status=batch.status.value,
            vehicle=batch.vehicle,
            driver=batch.driver,
            driver_id=batch.driver_id,
            parcel_count=batch.parcel_count,
        )
        self._session.add(record)
        for parcel_id in batch.parcels:
            self._session.add(BatchParcel(batch_id=batch.id, parcel_id=parcel_id))
        await self._session.commit()
        return batch

    async def update(self, batch_id: str, update: BatchUpdate) -> Optional[BatchPublic]:
        batch = await self._session.get(Batch, batch_id)
        if not batch:
            return None
        data = update.model_dump(by_alias=True, exclude_unset=True)
        parcels = data.pop("parcels", None)
        if "driverId" in data:
            batch.driver_id = data.pop("driverId")
        if "status" in data and data["status"] is not None:
            batch.status = data.pop("status").value
        for key, value in data.items():
            setattr(batch, key, value)
        if parcels is not None:
            await self._session.execute(delete(BatchParcel).where(BatchParcel.batch_id == batch_id))
            for parcel_id in parcels:
                self._session.add(BatchParcel(batch_id=batch_id, parcel_id=parcel_id))
            batch.parcel_count = len(parcels)
        await self._session.commit()
        return await self._to_public(batch)

    async def _to_public(self, batch: Batch) -> BatchPublic:
        result = await self._session.execute(
            select(BatchParcel).where(BatchParcel.batch_id == batch.id)
        )
        parcels = [item.parcel_id for item in result.scalars().all()]
        return BatchPublic(
            id=batch.id,
            parcels=parcels,
            status=BatchStatus(batch.status),
            vehicle=batch.vehicle,
            driver=batch.driver,
            driverId=batch.driver_id,
            parcelCount=batch.parcel_count,
        )


class SqlAlchemyVehicleRepository(VehicleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self) -> List[VehiclePublic]:
        result = await self._session.execute(select(Vehicle))
        vehicles = result.scalars().all()
        return [
            VehiclePublic(
                id=v.id,
                plate=v.plate,
                model=v.model,
                capacity=v.capacity,
                driver=v.driver,
            )
            for v in vehicles
        ]

    async def get(self, vehicle_id: int) -> Optional[VehiclePublic]:
        vehicle = await self._session.get(Vehicle, vehicle_id)
        if not vehicle:
            return None
        return VehiclePublic(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            capacity=vehicle.capacity,
            driver=vehicle.driver,
        )

    async def create(self, vehicle: VehiclePublic) -> VehiclePublic:
        record = Vehicle(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            capacity=vehicle.capacity,
            driver=vehicle.driver,
        )
        self._session.add(record)
        await self._session.commit()
        return vehicle
