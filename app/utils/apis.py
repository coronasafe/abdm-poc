import json
import os

from aiohttp import ClientSession
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()


class Api:
    def __init__(self, base_url: str, require_auth=True, token=None):
        self.token = token
        self.session = ClientSession(base_url, raise_for_status=True)
        self.require_auth = require_auth

    async def close(self):
        await self.session.close()

    async def call(self, relative_url: str, data=None, headers: dict = {}):
        if self.require_auth and not self.token:
            self.token = await self.get_token()
        req_headers = {"Authorization": f"Bearer {self.token}", **headers}
        return await self.session.post(relative_url, json=data, headers=req_headers)

    async def get_token(self):
        async with ClientSession() as session:
            res = await session.post(
                url="https://dev.abdm.gov.in/gateway/v0.5/sessions",
                json={
                    "clientId": os.environ.get("clientId"),
                    "clientSecret": os.environ.get("clientSecret"),
                },
            )
            data = await res.json()
            self.token = data["accessToken"]
            return self.token


gateway = Api("https://dev.abdm.gov.in")
healthService = Api("https://healthidsbx.ndhm.gov.in", require_auth=False)


async def verify_hip(X_HIP_ID: str | None = Header(default=None)):
    if not X_HIP_ID:
        raise HTTPException(status_code=400, detail="X-HIP-ID invalid")


async def verify_abha(healthId: str):
    return await healthService.call(
        "/api/v1/search/existsByHealthId", json={"healthId": healthId}
    )
