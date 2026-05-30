from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from app.schemas.base import AppBaseModel


class ParcelStatus(str, Enum):
    REGISTERED = "Registered"
    PICKED_UP = "Picked Up"
    IN_TRANSIT = "In Transit"
    AT_DESTINATION_BRANCH = "At Destination Branch"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    RETURNED = "Returned"


class ParcelBase(AppBaseModel):
    sender: str = Field(..., min_length=1, max_length=120)
    sender_id: str = Field(..., min_length=1, max_length=40, alias="senderId")
    sender_phone: str = Field(..., min_length=1, max_length=40, alias="senderPhone")
    recipient: str = Field(..., min_length=1, max_length=120)
    recipient_id: str = Field(..., min_length=1, max_length=40, alias="recipientId")
    recipient_phone: str = Field(..., min_length=1, max_length=40, alias="recipientPhone")
    recipient_address: str = Field(..., min_length=1, max_length=200, alias="recipientAddress")
    origin_address: Optional[str] = Field(default=None, max_length=200, alias="originAddress")
    origin_lat: Optional[float] = Field(default=None, alias="originLat")
    origin_lng: Optional[float] = Field(default=None, alias="originLng")
    destination_address: Optional[str] = Field(default=None, max_length=200, alias="destinationAddress")
    destination_lat: Optional[float] = Field(default=None, alias="destinationLat")
    destination_lng: Optional[float] = Field(default=None, alias="destinationLng")
    origin_branch: str = Field(..., min_length=1, max_length=120, alias="originBranch")
    destination_branch: str = Field(..., min_length=1, max_length=120, alias="destinationBranch")
    weight: float = Field(..., gt=0)
    dimensions: str = Field(default="N/A", max_length=60)
    declared_value: int = Field(..., ge=0, alias="declaredValue")
    description: str = Field(default="Sin descripción", max_length=200)


class ParcelCreate(ParcelBase):
    origin_branch: Optional[str] = Field(default=None, max_length=120, alias="originBranch")
    destination_branch: Optional[str] = Field(default=None, max_length=120, alias="destinationBranch")


class ParcelUpdate(AppBaseModel):
    sender: Optional[str] = None
    sender_id: Optional[str] = Field(default=None, alias="senderId")
    sender_phone: Optional[str] = Field(default=None, alias="senderPhone")
    recipient: Optional[str] = None
    recipient_id: Optional[str] = Field(default=None, alias="recipientId")
    recipient_phone: Optional[str] = Field(default=None, alias="recipientPhone")
    recipient_address: Optional[str] = Field(default=None, alias="recipientAddress")
    origin_address: Optional[str] = Field(default=None, alias="originAddress")
    origin_lat: Optional[float] = Field(default=None, alias="originLat")
    origin_lng: Optional[float] = Field(default=None, alias="originLng")
    destination_address: Optional[str] = Field(default=None, alias="destinationAddress")
    destination_lat: Optional[float] = Field(default=None, alias="destinationLat")
    destination_lng: Optional[float] = Field(default=None, alias="destinationLng")
    origin_branch: Optional[str] = Field(default=None, alias="originBranch")
    destination_branch: Optional[str] = Field(default=None, alias="destinationBranch")
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    declared_value: Optional[int] = Field(default=None, alias="declaredValue")
    description: Optional[str] = None
    status: Optional[ParcelStatus] = None


class ParcelStatusUpdate(AppBaseModel):
    status: ParcelStatus
    photo_url: Optional[str] = Field(default=None, alias="photoUrl")
    gps: Optional[str] = None


class ParcelPublic(ParcelBase):
    id: str
    guide: str
    status: ParcelStatus
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    qr_data: str = Field(..., alias="qrData")
    barcode: str


class PublicTrackingParcel(AppBaseModel):
    guide: str
    status: ParcelStatus
    origin_branch: str = Field(..., alias="originBranch")
    destination_branch: str = Field(..., alias="destinationBranch")
    origin_address: Optional[str] = Field(default=None, alias="originAddress")
    origin_lat: Optional[float] = Field(default=None, alias="originLat")
    origin_lng: Optional[float] = Field(default=None, alias="originLng")
    destination_address: Optional[str] = Field(default=None, alias="destinationAddress")
    destination_lat: Optional[float] = Field(default=None, alias="destinationLat")
    destination_lng: Optional[float] = Field(default=None, alias="destinationLng")
    sender: str
    recipient: str
    weight: float
