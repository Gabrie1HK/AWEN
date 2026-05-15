from __future__ import annotations

import time
from collections import defaultdict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - self.window_seconds

        requests = self._requests[client_ip]
        requests[:] = [t for t in requests if t > window_start]

        if len(requests) >= self.max_requests:
            return Response(
                status_code=429,
                content='{"message": "Demasiadas solicitudes. Intente de nuevo mas tarde."}',
                media_type="application/json",
                headers={"Retry-After": str(int(self.window_seconds))},
            )

        requests.append(now)
        return await call_next(request)
