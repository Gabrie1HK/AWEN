from fastapi import APIRouter, Depends, Query

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


@router.post("/{delivery_id}/pod", response_model=DeliveryPublic)
def add_pod(
    delivery_id: str,
    payload: DeliveryPOD,
    service: DeliveryService = Depends(get_delivery_service),
    _user=Depends(get_current_user),
) -> DeliveryPublic:
    return service.add_pod(delivery_id, payload)
