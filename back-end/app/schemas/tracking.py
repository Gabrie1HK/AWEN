from __future__ import annotations

from typing import Optional

from pydantic import Field

from app.schemas.base import AppBaseModel
from app.schemas.parcel import ParcelStatus, PublicTrackingParcel


class TrackingEvent(AppBaseModel):
    step: ParcelStatus
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None
    operator: Optional[str] = None
    completed: bool = False


class PublicTrackingResponse(AppBaseModel):
    guide: str
    parcel: Optional[PublicTrackingParcel] = None
    history: Optional[list[TrackingEvent]] = None
