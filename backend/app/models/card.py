from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cardmarket_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    collector_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    rarity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    expansion: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    expansion_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)
    scryfall_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    tcgplayer_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
