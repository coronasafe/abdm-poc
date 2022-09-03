from pydantic import BaseModel
from fastapi import APIRouter, Header
from app.utils.apis import healthService


class MobileOtpReqBody(BaseModel):
    mobile: str


class ABHAReqBody(BaseModel):
    address: str
    dayOfBirth: str
    districtCode: str
    email: str
    firstName: str
    gender: str
    # healthId: str
    lastName: str
    middleName: str
    address: str
    dayOfBirth: str
    districtCode: str
    email: str
    firstName: str
    gender: str
    healthId: str
    lastName: str
    middleName: str
    monthOfBirth: str
    name: str
    password: str
    pincode: str
    profilePhoto: str
    restrictions: str
    stateCode: str
    subdistrictCode: str
    token: str
    townCode: str
    txnId: str
    villageCode: str
    wardCode: str
    yearOfBirth: str


class VerifyOtpReqBody(BaseModel):
    otp: str
    txnId: str


router = APIRouter(tags=["Registration"])


@router.post("/sendMobileOtp")
async def register(requestBody: MobileOtpReqBody, X_HIP_ID: str = Header(default=None)):
    return await healthService.call(
        "v1/registration/mobile/generateOtp ", requestBody.dict()
    )


@router.post("/verifyMobileOtp")
async def verify(requestBody: VerifyOtpReqBody, X_HIP_ID: str = Header(default=None)):
    return await healthService.call(
        "/v1/registration/mobile/verifyOtp", requestBody.dict()
    )


@router.post("/createABHA")
async def verify(requestBody: ABHAReqBody, X_HIP_ID: str = Header(default=None)):
    return await healthService.call(
        "/v1/registration/mobile/createHealthId", requestBody.dict()
    )


@router.post("/verifyABHA")
async def verify_abha(healthId: str, X_HIP_ID: str = Header(default=None)):
    res = await healthService.call(
        "/api/v1/search/existsByHealthId", data={"healthId": healthId}
    )
    return res.ok
