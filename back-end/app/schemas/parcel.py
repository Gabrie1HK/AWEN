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
    sender: str
    sender_id: str = Field(..., alias="senderId")
    sender_phone: str = Field(..., alias="senderPhone")
    recipient: str
    recipient_id: str = Field(..., alias="recipientId")
    recipient_phone: str = Field(..., alias="recipientPhone")
    recipient_address: str = Field(..., alias="recipientAddress")
    origin_branch: str = Field(..., alias="originBranch")
    destination_branch: str = Field(..., alias="destinationBranch")
    weight: float
    dimensions: str
    declared_value: int = Field(..., alias="declaredValue")
    description: str


class ParcelCreate(ParcelBase):
    pass


class ParcelUpdate(AppBaseModel):
    sender: Optional[str] = None
    sender_id: Optional[str] = Field(default=None, alias="senderId")
    sender_phone: Optional[str] = Field(default=None, alias="senderPhone")
    recipient: Optional[str] = None
    recipient_id: Optional[str] = Field(default=None, alias="recipientId")
    recipient_phone: Optional[str] = Field(default=None, alias="recipientPhone")
    recipient_address: Optional[str] = Field(default=None, alias="recipientAddress")
    origin_branch: Optional[str] = Field(default=None, alias="originBranch")
    destination_branch: Optional[str] = Field(default=None, alias="destinationBranch")
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    declared_value: Optional[int] = Field(default=None, alias="declaredValue")
    description: Optional[str] = None
    status: Optional[ParcelStatus] = None


class ParcelStatusUpdate(AppBaseModel):
    status: ParcelStatus


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
    sender: str
    recipient: str
    weight: float
