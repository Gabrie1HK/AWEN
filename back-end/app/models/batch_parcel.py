from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class BatchParcel(Base):
    __tablename__ = "batch_parcels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    batch_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    parcel_id: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
