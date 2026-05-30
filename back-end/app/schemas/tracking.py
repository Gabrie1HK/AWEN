from __future__ import annotations

from typing import Optional

from pydantic import Field

from app.schemas.base import AppBaseModel
from app.schemas.parcel import ParcelStatus, PublicTrackingParcel
from app.schemas.parcel_note import ParcelNotePublic


class TrackingEvent(AppBaseModel):
    step: ParcelStatus
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    operator: Optional[str] = None
    completed: bool = False


class RouteResponse(AppBaseModel):
    route: list[dict]
    distance_km: float


class PublicTrackingResponse(AppBaseModel):
    guide: str
    parcel: Optional[PublicTrackingParcel] = None
    history: Optional[list[TrackingEvent]] = None
    route: Optional[list[dict]] = None
    public_notes: Optional[list[ParcelNotePublic]] = None
