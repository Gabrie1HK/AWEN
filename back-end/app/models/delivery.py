from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    guide: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    recipient: Mapped[str] = mapped_column(String(120), nullable=False)
    driver: Mapped[str] = mapped_column(String(120), nullable=False)
    delivery_date: Mapped[str | None] = mapped_column(String(20))
    pod_type: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    signature_data: Mapped[str | None] = mapped_column(String(500))
    photo_url: Mapped[str | None] = mapped_column(String(200))
    gps: Mapped[str | None] = mapped_column(String(40))
