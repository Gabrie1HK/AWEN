import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Query, UploadFile

from app.core.config import get_settings
from app.core.dependencies import get_delivery_service, require_permission
from app.schemas.delivery import DeliveryPOD, DeliveryPublic, DeliveryUpdate
from app.schemas.pagination import PaginatedResponse
from app.services.deliveries import DeliveryService


router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.get("", response_model=PaginatedResponse[DeliveryPublic], dependencies=[Depends(require_permission("GET", "/api/v1/deliveries"))])
async def list_deliveries(
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: DeliveryService = Depends(get_delivery_service),
) -> dict:
    return await service.list(page=page, page_size=page_size)


@router.get("/{delivery_id}", response_model=DeliveryPublic, dependencies=[Depends(require_permission("GET", "/api/v1/deliveries/"))])
async def get_delivery(
    delivery_id: str,
    service: DeliveryService = Depends(get_delivery_service),
) -> DeliveryPublic:
    return await service.get(delivery_id)


@router.patch("/{delivery_id}", response_model=DeliveryPublic, dependencies=[Depends(require_permission("PATCH", "/api/v1/deliveries/"))])
async def update_delivery(
    delivery_id: str,
    payload: DeliveryUpdate,
    service: DeliveryService = Depends(get_delivery_service),
) -> DeliveryPublic:
    return await service.update(delivery_id, payload)


@router.post("/{delivery_id}/pod", response_model=DeliveryPublic, summary="Registrar comprobante de entrega", dependencies=[Depends(require_permission("POST", "/api/v1/deliveries/pod"))])
async def add_pod(
    delivery_id: str,
    payload: DeliveryPOD,
    service: DeliveryService = Depends(get_delivery_service),
) -> DeliveryPublic:
    return await service.add_pod(delivery_id, payload)


@router.post("/{delivery_id}/upload", summary="Subir archivo de evidencia (foto/firma)", dependencies=[Depends(require_permission("POST", "/api/v1/deliveries/upload"))])
async def upload_evidence(
    delivery_id: str,
    file: UploadFile = File(...),
    service: DeliveryService = Depends(get_delivery_service),
) -> dict:
    settings = get_settings()
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix if file.filename else ".bin"
    filename = f"{delivery_id}_{uuid.uuid4().hex}{ext}"
    filepath = upload_dir / filename

    content = file.file.read()
    filepath.write_bytes(content)

    relative_url = f"/uploads/{filename}"
    await service.update(
        delivery_id,
        DeliveryUpdate(photoUrl=relative_url),
    )
    return {"filename": filename, "url": relative_url, "size": len(content)}
