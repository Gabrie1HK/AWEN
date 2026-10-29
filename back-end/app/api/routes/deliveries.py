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


router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.get("", response_model=PaginatedResponse[DeliveryPublic], dependencies=[Depends(require_permission())])
async def list_deliveries(
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: DeliveryService = Depends(get_delivery_service),
) -> dict:
    return await service.list(page=page, page_size=page_size)


@router.get("/{delivery_id}", response_model=DeliveryPublic, dependencies=[Depends(require_permission())])
async def get_delivery(
    delivery_id: str,
    service: DeliveryService = Depends(get_delivery_service),
) -> DeliveryPublic:
    return await service.get(delivery_id)


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
    # Validar archivo
    content = await file.read()
    file.filename = file.filename or "upload.bin"

    try:
        storage.validate_file(io.BytesIO(content), file.content_type or "application/octet-stream", file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Generar key única
    key = storage._generate_key("deliveries", file.filename)

    # Subir a storage
    if len(content) <= 5 * 1024 * 1024:  # 5MB threshold
        storage.upload_bytes(content, key, file.content_type or "application/octet-stream")
    else:
        storage.upload_fileobj(io.BytesIO(content), key, file.content_type or "application/octet-stream")

    # Generar pre-signed GET URL para descarga
    download_url = storage.generate_presigned_get_url(key)

    # Actualizar delivery con la URL firmada
    await service.update(delivery_id, DeliveryUpdate(photoUrl=download_url))

    return {"filename": file.filename, "url": download_url, "size": len(content)}
