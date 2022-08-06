from app.utils.exception import Acknowledgement_Callback
from fastapi import APIRouter


class PatientCareContextLinkResponse(Acknowledgement_Callback):
    pass


context_notify = APIRouter(prefix="/v0.5")


@context_notify.post("/links/link/on-add-contexts")
async def context_callback(requestBody: PatientCareContextLinkResponse):
    pass
