from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from typing import Any, Dict

from app.core.errors import NotFoundError, ValidationError
from app.core.pagination import paginate_with_meta
from app.repositories.parcels import ParcelRepository, TrackingRepository
from app.schemas.parcel import (
    ParcelCreate,
    ParcelPublic,
    ParcelStatus,
    ParcelStatusUpdate,
    ParcelUpdate,
)
from app.schemas.tracking import TrackingEvent
from app.services.notifications import NotificationService


class ParcelService:
    def __init__(self, parcel_repo: ParcelRepository, tracking_repo: TrackingRepository, notifications: Optional[NotificationService] = None) -> None:
        self._parcels = parcel_repo
        self._tracking = tracking_repo
        self._notifications = notifications

    async def list(
        self,
        search: Optional[str] = None,
        status: Optional[ParcelStatus] = None,
        origin_branch: Optional[str] = None,
        destination_branch: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        items = await self._parcels.list()
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
        return paginate_with_meta(items, page, page_size)

    async def list_by_user(self, user_name: str) -> List[ParcelPublic]:
        lowered = user_name.lower()
        items = await self._parcels.list()
        return [
            p for p in items
            if lowered in p.sender.lower() or lowered in p.recipient.lower()
        ]

    async def get(self, parcel_id: str) -> ParcelPublic:
        parcel = await self._parcels.get(parcel_id)
        if not parcel:
            raise NotFoundError("Encomienda no encontrada")
        return parcel

    async def get_by_guide(self, guide: str) -> ParcelPublic:
        parcel = await self._parcels.get_by_guide(guide)
        if not parcel:
            raise NotFoundError("Encomienda no encontrada")
        return parcel

    async def create(self, payload: ParcelCreate) -> ParcelPublic:
        now = datetime.now(timezone.utc).date().isoformat()
        next_id = await self._next_parcel_id()
        guide = await self._next_guide_number()
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
        await self._parcels.create(parcel)
        await self._tracking.set_history(guide, self._default_tracking(guide))
        if self._notifications:
            await self._notifications.create(
                text=f"Nueva encomienda {guide} registrada - {payload.sender} a {payload.recipient}",
                action_type="parcel_created",
                related_id=parcel.id,
            )
        return parcel

    async def update(self, parcel_id: str, update: ParcelUpdate) -> ParcelPublic:
        existing = await self._parcels.get(parcel_id)
        if not existing:
            raise NotFoundError("Encomienda no encontrada")
        updated = await self._parcels.update(parcel_id, update)
        if not updated:
            raise NotFoundError("Encomienda no encontrada")
        data = updated.model_dump(by_alias=True)
        data["updatedAt"] = datetime.now(timezone.utc).date().isoformat()
        await self._parcels.update(parcel_id, ParcelUpdate(**data))
        refreshed = await self._parcels.get(parcel_id)
        if not refreshed:
            raise NotFoundError("Encomienda no encontrada")
        return refreshed

    async def update_status(self, parcel_id: str, status_update: ParcelStatusUpdate) -> ParcelPublic:
        existing = await self._parcels.get(parcel_id)
        if not existing:
            raise NotFoundError("Encomienda no encontrada")
        self._validate_status_transition(existing.status, status_update.status)
        updated = await self._parcels.update_status(parcel_id, status_update.status)
        if not updated:
            raise NotFoundError("Encomienda no encontrada")
        data = updated.model_dump(by_alias=True)
        data["updatedAt"] = datetime.now(timezone.utc).date().isoformat()
        await self._parcels.update(parcel_id, ParcelUpdate(**data))
        refreshed = await self._parcels.get(parcel_id)
        if not refreshed:
            raise NotFoundError("Encomienda no encontrada")
        history = await self._tracking.list_by_guide(existing.guide)
        history = self._mark_tracking(history, status_update.status)
        await self._tracking.set_history(existing.guide, history)
        if self._notifications:
            await self._notifications.create(
                text=f"Encomienda {existing.guide} actualizada a {status_update.status.value}",
                action_type="parcel_status",
                related_id=parcel_id,
            )
        return refreshed

    async def cancel(self, parcel_id: str) -> ParcelPublic:
        update = ParcelUpdate(status=ParcelStatus.RETURNED)
        updated = await self.update(parcel_id, update)
        history = await self._tracking.list_by_guide(updated.guide)
        history = self._mark_tracking(history, ParcelStatus.RETURNED)
        await self._tracking.set_history(updated.guide, history)
        if self._notifications:
            await self._notifications.create(
                text=f"Encomienda {updated.guide} cancelada y devuelta",
                action_type="parcel_cancelled",
                related_id=parcel_id,
            )
        return updated

    async def tracking(self, guide: str) -> List[TrackingEvent]:
        return await self._tracking.list_by_guide(guide)

    async def _next_parcel_id(self) -> str:
        existing = await self._parcels.list()
        if not existing:
            return "ENV-001"
        last = max(int(p.id.split("-")[-1]) for p in existing)
        return f"ENV-{last + 1:03d}"

    async def _next_guide_number(self) -> str:
        existing = await self._parcels.list()
        if not existing:
            return "AWEN-2026-0001"
        last = max(int(p.guide.split("-")[-1]) for p in existing)
        return f"AWEN-2026-{last + 1:04d}"

    def _default_tracking(self, guide: str) -> List[TrackingEvent]:
        return [
            TrackingEvent(step=ParcelStatus.REGISTERED, date=datetime.now(timezone.utc).date().isoformat(), completed=True),
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

        current_date = datetime.now(timezone.utc).date().isoformat()
        current_time = datetime.now(timezone.utc).time().strftime("%H:%M")

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
                data = step.model_dump()
                data.update(completed=True, date=step.date or current_date, time=step.time or current_time)
                updated.append(TrackingEvent(**data))
            else:
                updated.append(step)
        return updated

    def _validate_status_transition(self, current: ParcelStatus, new: ParcelStatus) -> None:
        if current == new:
            return

        ordered = [
            ParcelStatus.REGISTERED,
            ParcelStatus.PICKED_UP,
            ParcelStatus.IN_TRANSIT,
            ParcelStatus.AT_DESTINATION_BRANCH,
            ParcelStatus.OUT_FOR_DELIVERY,
            ParcelStatus.DELIVERED,
        ]

        terminal = {ParcelStatus.DELIVERED, ParcelStatus.RETURNED}

        if current in terminal:
            raise ValidationError(
                f"No se puede cambiar el estado de {current.value}: es un estado terminal",
                detail={"current": current.value, "new": new.value},
            )

        if new == ParcelStatus.RETURNED:
            return

        if current not in ordered or new not in ordered:
            raise ValidationError(
                f"Transicion invalida de {current.value} a {new.value}",
                detail={"current": current.value, "new": new.value},
            )

        current_idx = ordered.index(current)
        new_idx = ordered.index(new)

        if new_idx <= current_idx:
            raise ValidationError(
                f"No se puede retroceder de {current.value} a {new.value}",
                detail={"current": current.value, "new": new.value},
            )

        if new_idx > current_idx + 1:
            raise ValidationError(
                f"No se puede saltar de {current.value} a {new.value}. Debe pasar por {ordered[current_idx + 1].value}",
                detail={
                    "current": current.value,
                    "new": new.value,
                    "next_valid": ordered[current_idx + 1].value,
                },
            )
