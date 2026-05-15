from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user, get_logistics_service
from app.schemas.logistics import (
    BatchAssign,
    BatchCreate,
    BatchPublic,
    BatchUpdate,
    VehicleCreate,
    VehiclePublic,
)
from app.services.logistics import LogisticsService


router = APIRouter(prefix="/logistics", tags=["logistics"])


@router.get("/batches", response_model=list[BatchPublic], summary="Listar lotes")
def list_batches(
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: LogisticsService = Depends(get_logistics_service),
    _user=Depends(get_current_user),
) -> list[BatchPublic]:
    return service.list_batches(page=page, page_size=page_size)


@router.get("/batches/{batch_id}", response_model=BatchPublic)
def get_batch(
    batch_id: str,
    service: LogisticsService = Depends(get_logistics_service),
    _user=Depends(get_current_user),
) -> BatchPublic:
    return service.get_batch(batch_id)


@router.post("/batches", response_model=BatchPublic)
def create_batch(
    payload: BatchCreate,
    service: LogisticsService = Depends(get_logistics_service),
    _user=Depends(get_current_user),
) -> BatchPublic:
    return service.create_batch(payload)


@router.patch("/batches/{batch_id}", response_model=BatchPublic)
def update_batch(
    batch_id: str,
    payload: BatchUpdate,
    service: LogisticsService = Depends(get_logistics_service),
    _user=Depends(get_current_user),
) -> BatchPublic:
    return service.update_batch(batch_id, payload)


@router.post("/batches/{batch_id}/assign", response_model=BatchPublic, summary="Asignar lote a vehiculo")
def assign_batch(
    batch_id: str,
    payload: BatchAssign,
    service: LogisticsService = Depends(get_logistics_service),
    _user=Depends(get_current_user),
) -> BatchPublic:
    return service.assign_batch(batch_id, payload)


@router.get("/vehicles", response_model=list[VehiclePublic])
def list_vehicles(
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: LogisticsService = Depends(get_logistics_service),
    _user=Depends(get_current_user),
) -> list[VehiclePublic]:
    return service.list_vehicles(page=page, page_size=page_size)


@router.post("/vehicles", response_model=VehiclePublic)
def create_vehicle(
    payload: VehicleCreate,
    service: LogisticsService = Depends(get_logistics_service),
    _user=Depends(get_current_user),
) -> VehiclePublic:
    return service.create_vehicle(payload)
