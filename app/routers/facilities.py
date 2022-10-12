from typing import List
from fastapi import APIRouter, Response, status
from pydantic import HttpUrl, BaseModel
from app.utils.apis import gateway

router = APIRouter(tags=["facility"])


class HIPUrlBody(BaseModel):
    url: HttpUrl


@router.post("/set-hip-url")
async def set_hip_url(req: HIPUrlBody):
    return await gateway.call("/gateway/v1/bridges", data=req.dict(), method="PATCH")


class FacilityData(BaseModel):
    facility_id: str
    name: str
    facility_type: str
    active: bool
    alias: list


@router.post("/set-facility")
async def set_facility(req: FacilityData):
    return await gateway.call("/gateway/v1/bridges/services", data=req.dict())


class FacilityEndpoint(BaseModel):
    address: str
    connectionType: str
    use: str


class FacilityLinkData(BaseModel):
    id: str
    name: str
    type: str
    active: bool
    alias: List[str]
    endpoints: List[FacilityEndpoint]


@router.post("/link-facility")
async def link_facility(req: FacilityLinkData):
    return await gateway.call("/gateway/v1/bridges/addUpdateServices", data=req.dict())
