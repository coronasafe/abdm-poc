from fastapi import FastAPI, APIRouter
from routers import discovery, links

app = FastAPI(title="ABDM POC")
root_router = APIRouter(prefix="/v0.5")

root_router.include_router(discovery.router, prefix="/care-contexts")
root_router.include_router(links.router, prefix="/links")

app.include_router(root_router)


@app.get("/")
async def root():
    return {"message": "API Working"}
