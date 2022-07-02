from fastapi import APIRouter, FastAPI

from .routers import discovery, links
from .utils import api

app = FastAPI(title="ABDM POC")
root_router = APIRouter(prefix="/v0.5")

root_router.include_router(discovery.router, prefix="/care-contexts")
root_router.include_router(links.router, prefix="/links")

app.include_router(root_router)


@app.on_event("shutdown")
async def close_client():
    await api.close()
