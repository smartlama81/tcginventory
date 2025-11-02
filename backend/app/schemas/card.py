from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CardBase(BaseModel):
    cardmarket_id: Optional[int] = None
    name: str
    collector_number: Optional[str] = None
    rarity: Optional[str] = None
    expansion: Optional[str] = None
    expansion_code: Optional[str] = None
    scryfall_id: Optional[str] = None
    tcgplayer_id: Optional[str] = None


class CardRead(CardBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
