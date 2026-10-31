import io
import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Query, UploadFile, HTTPException

from app.core.config import get_settings
from app.core.dependencies import get_delivery_service, get_storage_service, require_permission
from app.schemas.delivery import DeliveryPOD, DeliveryPublic, DeliveryUpdate
from app.schemas.pagination import PaginatedResponse
from app.services.deliveries import DeliveryService
from app.services.storage import StorageService
from app.schemas.user import UserInDB


router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.get("", response_model=PaginatedResponse[DeliveryPublic])
async def list_deliveries(
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: DeliveryService = Depends(get_delivery_service),
    user: UserInDB = Depends(require_permission()),
) -> dict:
    return await service.list(
        page=page,
        page_size=page_size,
        user_branch=user.branch,
        user_role=user.role,
    )


@router.get("/{delivery_id}", response_model=DeliveryPublic)
async def get_delivery(
    delivery_id: str,
    service: DeliveryService = Depends(get_delivery_service),
    user: UserInDB = Depends(require_permission()),
) -> DeliveryPublic:
    return await service.get(delivery_id, user_branch=user.branch, user_role=user.role)


@router.patch("/{delivery_id}", response_model=DeliveryPublic, dependencies=[Depends(require_permission())])
async def update_delivery(
    delivery_id: str,
    payload: DeliveryUpdate,
    service: DeliveryService = Depends(get_delivery_service),
) -> DeliveryPublic:
    return await service.update(delivery_id, payload)


@router.post("/{delivery_id}/pod", response_model=DeliveryPublic, summary="Registrar comprobante de entrega", dependencies=[Depends(require_permission())])
async def add_pod(
    delivery_id: str,
    payload: DeliveryPOD,
    service: DeliveryService = Depends(get_delivery_service),
) -> DeliveryPublic:
    return await service.add_pod(delivery_id, payload)


@router.post("/{delivery_id}/upload", summary="Subir archivo de evidencia (foto/firma)", dependencies=[Depends(require_permission())])
async def upload_evidence(
    delivery_id: str,
    file: UploadFile = File(...),
    service: DeliveryService = Depends(get_delivery_service),
    storage: StorageService = Depends(get_storage_service),
) -> dict:
    content = await file.read()
    file.filename = file.filename or "upload.bin"

    try:
        result = storage.upload_file(
            content=content,
            file_type="deliveries",
            original_filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Actualizar delivery con la URL firmada
    await service.update(delivery_id, DeliveryUpdate(photoUrl=result["url"]))

    return result
