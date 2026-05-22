from __future__ import annotations

from typing import Optional

from app.schemas.base import AppBaseModel


class NotificationSchema(AppBaseModel):
    id: str
    user_id: Optional[int] = None
    text: str
    time: str
    created_at: str
    read: bool = False
    action_type: str
    related_id: Optional[str] = None


class NotificationCreate(AppBaseModel):
    text: str
    action_type: str
    related_id: Optional[str] = None
    user_id: Optional[int] = None
