import os

from aiohttp import ClientSession
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()


class Api:
    def __init__(self, base_url: str):
        self.token = None
        self.session = ClientSession(base_url, raise_for_status=True)

    async def close(self):
        await self.session.close()

    async def call(self, url: str, data=None):
        if not self.token:
            self.token = await self.get_token()
            self.session.headers.add("Authorization", f"Bearer {self.token}")
        return await self.session.post(url, json=data)

    async def get_token(self):
        res = await self.session.post(
            url="/gateway/v0.5/sessions",
            json={
                "clientId": os.environ.get("clientId"),
                "clientSecret": os.environ.get("clientSecret"),
            },
        )

        data = await res.json()
        self.token = data["accessToken"]
        return self.token


gateway = Api("https://dev.abdm.gov.in")


async def verify_hip(X_HIP_ID: str | None = Header(default=None)):
    if not X_HIP_ID:
        raise HTTPException(status_code=400, detail="X-HIP-ID invalid")
