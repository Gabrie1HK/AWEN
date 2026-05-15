from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.branches import router as branches_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.deliveries import router as deliveries_router
from app.api.routes.logistics import router as logistics_router
from app.api.routes.parcels import router as parcels_router
from app.api.routes.reports import router as reports_router
from app.api.routes.tracking import router as tracking_router
from app.api.routes.users import router as users_router

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}


router.include_router(auth_router)
router.include_router(parcels_router)
router.include_router(tracking_router)
router.include_router(logistics_router)
router.include_router(reports_router)
router.include_router(dashboard_router)
router.include_router(users_router)
router.include_router(branches_router)
router.include_router(deliveries_router)
