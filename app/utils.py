from typing import TypedDict
from aiohttp import ClientSession
from fastapi import Header, HTTPException

api = ClientSession()


async def verify_auth(Authorization: str | None = Header(default=None)):
    if not Authorization:
        raise HTTPException(status_code=400, detail="Authorization token invalid")


async def verify_hip(X_HIP_ID: str | None = Header(default=None)):
    if not X_HIP_ID:
        raise HTTPException(status_code=400, detail="X-HIP-ID invalid")


class CareContext(TypedDict):
    reference_number: str
    display: str
    details: str


class Patient(TypedDict):
    mobile: str
    name: str
    gender: str
    id: str
    abha: str
    linked: bool
    care_contexts: list[CareContext]


class Facility(TypedDict):
    name: str
    id: str
    patients: list[Patient]


db: list[Facility] = [
    {
        "id": "f1",
        "name": "facility #1",
        "patients": [
            {
                "id": "p1",
                "name": "patient 1",
                "mobile": "999999999",
                "abha": None,
                "gender": "M",
                "linked": False,
                "care_contexts": [],
            },
        ],
    }
]
