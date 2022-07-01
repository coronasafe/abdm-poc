from fastapi import APIRouter, Depends
from app.utils import api, verify_auth, verify_hip

router = APIRouter(
    tags=["link"], dependencies=[Depends(verify_auth), Depends(verify_hip)]
)


@router.post("/link/init")
async def init():
    await api.post("/links/link/on-init")
    return {}


@router.post("/link/confirm")
async def confirm():
    await api.post("/links/link/on-confirm")
    return {}
