from typing import Any, TypedDict
from app.utils.apis import gateway, verify_hip
from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel

router = APIRouter(tags=["discovery"], dependencies=[Depends(verify_hip)])


class PatientIdentifiers(TypedDict):
    id: str
    name: str
    gender: str
    yearOfBirth: str
    verifiedIdentifiers: list[dict[str, Any]]
    unverifiedIdentifiers: list[dict[str, Any]]


class ReqBody(BaseModel):
    requestId: str
    timestamp: str
    transactionId: str
    patient: PatientIdentifiers


@router.post("/discover", status_code=202)
async def discover(body: ReqBody):
    return await gateway.call(
        "/devservice/gateway/v0.5/care-contexts/on-discover", data=body.dict()
    )
