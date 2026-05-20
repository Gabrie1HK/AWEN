from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_notification_service
from app.core.pagination import paginate_with_meta
from app.schemas.notification import NotificationSchema
from app.schemas.pagination import PaginatedResponse
from app.services.notifications import NotificationService


router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=PaginatedResponse[NotificationSchema])
async def list_notifications(
    service: NotificationService = Depends(get_notification_service),
    _user=Depends(get_current_user),
) -> PaginatedResponse[NotificationSchema]:
    items = await service.list()
    return paginate_with_meta(items, page=None, page_size=None)


@router.patch("/{notif_id}/read")
async def mark_read(
    notif_id: str,
    service: NotificationService = Depends(get_notification_service),
    _user=Depends(get_current_user),
) -> dict:
    await service.mark_read(notif_id)
    return {"ok": True}


@router.patch("/read-all")
async def mark_all_read(
    service: NotificationService = Depends(get_notification_service),
    _user=Depends(get_current_user),
) -> dict:
    await service.mark_all_read()
    return {"ok": True}
