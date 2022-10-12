from typing import List
from fastapi import APIRouter, Body, Response, status, Header
from datetime import datetime
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, Field
from app.routers.link import context_notify
from app.utils.apis import gateway

router = APIRouter(tags=["Gateway"])


# For auth init


class PatientAuthPurpose(str, Enum):
    link = "LINK"
    kyc = "KYC"
    kyc_and_link = "KYC_AND_LINK"


class AuthenticationMode(str, Enum):
    mobile_otp = "MOBILE_OTP"
    direct = "DIRECT"
    aadhaar_otp = "AADHAAR_OTP"
    demographics = "DEMOGRAPHICS"


class PatientAuthRequesterType(str, Enum):
    hip = "HIP"
    hiu = "HIU"


class PatientAuthRequester(BaseModel):
    type: PatientAuthRequesterType = PatientAuthRequesterType.hip
    id: int = Field(example="10005")


class PatientAuthInitRequestQuery(BaseModel):
    id: str = Field(description="id of the patient understood by the CM")
    purpose: PatientAuthPurpose = Field(description="what is the purpose of user auth")
    authMode: AuthenticationMode = Field(
        default=AuthenticationMode.direct, description="Authorization Mode"
    )
    requester: PatientAuthRequester


class PatientAuthInitRequest(BaseModel):
    requestId: UUID
    timestamp: datetime
    query: PatientAuthInitRequestQuery


# For add-contexts


class CareContextRepresentation(BaseModel):
    referenceNumber: str
    display: str


class PatientCareContextLinkPatient(BaseModel):
    refenceNumber: str = Field(
        example="TMH-PUID-001", description="patient reference id at HIP"
    )
    display: str
    careContexts: List[CareContextRepresentation]


class PatientCareContextLink(BaseModel):
    accessToken: str
    patient: PatientCareContextLinkPatient


class PatientCareContextLinkRequest(BaseModel):
    requestId: UUID
    timestamp: datetime
    link: PatientCareContextLink


@router.post("/users/auth/init", status_code=202)
async def init(
    Authorization: str = Header(description="Access Token"),
    X_CM_ID: str = Header(
        description="Suffix of consent manager",
        convert_underscores=True,
    ),
    gatewayBody: PatientAuthInitRequest = Body(),
):
    headers = {"X-CM-ID": X_CM_ID}
    return await gateway.call(
        "/gateway/v0.5/users/auth/init", data=gatewayBody.dict(), headers=headers
    )


@router.post(
    "/links/link/add-contexts", status_code=202, callbacks=context_notify.routes
)
async def add_contexts(
    Authorization: str = Header(description="Access Token"),
    X_CM_ID: str = Header(
        description="Suffix of consent manager",
        convert_underscores=True,
    ),
    gatewayBody: PatientCareContextLinkRequest = Body(),
):

    headers = {"X-CM-ID": X_CM_ID}
    return await gateway.call(
        "/gateway/v0.5/links/link/add-contexts",
        data=gatewayBody.dict(),
        headers=headers,
    )
