from fastapi import APIRouter, Depends
from app.utils import api, verify_auth, verify_hip

router = APIRouter(
    tags=["discovery"], dependencies=[Depends(verify_auth), Depends(verify_hip)]
)


@router.post("/discover")
async def discover():
    await api.post("/care-contexts/on-discover")
    return {}
