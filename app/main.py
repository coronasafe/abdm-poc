from fastapi import FastAPI

from .routers.base import router
from .utils.apis import gateway

app = FastAPI(title="ABDM POC")
app.include_router(router)


@app.on_event("shutdown")
async def close_client():
    await gateway.close()
