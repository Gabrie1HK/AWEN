from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from app.core.errors import NotFoundError
from app.core.pagination import paginate
from app.repositories.parcels import ParcelRepository, TrackingRepository
from app.schemas.parcel import (
    ParcelCreate,
    ParcelPublic,
    ParcelStatus,
    ParcelStatusUpdate,
    ParcelUpdate,
)
from app.schemas.tracking import TrackingEvent


class ParcelService:
    def __init__(self, parcel_repo: ParcelRepository, tracking_repo: TrackingRepository) -> None:
        self._parcels = parcel_repo
        self._tracking = tracking_repo

    def list(
        self,
        search: Optional[str] = None,
        status: Optional[ParcelStatus] = None,
        origin_branch: Optional[str] = None,
        destination_branch: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[ParcelPublic]:
        items = self._parcels.list()
        if search:
            lowered = search.lower()
            items = [
                p for p in items
                if lowered in p.guide.lower()
                or lowered in p.sender.lower()
                or lowered in p.recipient.lower()
            ]
        if status:
            items = [p for p in items if p.status == status]
        if origin_branch:
            items = [p for p in items if p.origin_branch == origin_branch]
        if destination_branch:
            items = [p for p in items if p.destination_branch == destination_branch]
        return paginate(items, page, page_size)

    def get(self, parcel_id: str) -> ParcelPublic:
        parcel = self._parcels.get(parcel_id)
        if not parcel:
            raise NotFoundError("Encomienda no encontrada")
        return parcel

    def get_by_guide(self, guide: str) -> ParcelPublic:
        parcel = self._parcels.get_by_guide(guide)
        if not parcel:
            raise NotFoundError("Encomienda no encontrada")
        return parcel

    def create(self, payload: ParcelCreate) -> ParcelPublic:
        now = datetime.utcnow().date().isoformat()
        next_id = self._next_parcel_id()
        guide = self._next_guide_number()
        parcel = ParcelPublic(
            id=next_id,
            guide=guide,
            status=ParcelStatus.REGISTERED,
            createdAt=now,
            updatedAt=now,
            qrData=guide,
            barcode=f"|||{guide}|||",
            **payload.model_dump(by_alias=True),
        )
        self._parcels.create(parcel)
        self._tracking.set_history(guide, self._default_tracking(guide))
        return parcel

    def update(self, parcel_id: str, update: ParcelUpdate) -> ParcelPublic:
        existing = self._parcels.get(parcel_id)
        if not existing:
            raise NotFoundError("Encomienda no encontrada")
        updated = self._parcels.update(parcel_id, update)
        if not updated:
            raise NotFoundError("Encomienda no encontrada")
        data = updated.model_dump(by_alias=True)
        data["updatedAt"] = datetime.utcnow().date().isoformat()
        refreshed = ParcelPublic(**data)
        self._parcels.create(refreshed)
        return refreshed

    def update_status(self, parcel_id: str, status_update: ParcelStatusUpdate) -> ParcelPublic:
        existing = self._parcels.get(parcel_id)
        if not existing:
            raise NotFoundError("Encomienda no encontrada")
        updated = self._parcels.update_status(parcel_id, status_update.status)
        if not updated:
            raise NotFoundError("Encomienda no encontrada")
        data = updated.model_dump(by_alias=True)
        data["updatedAt"] = datetime.utcnow().date().isoformat()
        refreshed = ParcelPublic(**data)
        self._parcels.create(refreshed)
        history = self._tracking.list_by_guide(existing.guide)
        history = self._mark_tracking(history, status_update.status)
        self._tracking.set_history(existing.guide, history)
        return refreshed

    def cancel(self, parcel_id: str) -> ParcelPublic:
        update = ParcelUpdate(status=ParcelStatus.RETURNED)
        updated = self.update(parcel_id, update)
        history = self._tracking.list_by_guide(updated.guide)
        history = self._mark_tracking(history, ParcelStatus.RETURNED)
        self._tracking.set_history(updated.guide, history)
        return updated

    def tracking(self, guide: str) -> List[TrackingEvent]:
        return self._tracking.list_by_guide(guide)

    def _next_parcel_id(self) -> str:
        existing = self._parcels.list()
        if not existing:
            return "ENV-001"
        last = max(int(p.id.split("-")[-1]) for p in existing)
        return f"ENV-{last + 1:03d}"

    def _next_guide_number(self) -> str:
        existing = self._parcels.list()
        if not existing:
            return "AWEN-2026-0001"
        last = max(int(p.guide.split("-")[-1]) for p in existing)
        return f"AWEN-2026-{last + 1:04d}"

    def _default_tracking(self, guide: str) -> List[TrackingEvent]:
        return [
            TrackingEvent(step=ParcelStatus.REGISTERED, date=datetime.utcnow().date().isoformat(), completed=True),
            TrackingEvent(step=ParcelStatus.PICKED_UP, completed=False),
            TrackingEvent(step=ParcelStatus.IN_TRANSIT, completed=False),
            TrackingEvent(step=ParcelStatus.AT_DESTINATION_BRANCH, completed=False),
            TrackingEvent(step=ParcelStatus.OUT_FOR_DELIVERY, completed=False),
            TrackingEvent(step=ParcelStatus.DELIVERED, completed=False),
        ]

    def _mark_tracking(self, history: List[TrackingEvent], status: ParcelStatus) -> List[TrackingEvent]:
        if not history:
            return history

        ordered = [
            ParcelStatus.REGISTERED,
            ParcelStatus.PICKED_UP,
            ParcelStatus.IN_TRANSIT,
            ParcelStatus.AT_DESTINATION_BRANCH,
            ParcelStatus.OUT_FOR_DELIVERY,
            ParcelStatus.DELIVERED,
        ]
        if status not in ordered and status != ParcelStatus.RETURNED:
            return history

        current_date = datetime.utcnow().date().isoformat()
        current_time = datetime.utcnow().time().strftime("%H:%M")

        if status == ParcelStatus.RETURNED:
            updated = []
            has_returned = False
            for step in history:
                if step.step == ParcelStatus.RETURNED:
                    has_returned = True
                    updated.append(
                        TrackingEvent(
                            **step.model_dump(),
                            completed=True,
                            date=step.date or current_date,
                            time=step.time or current_time,
                        )
                    )
                else:
                    updated.append(step)
            if not has_returned:
                updated.append(
                    TrackingEvent(
                        step=ParcelStatus.RETURNED,
                        completed=True,
                        date=current_date,
                        time=current_time,
                    )
                )
            return updated

        target_index = ordered.index(status)
        updated = []
        for step in history:
            if step.step in ordered and ordered.index(step.step) <= target_index:
                updated.append(
                    TrackingEvent(
                        **step.model_dump(),
                        completed=True,
                        date=step.date or current_date,
                        time=step.time or current_time,
                    )
                )
            else:
                updated.append(step)
        return updated
