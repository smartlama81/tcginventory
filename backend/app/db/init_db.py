from sqlalchemy.ext.asyncio import AsyncEngine

from app.db.base import Base
from app.db.session import engine
from app.models import Card  # noqa: F401


async def init_models(async_engine: AsyncEngine | None = None) -> None:
    engine_to_use = async_engine or engine
    async with engine_to_use.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
