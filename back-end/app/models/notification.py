from __future__ import annotations

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(String(300), nullable=False)
    time: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[str] = mapped_column(String(40), nullable=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    action_type: Mapped[str] = mapped_column(String(40), nullable=False)
    related_id: Mapped[str | None] = mapped_column(String(40))
