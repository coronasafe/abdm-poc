from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel


class Error(BaseModel):
    code: int
    message: str


class Status(str, Enum):
    ok = "OK"


class Acknowledgement(BaseModel):
    status: Status


class RequestReference(BaseModel):
    requestId: UUID


class Acknowledgement_Callback(BaseModel):
    requestId: UUID
    timestamp: datetime
    acknowledgement: Acknowledgement | None = None
    error: Error | None = None
    resp: RequestReference
