import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Query, UploadFile

from app.core.config import get_settings

from app.core.dependencies import get_current_user, get_delivery_service
from app.schemas.delivery import DeliveryPOD, DeliveryPublic, DeliveryUpdate
from app.services.deliveries import DeliveryService


router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.get("", response_model=list[DeliveryPublic])
def list_deliveries(
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: DeliveryService = Depends(get_delivery_service),
    _user=Depends(get_current_user),
) -> list[DeliveryPublic]:
    return service.list(page=page, page_size=page_size)


@router.get("/{delivery_id}", response_model=DeliveryPublic)
def get_delivery(
    delivery_id: str,
    service: DeliveryService = Depends(get_delivery_service),
    _user=Depends(get_current_user),
) -> DeliveryPublic:
    return service.get(delivery_id)


@router.patch("/{delivery_id}", response_model=DeliveryPublic)
def update_delivery(
    delivery_id: str,
    payload: DeliveryUpdate,
    service: DeliveryService = Depends(get_delivery_service),
    _user=Depends(get_current_user),
) -> DeliveryPublic:
    return service.update(delivery_id, payload)


@router.post("/{delivery_id}/pod", response_model=DeliveryPublic, summary="Registrar comprobante de entrega")
def add_pod(
    delivery_id: str,
    payload: DeliveryPOD,
    service: DeliveryService = Depends(get_delivery_service),
    _user=Depends(get_current_user),
) -> DeliveryPublic:
    return service.add_pod(delivery_id, payload)


@router.post("/{delivery_id}/upload", summary="Subir archivo de evidencia (foto/firma)")
def upload_evidence(
    delivery_id: str,
    file: UploadFile = File(...),
    service: DeliveryService = Depends(get_delivery_service),
    _user=Depends(get_current_user),
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
    service.update(
        delivery_id,
        DeliveryUpdate(photoUrl=relative_url),
    )
    return {"filename": filename, "url": relative_url, "size": len(content)}
