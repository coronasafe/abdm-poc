from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from ..utils.apis import gateway
from ..utils.db import consents

router = APIRouter(tags=["consents"])


class Notification(BaseModel):
    status: str
    consentId: str
    consentDetails: dict | None = None


class ReqBody(BaseModel):
    requestId: str
    timestamp: str
    signature: str
    grantAcknowledgement: bool
    notification: Notification


@router.post("/notify", status_code=202)
async def notify(body: ReqBody):
    if body.notification.status == "GRANTED":
        consents[body.notification.consentId] = body.notification.consentDetails
        response = {
            "requestId": body.requestId,
            "timestamp": body.timestamp,
            "acknowledgement": {
                "status": "OK",
                "consentId": body.notification.consentId,
            },
            "resp": {"requestId": body.requestId},
        }
        headers = {"X-CM-ID": body.notification.consentDetails["consentManager"]["id"]}
        await gateway.call(
            "/gateway/v0.5/consents/hip/on-notify", data=response, headers=headers
        )
    return Response(status_code=status.HTTP_202_ACCEPTED)
