from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationSchema


class NotificationRepository:
    async def list(self) -> List[NotificationSchema]:
        raise NotImplementedError

    async def create(self, payload: NotificationCreate) -> NotificationSchema:
        raise NotImplementedError

    async def mark_read(self, notif_id: str) -> bool:
        raise NotImplementedError

    async def mark_all_read(self) -> None:
        raise NotImplementedError


class InMemoryNotificationRepository(NotificationRepository):
    def __init__(self, initial: Optional[List[NotificationSchema]] = None) -> None:
        self._items: list[NotificationSchema] = initial or []

    async def list(self) -> List[NotificationSchema]:
        return list(reversed(self._items))

    async def create(self, payload: NotificationCreate) -> NotificationSchema:
        now = datetime.now(timezone.utc)
        notif = NotificationSchema(
            id=str(int(now.timestamp() * 1000)),
            user_id=payload.user_id,
            text=payload.text,
            time=now.strftime("%H:%M"),
            created_at=now.isoformat(),
            read=False,
            action_type=payload.action_type,
            related_id=payload.related_id,
        )
        self._items.append(notif)
        return notif

    async def mark_read(self, notif_id: str) -> bool:
        for item in self._items:
            if item.id == notif_id:
                item.read = True
                return True
        return False

    async def mark_all_read(self) -> None:
        for item in self._items:
            item.read = True


class SqlAlchemyNotificationRepository(NotificationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self) -> List[NotificationSchema]:
        result = await self._session.execute(
            select(Notification).order_by(Notification.created_at.desc())
        )
        items = result.scalars().all()
        return [self._to_schema(item) for item in items]

    async def create(self, payload: NotificationCreate) -> NotificationSchema:
        now = datetime.now(timezone.utc)
        record = Notification(
            id=str(int(now.timestamp() * 1000)),
            user_id=payload.user_id,
            text=payload.text,
            time=now.strftime("%H:%M"),
            created_at=now.isoformat(),
            read=False,
            action_type=payload.action_type,
            related_id=payload.related_id,
        )
        self._session.add(record)
        await self._session.commit()
        return self._to_schema(record)

    async def mark_read(self, notif_id: str) -> bool:
        notif = await self._session.get(Notification, notif_id)
        if not notif:
            return False
        notif.read = True
        await self._session.commit()
        return True

    async def mark_all_read(self) -> None:
        result = await self._session.execute(select(Notification))
        items = result.scalars().all()
        for item in items:
            item.read = True
        await self._session.commit()

    @staticmethod
    def _to_schema(item: Notification) -> NotificationSchema:
        return NotificationSchema(
            id=item.id,
            user_id=item.user_id,
            text=item.text,
            time=item.time,
            created_at=item.created_at,
            read=item.read,
            action_type=item.action_type,
            related_id=item.related_id,
        )
