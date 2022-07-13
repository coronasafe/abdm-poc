from fastapi import APIRouter, Response, status
from pydantic import HttpUrl, BaseModel
from ..utils.apis import gateway

router = APIRouter(tags=["facility"])


class HIPUrlBody(BaseModel):
    url: HttpUrl


@router.post("/set-hip-url")
async def set_hip_url(req: HIPUrlBody):
    try:
        await gateway.call("/devservice/v1/bridges", data=req.json())
    except Exception as e:
        print(e)
    return Response(status_code=status.HTTP_202_ACCEPTED)


class FacilityData(BaseModel):
    facility_id: str
    name: str
    facility_type: str
    active: bool
    alias: list


@router.post("/set-facility")
async def set_facility(req: FacilityData):
    try:
        await gateway.call("/devservice/v1/bridges/services", data=req.json())
    except Exception as e:
        print(e)
    return Response(status_code=status.HTTP_202_ACCEPTED)
