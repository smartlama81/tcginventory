from fastapi import FastAPI

from app.api.v1 import router as api_router

app = FastAPI(title="TCG Inventory Backend", version="0.1.0")

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
