from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence, TypeVar

from app.schemas.pagination import PaginatedResponse


T = TypeVar("T")

DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 200


def normalize_page(page: int | None) -> int:
    if not page or page < 1:
        return 1
    return page


def normalize_page_size(page_size: int | None) -> int:
    if not page_size or page_size < 1:
        return DEFAULT_PAGE_SIZE
    return min(page_size, MAX_PAGE_SIZE)


def paginate(items: Sequence[T] | Iterable[T], page: int | None, page_size: int | None) -> List[T]:
    if not isinstance(items, list):
        items = list(items)
    current_page = normalize_page(page)
    size = normalize_page_size(page_size)
    start = (current_page - 1) * size
    end = start + size
    return items[start:end]


def paginate_with_meta(items: Sequence[T] | Iterable[T], page: int | None, page_size: int | None) -> Dict[str, Any]:
    if not isinstance(items, list):
        items = list(items)
    total = len(items)
    p = normalize_page(page)
    s = normalize_page_size(page_size)
    total_pages = max(1, (total + s - 1) // s)
    start = (p - 1) * s
    end = start + s
    return {
        "data": items[start:end],
        "total": total,
        "page": p,
        "pageSize": s,
        "totalPages": total_pages,
    }
