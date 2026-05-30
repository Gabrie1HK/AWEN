from __future__ import annotations

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Parcel(Base):
    __tablename__ = "parcels"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    guide: Mapped[str] = mapped_column(String(40), unique=True, index=True, nullable=False)
    sender: Mapped[str] = mapped_column(String(120), nullable=False)
    sender_id: Mapped[str] = mapped_column(String(40), nullable=False)
    sender_phone: Mapped[str] = mapped_column(String(40), nullable=False)
    recipient: Mapped[str] = mapped_column(String(120), nullable=False)
    recipient_id: Mapped[str] = mapped_column(String(40), nullable=False)
    recipient_phone: Mapped[str] = mapped_column(String(40), nullable=False)
    recipient_address: Mapped[str] = mapped_column(String(200), nullable=False)
    origin_address: Mapped[str | None] = mapped_column(String(200))
    origin_lat: Mapped[float | None] = mapped_column(Float)
    origin_lng: Mapped[float | None] = mapped_column(Float)
    destination_address: Mapped[str | None] = mapped_column(String(200))
    destination_lat: Mapped[float | None] = mapped_column(Float)
    destination_lng: Mapped[float | None] = mapped_column(Float)
    origin_branch: Mapped[str] = mapped_column(String(120), nullable=False)
    destination_branch: Mapped[str] = mapped_column(String(120), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    dimensions: Mapped[str] = mapped_column(String(60), nullable=False)
    declared_value: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[str] = mapped_column(String(20), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(20), nullable=False)
    qr_data: Mapped[str] = mapped_column(String(60), nullable=False)
    barcode: Mapped[str] = mapped_column(String(60), nullable=False)
