from fastapi import FastAPI

from app.routers.base import router
from app.utils.apis import gateway, healthService

app = FastAPI(title="ABDM POC")
app.include_router(router)


@app.on_event("shutdown")
async def close_client():
    await gateway.close()
    await healthService.close()
