import asyncio
import sys
import time

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router as api_router
from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging
from app.core.ratelimit import RateLimitMiddleware


def create_app() -> FastAPI:
    setup_logging()
    settings = get_settings()
    logger = get_logger("app")
    logger.info("Starting %s v%s", settings.project_name, settings.version)

    application = FastAPI(
        title=settings.project_name,
        version=settings.version,
        description="API de gestion de encomiendas AWEN. Proporciona autenticacion JWT, CRUD de encomiendas, tracking publico, logistica, reportes y mas.",
        openapi_tags=[
            {"name": "health", "description": "Health check del servicio"},
            {"name": "auth", "description": "Autenticacion y sesion de usuarios"},
            {"name": "parcels", "description": "Gestion de encomiendas (CRUD, estados, cancelacion)"},
            {"name": "tracking", "description": "Tracking publico de encomiendas (sin autenticacion)"},
            {"name": "logistics", "description": "Logistica: lotes y vehiculos"},
            {"name": "dashboard", "description": "KPIs y graficos del dashboard"},
            {"name": "reports", "description": "Reportes, resumenes y exportacion CSV"},
            {"name": "users", "description": "Gestion de usuarios del sistema"},
            {"name": "branches", "description": "Gestion de sucursales"},
            {"name": "deliveries", "description": "Comprobantes de entrega (POD)"},
        ],
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    application.add_middleware(
        RateLimitMiddleware,
        max_requests=settings.rate_limit_max,
        window_seconds=settings.rate_limit_window,
    )

    @application.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        logger.info(
            "%s %s -> %d (%.0fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration * 1000,
        )
        return response

    application.include_router(api_router, prefix=settings.api_v1_prefix)

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    application.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

    return application


app = create_app()

