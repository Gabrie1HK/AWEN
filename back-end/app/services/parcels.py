from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from typing import Any, Dict

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError, ValidationError
from app.core.pagination import paginate_with_meta
from app.models.parcel_note import ParcelNote
from app.repositories.deliveries import DeliveryRepository
from app.repositories.parcels import ParcelRepository, TrackingRepository
from app.schemas.delivery import DeliveryPublic, DeliveryStatus, DeliveryUpdate, PodType
from app.schemas.parcel import (
    ParcelCreate,
    ParcelPublic,
    ParcelStatus,
    ParcelStatusUpdate,
    ParcelUpdate,
)
from app.schemas.parcel_note import ParcelNoteCreate, ParcelNotePublic
from app.schemas.tracking import TrackingEvent
from app.core.config import get_settings
from app.services.notifications import NotificationService


class ParcelService:
    def __init__(self, parcel_repo: ParcelRepository, tracking_repo: TrackingRepository, notifications: Optional[NotificationService] = None, delivery_repo: Optional[DeliveryRepository] = None) -> None:
        self._parcels = parcel_repo
        self._tracking = tracking_repo
        self._notifications = notifications
        self._delivery_repo = delivery_repo
        self._settings = get_settings()

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

    async def list_by_user(self, user_name: str, user_last_name: str | None = None) -> List[ParcelPublic]:
        full_name = f"{user_name} {user_last_name}".lower() if user_last_name else user_name.lower()
        items = await self._parcels.list()
        return [
            p for p in items
            if full_name in p.sender.lower() or full_name in p.recipient.lower()
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
        payload = await self._apply_location_defaults(payload)
        if not payload.origin_branch:
            fallback = (payload.origin_address or "Sucursal")[:120]
            payload = ParcelCreate(**{**payload.model_dump(by_alias=True), "originBranch": fallback})
        if not payload.destination_branch:
            fallback = (payload.destination_address or "Sucursal")[:120]
            payload = ParcelCreate(**{**payload.model_dump(by_alias=True), "destinationBranch": fallback})
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
        await self._tracking.set_history(
            guide,
            self._default_tracking(
                guide,
                origin_address=parcel.origin_address,
                origin_lat=parcel.origin_lat,
                origin_lng=parcel.origin_lng,
            ),
        )
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
        update = await self._apply_location_defaults(update)
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

    async def update_status(self, parcel_id: str, status_update: ParcelStatusUpdate, driver_name: Optional[str] = None) -> ParcelPublic:
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

        if status_update.status == ParcelStatus.DELIVERED and self._delivery_repo:
            await self._ensure_delivery_record(existing, status_update, driver_name)

        if self._notifications:
            await self._notifications.create(
                text=f"Encomienda {existing.guide} actualizada a {status_update.status.value}",
                action_type="parcel_status",
                related_id=parcel_id,
            )
        return refreshed

    async def _ensure_delivery_record(self, parcel: ParcelPublic, status_update: ParcelStatusUpdate, driver_name: Optional[str] = None) -> None:
        deliveries = await self._delivery_repo.list()
        existing_delivery = next((d for d in deliveries if d.guide == parcel.guide), None)
        if existing_delivery:
            update = DeliveryUpdate(
                photoUrl=status_update.photo_url or existing_delivery.photo_url,
                gps=status_update.gps or existing_delivery.gps,
                deliveryDate=datetime.now(timezone.utc).date().isoformat(),
                status=DeliveryStatus.COMPLETED if (status_update.photo_url or existing_delivery.photo_url) else DeliveryStatus.PENDING,
            )
            await self._delivery_repo.update(existing_delivery.id, update)
        else:
            last_id = max((int(d.id.split("-")[-1]) for d in deliveries), default=0)
            new_id = f"DEL-{last_id + 1:03d}"
            driver = driver_name or "Conductor"
            delivery = DeliveryPublic(
                id=new_id,
                guide=parcel.guide,
                recipient=parcel.recipient,
                driver=driver,
                deliveryDate=datetime.now(timezone.utc).date().isoformat(),
                podType=PodType.PHOTO,
                status=DeliveryStatus.COMPLETED if status_update.photo_url else DeliveryStatus.PENDING,
                photoUrl=status_update.photo_url,
                gps=status_update.gps,
            )
            await self._delivery_repo.create(delivery)

    async def delete_parcel(self, parcel_id: str) -> None:
        existing = await self._parcels.get(parcel_id)
        if not existing:
            raise NotFoundError("Encomienda no encontrada")
        await self._tracking.set_history(existing.guide, [])
        deleted = await self._parcels.delete(parcel_id)
        if not deleted:
            raise NotFoundError("Encomienda no encontrada")

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

    async def tracking(
        self,
        guide: str,
        origin: Optional[tuple[float, float]] = None,
        destination: Optional[tuple[float, float]] = None,
    ) -> tuple[List[TrackingEvent], Optional[List[dict]]]:
        history = await self._tracking.list_by_guide(guide)
        enriched = await self._enrich_tracking_coords(history)
        route = await self._build_route(enriched)
        if not route and origin and destination:
            result = await self._build_route_from_points(origin, destination)
            route = result["route"] if result else None
        return enriched, route

    async def add_note(self, guide: str, text: str, created_by: str, is_public: bool, db: AsyncSession) -> ParcelNotePublic:
        parcel = await self._parcels.get_by_guide(guide)
        if not parcel:
            raise NotFoundError("Encomienda no encontrada")
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        record = ParcelNote(guide=guide, text=text, created_by=created_by, created_at=now, is_public=is_public)
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return ParcelNotePublic(id=record.id, guide=record.guide, text=record.text, created_by=record.created_by, created_at=record.created_at, is_public=record.is_public)

    async def get_notes(self, guide: str, db: AsyncSession, is_public_only: bool = False) -> list[ParcelNotePublic]:
        stmt = select(ParcelNote).where(ParcelNote.guide == guide)
        if is_public_only:
            stmt = stmt.where(ParcelNote.is_public == True)
        stmt = stmt.order_by(ParcelNote.id)
        result = await db.execute(stmt)
        records = result.scalars().all()
        return [
            ParcelNotePublic(id=r.id, guide=r.guide, text=r.text, created_by=r.created_by, created_at=r.created_at, is_public=r.is_public)
            for r in records
        ]

    async def _enrich_tracking_coords(self, history: List[TrackingEvent]) -> List[TrackingEvent]:
        if not history:
            return history

        missing = [event for event in history if event.completed and event.location and not (event.lat and event.lng)]
        if not missing:
            return history

        results: Dict[str, Dict[str, float]] = {}
        for event in missing:
            if event.location in results:
                continue
            coords = await self._geocode_location(event.location)
            if coords:
                results[event.location] = coords

        if not results:
            return history

        updated: List[TrackingEvent] = []
        for event in history:
            coords = results.get(event.location) if event.location else None
            if coords and not (event.lat and event.lng):
                data = event.model_dump()
                data.update(lat=coords["lat"], lng=coords["lng"])
                updated.append(TrackingEvent(**data))
            else:
                updated.append(event)
        return updated

    async def _geocode_location(self, location: str) -> Optional[Dict[str, float]]:
        params = {
            "format": "json",
            "limit": 1,
            "q": location,
        }
        headers = {
            "User-Agent": self._settings.nominatim_user_agent,
        }
        try:
            async with httpx.AsyncClient(timeout=self._settings.nominatim_timeout_seconds) as client:
                response = await client.get(self._settings.nominatim_url, params=params, headers=headers)
                if response.status_code != 200:
                    return None
                payload = response.json()
        except httpx.RequestError:
            return None

        if not payload:
            return None
        try:
            return {"lat": float(payload[0]["lat"]), "lng": float(payload[0]["lon"])}
        except (KeyError, ValueError, TypeError, IndexError):
            return None

    async def _reverse_geocode(self, lat: float, lng: float) -> Optional[str]:
        params = {
            "format": "json",
            "lat": lat,
            "lon": lng,
        }
        headers = {
            "User-Agent": self._settings.nominatim_user_agent,
        }
        try:
            async with httpx.AsyncClient(timeout=self._settings.nominatim_timeout_seconds) as client:
                response = await client.get(self._settings.nominatim_reverse_url, params=params, headers=headers)
                if response.status_code != 200:
                    return None
                payload = response.json()
        except httpx.RequestError:
            return None
        address = payload.get("display_name")
        return address if isinstance(address, str) else None

    async def _apply_location_defaults(self, payload: ParcelCreate | ParcelUpdate) -> ParcelCreate | ParcelUpdate:
        data = payload.model_dump(by_alias=True, exclude_unset=True)
        origin_lat = data.get("originLat")
        origin_lng = data.get("originLng")
        destination_lat = data.get("destinationLat")
        destination_lng = data.get("destinationLng")
        origin_address = data.get("originAddress")
        destination_address = data.get("destinationAddress")

        if origin_lat is not None and origin_lng is not None and not origin_address:
            origin_address = await self._reverse_geocode(float(origin_lat), float(origin_lng))
        if destination_lat is not None and destination_lng is not None and not destination_address:
            destination_address = await self._reverse_geocode(float(destination_lat), float(destination_lng))

        if origin_address is not None:
            data["originAddress"] = origin_address
        if destination_address is not None:
            data["destinationAddress"] = destination_address

        if isinstance(payload, ParcelCreate):
            return ParcelCreate(**data)
        return ParcelUpdate(**data)

    async def _build_route(self, history: List[TrackingEvent]) -> Optional[List[dict]]:
        steps = [event for event in history if event.completed and event.lat and event.lng]
        if len(steps) < 2:
            return None
        origin = steps[0]
        destination = steps[-1]
        url = f"{self._settings.osrm_url}/{origin.lng},{origin.lat};{destination.lng},{destination.lat}"
        params = {"overview": "full", "geometries": "geojson"}
        try:
            async with httpx.AsyncClient(timeout=self._settings.osrm_timeout_seconds) as client:
                response = await client.get(url, params=params)
                if response.status_code != 200:
                    return None
                payload = response.json()
        except httpx.RequestError:
            return None
        coords = payload.get("routes", [{}])[0].get("geometry", {}).get("coordinates")
        if not coords:
            return None
        return [{"lat": float(lat), "lng": float(lng)} for lng, lat in coords]

    async def _build_route_from_points(
        self,
        origin: tuple[float, float],
        destination: tuple[float, float],
    ) -> Optional[dict]:
        origin_lat, origin_lng = origin
        destination_lat, destination_lng = destination
        url = f"{self._settings.osrm_url}/{origin_lng},{origin_lat};{destination_lng},{destination_lat}"
        params = {"overview": "full", "geometries": "geojson"}
        try:
            async with httpx.AsyncClient(timeout=self._settings.osrm_timeout_seconds) as client:
                response = await client.get(url, params=params)
                if response.status_code != 200:
                    return None
                payload = response.json()
        except httpx.RequestError:
            return None
        routes = payload.get("routes")
        if not routes:
            return None
        coords = routes[0].get("geometry", {}).get("coordinates")
        if not coords:
            return None
        route = [{"lat": float(lat), "lng": float(lng)} for lng, lat in coords]
        distance_m = routes[0].get("distance", 0)
        distance_km = round(distance_m / 1000, 2)
        return {"route": route, "distance_km": distance_km}

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

    def _default_tracking(
        self,
        guide: str,
        origin_address: Optional[str] = None,
        origin_lat: Optional[float] = None,
        origin_lng: Optional[float] = None,
    ) -> List[TrackingEvent]:
        return [
            TrackingEvent(
                step=ParcelStatus.REGISTERED,
                date=datetime.now(timezone.utc).date().isoformat(),
                location=origin_address,
                lat=origin_lat,
                lng=origin_lng,
                completed=True,
            ),
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
