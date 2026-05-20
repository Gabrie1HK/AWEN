from __future__ import annotations

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class TrackingEvent(Base):
    __tablename__ = "tracking_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guide: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    step: Mapped[str] = mapped_column(String(40), nullable=False)
    date: Mapped[str | None] = mapped_column(String(20))
    time: Mapped[str | None] = mapped_column(String(10))
    location: Mapped[str | None] = mapped_column(String(200))
    operator: Mapped[str | None] = mapped_column(String(120))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
