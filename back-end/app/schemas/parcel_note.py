from __future__ import annotations

from typing import Optional

from pydantic import Field

from app.schemas.base import AppBaseModel


class ParcelNoteCreate(AppBaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    is_public: bool = False


class ParcelNotePublic(AppBaseModel):
    id: int
    guide: str
    text: str
    created_by: str
    created_at: str
    is_public: bool
