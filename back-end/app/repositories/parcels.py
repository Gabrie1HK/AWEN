from __future__ import annotations

from typing import Dict, List, Optional

from app.schemas.parcel import ParcelPublic, ParcelStatus, ParcelUpdate
from app.schemas.tracking import TrackingEvent


class ParcelRepository:
    def list(self) -> List[ParcelPublic]:
        raise NotImplementedError

    def get(self, parcel_id: str) -> Optional[ParcelPublic]:
        raise NotImplementedError

    def get_by_guide(self, guide: str) -> Optional[ParcelPublic]:
        raise NotImplementedError

    def create(self, parcel: ParcelPublic) -> ParcelPublic:
        raise NotImplementedError

    def update(self, parcel_id: str, update: ParcelUpdate) -> Optional[ParcelPublic]:
        raise NotImplementedError

    def update_status(self, parcel_id: str, status: ParcelStatus) -> Optional[ParcelPublic]:
        raise NotImplementedError

    def delete(self, parcel_id: str) -> bool:
        raise NotImplementedError


class TrackingRepository:
    def list_by_guide(self, guide: str) -> List[TrackingEvent]:
        raise NotImplementedError

    def set_history(self, guide: str, history: List[TrackingEvent]) -> None:
        raise NotImplementedError


class InMemoryParcelRepository(ParcelRepository):
    def __init__(self, parcels: List[ParcelPublic]) -> None:
        self._parcels: Dict[str, ParcelPublic] = {p.id: p for p in parcels}
        self._guide_index: Dict[str, str] = {p.guide: p.id for p in parcels}

    def list(self) -> List[ParcelPublic]:
        return list(self._parcels.values())

    def get(self, parcel_id: str) -> Optional[ParcelPublic]:
        return self._parcels.get(parcel_id)

    def get_by_guide(self, guide: str) -> Optional[ParcelPublic]:
        parcel_id = self._guide_index.get(guide)
        if not parcel_id:
            return None
        return self._parcels.get(parcel_id)

    def create(self, parcel: ParcelPublic) -> ParcelPublic:
        self._parcels[parcel.id] = parcel
        self._guide_index[parcel.guide] = parcel.id
        return parcel

    def update(self, parcel_id: str, update: ParcelUpdate) -> Optional[ParcelPublic]:
        existing = self._parcels.get(parcel_id)
        if not existing:
            return None
        data = existing.model_dump(by_alias=True)
        for key, value in update.model_dump(by_alias=True, exclude_unset=True).items():
            data[key] = value
        updated = ParcelPublic(**data)
        self._parcels[parcel_id] = updated
        return updated

    def update_status(self, parcel_id: str, status: ParcelStatus) -> Optional[ParcelPublic]:
        existing = self._parcels.get(parcel_id)
        if not existing:
            return None
        data = existing.model_dump(by_alias=True)
        data["status"] = status
        updated = ParcelPublic(**data)
        self._parcels[parcel_id] = updated
        return updated

    def delete(self, parcel_id: str) -> bool:
        existing = self._parcels.pop(parcel_id, None)
        if not existing:
            return False
        self._guide_index.pop(existing.guide, None)
        return True


class InMemoryTrackingRepository(TrackingRepository):
    def __init__(self, history: Dict[str, List[TrackingEvent]]) -> None:
        self._history = history

    def list_by_guide(self, guide: str) -> List[TrackingEvent]:
        return self._history.get(guide, [])

    def set_history(self, guide: str, history: List[TrackingEvent]) -> None:
        self._history[guide] = history
