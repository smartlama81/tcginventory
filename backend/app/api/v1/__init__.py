from fastapi import APIRouter

from app.api.v1 import cards

router = APIRouter()
router.include_router(cards.router, prefix="/cards", tags=["cards"])
