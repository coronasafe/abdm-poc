from fastapi import APIRouter
from . import discovery, facilities, consents, health_info

router = APIRouter(prefix="/v0.5")
router.include_router(discovery.router, prefix="/care-contexts")
router.include_router(facilities.router, prefix="/facility")
router.include_router(consents.router, prefix="/consents/hip")
router.include_router(health_info.router, prefix="/health-information/hip")
