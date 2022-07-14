from aiohttp import ClientSession
from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from ..utils.apis import gateway
from ..utils.db import consents
from ..utils.crypt import crypt

router = APIRouter(tags=["health-information"])


class InfoReq(BaseModel):
    consent: dict
    dateRange: dict
    dataPushUrl: str
    keyMaterial: dict
    nonce: str


class ReqBody(BaseModel):
    requestId: str
    timestamp: str
    transactionId: str
    hiRequest: InfoReq


@router.post("/request", status_code=202)
async def notify(body: ReqBody):
    if body.hiRequest.consent["id"] in consents:
        resp = {
            "requestId": body.requestId,
            "timestamp": body.timestamp,
            "hiRequest": {
                "transactionId": body.transactionId,
                "sessionStatus": "ACKNOWLEDGED",
            },
            "resp": {"requestId": body.requestId},
        }
        headers = {"X-CM-ID": consents[body.hiRequest.consent["id"]]}
        await gateway.call(
            "/gateway/v0.5/health-information/hip/on-request",
            data=resp,
            headers=headers,
        )
        public_key = body.hiRequest.keyMaterial["dhPublicKey"]["keyValue"]
        nonce = body.hiRequest.keyMaterial["dhPublicKey"]["parameters"]
        data = []
        health_info = crypt.encrypt(public_key, bytes(data), nonce)
        data = {
            "pageNumber": 0,
            "pageCount": 0,
            "transactionId": body.transactionId,
            "entries": health_info,
            "keyMaterial": {
                "curve": "Curve25519",
                "dhPublicKey": {
                    "expiry": "",
                    "parameters": crypt.random,
                    "keyValue": crypt.public_key_bytes,
                },
            },
            "nonce": "",
        }
        async with ClientSession() as session:
            await session.post(
                body.hiRequest.dataPushUrl,
                json=data,
                headers={"Authorization": f"Bearer {gateway.token}"},
            )

    return Response(status_code=status.HTTP_202_ACCEPTED)
