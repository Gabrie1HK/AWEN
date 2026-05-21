from __future__ import annotations

import asyncio

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import StreamingResponse

from app.core.dependencies import get_auth_service
from app.services.auth import AuthService
from app.services.broadcaster import broadcaster


router = APIRouter(tags=["notifications"])


async def _get_user_from_token(
    token: str = Query(default="", description="JWT token for SSE auth"),
    service: AuthService = Depends(get_auth_service),
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return await service.get_current_user(token)


@router.get("/notifications/stream")
async def notification_stream(_user=Depends(_get_user_from_token)):
    queue = broadcaster.subscribe()

    async def event_generator():
        try:
            while True:
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield f"data: {data}\n\n"
                except asyncio.TimeoutError:
                    yield "data: {\"type\":\"ping\"}\n\n"
        finally:
            broadcaster.unsubscribe(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
