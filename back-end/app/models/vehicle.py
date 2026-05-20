from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plate: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    capacity: Mapped[str] = mapped_column(String(40), nullable=False)
    driver: Mapped[str | None] = mapped_column(String(120))
