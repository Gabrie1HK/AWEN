from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from app.schemas.base import AppBaseModel


class DeliveryStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"


class PodType(str, Enum):
    SIGNATURE = "Signature"
    PHOTO = "Photo"


class DeliveryBase(AppBaseModel):
    guide: str
    recipient: str
    driver: str
    delivery_date: Optional[str] = Field(default=None, alias="deliveryDate")
    pod_type: PodType = Field(..., alias="podType")
    status: DeliveryStatus
    signature_data: Optional[str] = Field(default=None, alias="signatureData")
    photo_url: Optional[str] = Field(default=None, alias="photoUrl")
    gps: Optional[str] = None


class DeliveryCreate(DeliveryBase):
    pass


class DeliveryUpdate(AppBaseModel):
    guide: Optional[str] = None
    recipient: Optional[str] = None
    driver: Optional[str] = None
    delivery_date: Optional[str] = Field(default=None, alias="deliveryDate")
    pod_type: Optional[PodType] = Field(default=None, alias="podType")
    status: Optional[DeliveryStatus] = None
    signature_data: Optional[str] = Field(default=None, alias="signatureData")
    photo_url: Optional[str] = Field(default=None, alias="photoUrl")
    gps: Optional[str] = None


class DeliveryPOD(AppBaseModel):
    pod_type: PodType = Field(..., alias="podType")
    signature_data: Optional[str] = Field(default=None, alias="signatureData")
    photo_url: Optional[str] = Field(default=None, alias="photoUrl")
    gps: Optional[str] = None
    delivery_date: Optional[str] = Field(default=None, alias="deliveryDate")


class DeliveryPublic(DeliveryBase):
    id: str
