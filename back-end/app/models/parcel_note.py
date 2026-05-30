from __future__ import annotations

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class ParcelNote(Base):
    __tablename__ = "parcel_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guide: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[str] = mapped_column(String(20), nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
