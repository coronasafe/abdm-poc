from fastapi import APIRouter
from . import discovery, facilities

router = APIRouter(prefix="/v0.5")
router.include_router(discovery.router, prefix="/care-contexts")
router.include_router(facilities.router, prefix="/facility")
