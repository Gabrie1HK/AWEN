from __future__ import annotations

from typing import Dict, List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.parcel import Parcel
from app.models.tracking_event import TrackingEvent as TrackingEventModel
from app.schemas.parcel import ParcelPublic, ParcelStatus, ParcelUpdate
from app.schemas.tracking import TrackingEvent


class ParcelRepository:
    async def list(self) -> List[ParcelPublic]:
        raise NotImplementedError

    async def get(self, parcel_id: str) -> Optional[ParcelPublic]:
        raise NotImplementedError

    async def get_by_guide(self, guide: str) -> Optional[ParcelPublic]:
        raise NotImplementedError

    async def create(self, parcel: ParcelPublic) -> ParcelPublic:
        raise NotImplementedError

    async def update(self, parcel_id: str, update: ParcelUpdate) -> Optional[ParcelPublic]:
        raise NotImplementedError

    async def update_status(self, parcel_id: str, status: ParcelStatus) -> Optional[ParcelPublic]:
        raise NotImplementedError

    async def delete(self, parcel_id: str) -> bool:
        raise NotImplementedError


class TrackingRepository:
    async def list_by_guide(self, guide: str) -> List[TrackingEvent]:
        raise NotImplementedError

    async def set_history(self, guide: str, history: List[TrackingEvent]) -> None:
        raise NotImplementedError


class InMemoryParcelRepository(ParcelRepository):
    def __init__(self, parcels: List[ParcelPublic]) -> None:
        self._parcels: Dict[str, ParcelPublic] = {p.id: p for p in parcels}
        self._guide_index: Dict[str, str] = {p.guide: p.id for p in parcels}

    async def list(self) -> List[ParcelPublic]:
        return list(self._parcels.values())

    async def get(self, parcel_id: str) -> Optional[ParcelPublic]:
        return self._parcels.get(parcel_id)

    async def get_by_guide(self, guide: str) -> Optional[ParcelPublic]:
        parcel_id = self._guide_index.get(guide)
        if not parcel_id:
            return None
        return self._parcels.get(parcel_id)

    async def create(self, parcel: ParcelPublic) -> ParcelPublic:
        self._parcels[parcel.id] = parcel
        self._guide_index[parcel.guide] = parcel.id
        return parcel

    async def update(self, parcel_id: str, update: ParcelUpdate) -> Optional[ParcelPublic]:
        existing = self._parcels.get(parcel_id)
        if not existing:
            return None
        data = existing.model_dump(by_alias=True)
        for key, value in update.model_dump(by_alias=True, exclude_unset=True).items():
            data[key] = value
        updated = ParcelPublic(**data)
        self._parcels[parcel_id] = updated
        return updated

    async def update_status(self, parcel_id: str, status: ParcelStatus) -> Optional[ParcelPublic]:
        existing = self._parcels.get(parcel_id)
        if not existing:
            return None
        data = existing.model_dump(by_alias=True)
        data["status"] = status
        updated = ParcelPublic(**data)
        self._parcels[parcel_id] = updated
        return updated

    async def delete(self, parcel_id: str) -> bool:
        existing = self._parcels.pop(parcel_id, None)
        if not existing:
            return False
        self._guide_index.pop(existing.guide, None)
        return True


class InMemoryTrackingRepository(TrackingRepository):
    def __init__(self, history: Dict[str, List[TrackingEvent]]) -> None:
        self._history = history

    async def list_by_guide(self, guide: str) -> List[TrackingEvent]:
        return self._history.get(guide, [])

    async def set_history(self, guide: str, history: List[TrackingEvent]) -> None:
        self._history[guide] = history


