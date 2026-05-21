from __future__ import annotations

from typing import List, Optional

from app.repositories.notifications import NotificationRepository
from app.schemas.notification import NotificationCreate, NotificationSchema
from app.services.broadcaster import broadcaster


class NotificationService:
    def __init__(self, repo: NotificationRepository) -> None:
        self._repo = repo

    async def list(self) -> List[NotificationSchema]:
        return await self._repo.list()

    async def create(self, text: str, action_type: str, related_id: Optional[str] = None, user_id: Optional[str] = None) -> NotificationSchema:
        payload = NotificationCreate(text=text, action_type=action_type, related_id=related_id, user_id=user_id)
        result = await self._repo.create(payload)
        await broadcaster.publish({
            "type": "notification",
            "data": result.model_dump(by_alias=True),
        })
        return result

    async def mark_read(self, notif_id: str) -> bool:
        return await self._repo.mark_read(notif_id)

    async def mark_all_read(self) -> None:
        await self._repo.mark_all_read()
