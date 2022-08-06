from fastapi import APIRouter, Body, Response, status, Header
from datetime import datetime
from uuid import UUID
from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from app.routers.gateway import PatientAuthPurpose, PatientAuthRequester
from app.utils.exception import Acknowledgement, Acknowledgement_Callback, Error

router = APIRouter(tags=["user auth"])


class IdentifierType(str, Enum):
    mr = "MR"
    mobile = "Mobile"
    ndhm_health_number = "NDHM_HEALTH_NUMBER"
    health_id = "HEALTH_ID"


class PatientGender(str, Enum):
    male = "M"
    female = "F"
    other = "O"
    unknown = "U"


class PatientAddress(BaseModel):
    line: str
    district: str
    state: str
    pincode: str


class Identifier(BaseModel):
    type: IdentifierType
    value: str = Field(example="+919800083232")


class PatientAuthStatus(str, Enum):
    granted = "GRANTED"
    denied = "DENIED"


class AccessTokenValidity(BaseModel):
    purpose: PatientAuthPurpose
    requester: PatientAuthRequester
    expiry: datetime
    limit: int = Field(example=1, description="number of times, the token can be used")


class PatientDemographicResponse(BaseModel):
    id: str = Field(
        example="<patient-id>@<consent-manager-id>",
        description="PHR Identifier of patient at consent manager",
    )
    name: str
    gender: PatientGender = PatientGender.male
    yearOfBirth: int = Field(example=2000)
    address: PatientAddress | None = Field(default=None)
    identifiers: List[Identifier]


class PatientAuthNotificationAuth(BaseModel):
    transactionId: str
    status: PatientAuthStatus
    accessToken: str = Field(
        description="string access token for initialization of subsequent action"
    )
    validity: AccessTokenValidity
    patient: PatientDemographicResponse


class PatientAuthNotification(BaseModel):
    requestId: UUID
    timestamp: datetime
    auth: PatientAuthNotificationAuth


class PatientAuthNotificationAcknowledgement(Acknowledgement_Callback):
    pass


auth_notify = APIRouter(prefix="/v0.5")


@auth_notify.post("/users/auth/on-notify")
async def auth_callback(requestBody: PatientAuthNotificationAcknowledgement):
    pass


@router.post("/notify", status_code=202, callbacks=auth_notify.routes)
async def notify(
    Authorization: str = Header(description="Access Token"),
    X_HIP_ID: str = Header(
        description="Identifier of the health information provider to which the request was intended",
        convert_underscores=True,
    ),
    X_HIU_ID: str = Header(
        description="Identifier of the health information user to which the request was intended",
        convert_underscores=True,
    ),
    requestBody: PatientAuthNotification = Body(),
):
    return Response(status_code=status.HTTP_202_ACCEPTED)
