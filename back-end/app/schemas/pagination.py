from __future__ import annotations

from typing import Generic, List, TypeVar

from app.schemas.base import AppBaseModel

T = TypeVar("T")


class PaginatedResponse(AppBaseModel, Generic[T]):
    data: List[T]
    total: int
    page: int
    pageSize: int
    totalPages: int
