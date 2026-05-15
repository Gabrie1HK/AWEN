from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from app.schemas.base import AppBaseModel


class BatchStatus(str, Enum):
    PENDING = "Pending Assignment"
    ASSIGNED = "Assigned"
    COMPLETED = "Completed"


class VehicleBase(AppBaseModel):
    plate: str
    model: str
    capacity: str
    driver: str


class VehicleCreate(VehicleBase):
    pass


class VehiclePublic(VehicleBase):
    id: int


class BatchBase(AppBaseModel):
    parcels: list[str]
    status: BatchStatus
    vehicle: Optional[str] = None
    driver: Optional[str] = None
    driver_id: Optional[int] = Field(default=None, alias="driverId")
    parcel_count: int = Field(..., alias="parcelCount")


class BatchCreate(AppBaseModel):
    parcels: list[str] = []
    vehicle: Optional[str] = None
    driver: Optional[str] = None
    driver_id: Optional[int] = Field(default=None, alias="driverId")
    status: Optional[BatchStatus] = None


class BatchUpdate(AppBaseModel):
    parcels: Optional[list[str]] = None
    vehicle: Optional[str] = None
    driver: Optional[str] = None
    driver_id: Optional[int] = Field(default=None, alias="driverId")
    status: Optional[BatchStatus] = None


class BatchAssign(AppBaseModel):
    vehicle: str
    driver: str
    driver_id: Optional[int] = Field(default=None, alias="driverId")
    status: Optional[BatchStatus] = None


class BatchPublic(BatchBase):
    id: str
