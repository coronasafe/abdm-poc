from fastapi import APIRouter, Depends, Response, status
from utils import api, verify_hip

router = APIRouter(tags=["link"], dependencies=[Depends(verify_hip)])


@router.post("/link/init")
async def init():
    await api.post("/links/link/on-init")
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/link/confirm")
async def confirm():
    await api.post("/links/link/on-confirm")
    return Response(status_code=status.HTTP_202_ACCEPTED)