class SqlAlchemyParcelRepository(ParcelRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self) -> List[ParcelPublic]:
        result = await self._session.execute(select(Parcel))
        items = result.scalars().all()
        return [self._to_public(p) for p in items]

    async def get(self, parcel_id: str) -> Optional[ParcelPublic]:
        parcel = await self._session.get(Parcel, parcel_id)
        if not parcel:
            return None
        return self._to_public(parcel)

    async def get_by_guide(self, guide: str) -> Optional[ParcelPublic]:
        result = await self._session.execute(select(Parcel).where(Parcel.guide == guide))
        parcel = result.scalar_one_or_none()
        if not parcel:
            return None
        return self._to_public(parcel)

    async def create(self, parcel: ParcelPublic) -> ParcelPublic:
        record = Parcel(
            id=parcel.id,
            guide=parcel.guide,
            sender=parcel.sender,
            sender_id=parcel.sender_id,
            sender_phone=parcel.sender_phone,
            recipient=parcel.recipient,
            recipient_id=parcel.recipient_id,
            recipient_phone=parcel.recipient_phone,
            recipient_address=parcel.recipient_address,
            origin_branch=parcel.origin_branch,
            destination_branch=parcel.destination_branch,
            weight=parcel.weight,
            dimensions=parcel.dimensions,
            declared_value=parcel.declared_value,
            description=parcel.description,
            status=parcel.status.value,
            created_at=parcel.created_at,
            updated_at=parcel.updated_at,
            qr_data=parcel.qr_data,
            barcode=parcel.barcode,
        )
        self._session.add(record)
        await self._session.commit()
        return parcel

    async def update(self, parcel_id: str, update: ParcelUpdate) -> Optional[ParcelPublic]:
        parcel = await self._session.get(Parcel, parcel_id)
        if not parcel:
            return None
        data = update.model_dump(by_alias=True, exclude_unset=True)
        if "senderId" in data:
            data["sender_id"] = data.pop("senderId")
        if "senderPhone" in data:
            data["sender_phone"] = data.pop("senderPhone")
        if "recipientId" in data:
            data["recipient_id"] = data.pop("recipientId")
        if "recipientPhone" in data:
            data["recipient_phone"] = data.pop("recipientPhone")
        if "recipientAddress" in data:
            data["recipient_address"] = data.pop("recipientAddress")
        if "originBranch" in data:
            data["origin_branch"] = data.pop("originBranch")
        if "destinationBranch" in data:
            data["destination_branch"] = data.pop("destinationBranch")
        if "declaredValue" in data:
            data["declared_value"] = data.pop("declaredValue")
        if "createdAt" in data:
            data["created_at"] = data.pop("createdAt")
        if "updatedAt" in data:
            data["updated_at"] = data.pop("updatedAt")
        if "qrData" in data:
            data["qr_data"] = data.pop("qrData")
        for key, value in data.items():
            if key == "status" and value is not None:
                setattr(parcel, key, value.value)
            else:
                setattr(parcel, key, value)
        await self._session.commit()
        return self._to_public(parcel)

    async def update_status(self, parcel_id: str, status: ParcelStatus) -> Optional[ParcelPublic]:
        parcel = await self._session.get(Parcel, parcel_id)
        if not parcel:
            return None
        parcel.status = status.value
        await self._session.commit()
        return self._to_public(parcel)

    async def delete(self, parcel_id: str) -> bool:
        parcel = await self._session.get(Parcel, parcel_id)
        if not parcel:
            return False
        await self._session.delete(parcel)
        await self._session.commit()
        return True

    @staticmethod
    def _to_public(parcel: Parcel) -> ParcelPublic:
        return ParcelPublic(
            id=parcel.id,
            guide=parcel.guide,
            sender=parcel.sender,
            senderId=parcel.sender_id,
            senderPhone=parcel.sender_phone,
            recipient=parcel.recipient,
            recipientId=parcel.recipient_id,
            recipientPhone=parcel.recipient_phone,
            recipientAddress=parcel.recipient_address,
            originBranch=parcel.origin_branch,
            destinationBranch=parcel.destination_branch,
            weight=parcel.weight,
            dimensions=parcel.dimensions,
            declaredValue=parcel.declared_value,
            description=parcel.description,
            status=ParcelStatus(parcel.status),
            createdAt=parcel.created_at,
            updatedAt=parcel.updated_at,
            qrData=parcel.qr_data,
            barcode=parcel.barcode,
        )


class SqlAlchemyTrackingRepository(TrackingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_guide(self, guide: str) -> List[TrackingEvent]:
        result = await self._session.execute(select(TrackingEventModel).where(TrackingEventModel.guide == guide))
        items = result.scalars().all()
        return [
            TrackingEvent(
                step=ParcelStatus(item.step),
                date=item.date,
                time=item.time,
                location=item.location,
                operator=item.operator,
                completed=item.completed,
            )
            for item in items
        ]

    async def set_history(self, guide: str, history: List[TrackingEvent]) -> None:
        await self._session.execute(delete(TrackingEventModel).where(TrackingEventModel.guide == guide))
        for item in history:
            record = TrackingEventModel(
                guide=guide,
                step=item.step.value,
                date=item.date,
                time=item.time,
                location=item.location,
                operator=item.operator,
                completed=item.completed,
            )
            self._session.add(record)
        await self._session.commit()
