from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    vehicle: Mapped[str | None] = mapped_column(String(20))
    driver: Mapped[str | None] = mapped_column(String(120))
    driver_id: Mapped[int | None] = mapped_column(Integer)
    parcel_count: Mapped[int] = mapped_column(Integer, nullable=False)
