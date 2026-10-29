from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_logistics_service, require_permission
from app.schemas.logistics import (
    BatchAssign,
    BatchCreate,
    BatchPublic,
    BatchUpdate,
    VehicleCreate,
    VehiclePublic,
)
from app.schemas.pagination import PaginatedResponse
from app.services.logistics import LogisticsService
from app.schemas.user import UserInDB


router = APIRouter(prefix="/logistics", tags=["logistics"])


@router.get("/batches", response_model=PaginatedResponse[BatchPublic], summary="Listar lotes")
async def list_batches(
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: LogisticsService = Depends(get_logistics_service),
    user: UserInDB = Depends(require_permission()),
) -> dict:
    return await service.list_batches(page=page, page_size=page_size, user_branch=user.branch, user_role=user.role)


@router.get("/batches/{batch_id}", response_model=BatchPublic)
async def get_batch(
    batch_id: str,
    service: LogisticsService = Depends(get_logistics_service),
    user: UserInDB = Depends(require_permission()),
) -> BatchPublic:
    return await service.get_batch(batch_id, user_branch=user.branch, user_role=user.role)


@router.post("/batches", response_model=BatchPublic, dependencies=[Depends(require_permission())])
async def create_batch(
    payload: BatchCreate,
    service: LogisticsService = Depends(get_logistics_service),
) -> BatchPublic:
    return await service.create_batch(payload)


@router.patch("/batches/{batch_id}", response_model=BatchPublic, dependencies=[Depends(require_permission())])
async def update_batch(
    batch_id: str,
    payload: BatchUpdate,
    service: LogisticsService = Depends(get_logistics_service),
) -> BatchPublic:
    return await service.update_batch(batch_id, payload)


@router.post("/batches/{batch_id}/assign", response_model=BatchPublic, summary="Asignar lote a vehiculo", dependencies=[Depends(require_permission())])
async def assign_batch(
    batch_id: str,
    payload: BatchAssign,
    service: LogisticsService = Depends(get_logistics_service),
) -> BatchPublic:
    return await service.assign_batch(batch_id, payload)


@router.get("/vehicles", response_model=PaginatedResponse[VehiclePublic])
async def list_vehicles(
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: LogisticsService = Depends(get_logistics_service),
    user: UserInDB = Depends(require_permission()),
) -> dict:
    return await service.list_vehicles(page=page, page_size=page_size, user_branch=user.branch, user_role=user.role)


@router.post("/vehicles", response_model=VehiclePublic, dependencies=[Depends(require_permission())])
async def create_vehicle(
    payload: VehicleCreate,
    service: LogisticsService = Depends(get_logistics_service),
) -> VehiclePublic:
    return await service.create_vehicle(payload)
