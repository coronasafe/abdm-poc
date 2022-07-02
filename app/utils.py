import os
from typing import TypedDict

from aiohttp import ClientSession
from dotenv import load_dotenv
from fastapi import Header, HTTPException
from fastapi.security import HTTPBearer

load_dotenv(dotenv_path=".env.local")


class Api:
    def __init__(self):
        self.token = None
        self.session = ClientSession("https://dev.ndhm.gov.in", raise_for_status=True)

    async def close(self):
        await self.session.close()

    async def call(self, url: str, data=None):
        if not self.token:
            self.token = await self.get_token()
            self.session.headers.add("Authorization", f"Bearer {self.token}")
        return await self.session.post(url, data)

    async def get_token(self):
        res = await self.session.post(
            "https://dev.abdm.gov.in/gateway/v1/bridges",
            data={
                "clientId": os.environ.get("clientId"),
                "clientSecret": os.environ.get("clientSecret"),
            },
        )
        print("res", res.headers, res)
        return res


api = Api()


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
