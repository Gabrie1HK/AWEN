from fastapi import APIRouter, Depends

from app.core.dependencies import get_notification_service, require_permission
from app.core.pagination import paginate_with_meta
from app.schemas.notification import NotificationSchema
from app.schemas.pagination import PaginatedResponse
from app.services.notifications import NotificationService


router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=PaginatedResponse[NotificationSchema], dependencies=[Depends(require_permission("GET", "/api/v1/notifications"))])
async def list_notifications(
    service: NotificationService = Depends(get_notification_service),
) -> PaginatedResponse[NotificationSchema]:
    items = await service.list()
    return paginate_with_meta(items, page=None, page_size=None)


@router.patch("/{notif_id}/read", dependencies=[Depends(require_permission("PATCH", "/api/v1/notifications/read"))])
async def mark_read(
    notif_id: str,
    service: NotificationService = Depends(get_notification_service),
) -> dict:
    await service.mark_read(notif_id)
    return {"ok": True}


@router.patch("/read-all", dependencies=[Depends(require_permission("PATCH", "/api/v1/notifications/read-all"))])
async def mark_all_read(
    service: NotificationService = Depends(get_notification_service),
) -> dict:
    await service.mark_all_read()
    return {"ok": True}
