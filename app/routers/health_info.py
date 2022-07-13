from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from ..utils.apis import gateway

router = APIRouter(tags=["health-information"])


class ReqBody(BaseModel):
    pass


@router.post("/notify", status_code=202)
async def notify(body: ReqBody):
    await gateway.call(
        "/gateway/v0.5/health-information/hip/on-notify", data=body.json()
    )
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/request", status_code=202)
async def notify(body: ReqBody):
    await gateway.call(
        "/gateway/v0.5/health-information/hip/on-request", data=body.json()
    )
    return Response(status_code=status.HTTP_202_ACCEPTED)
