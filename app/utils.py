from aiohttp import ClientSession
from fastapi import Header, HTTPException

api = ClientSession()


async def verify_auth(Authorization: str | None = Header(default=None)):
    if not Authorization:
        raise HTTPException(status_code=400, detail="Authorization token invalid")


async def verify_hip(X_HIP_ID: str | None = Header(default=None)):
    if not X_HIP_ID:
        raise HTTPException(status_code=400, detail="X-HIP-ID invalid")
