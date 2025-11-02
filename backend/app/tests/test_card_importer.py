from pathlib import Path

import pandas as pd
import pytest
from sqlalchemy import select
from sqlalchemy.engine import make_url

from app.core.config import get_settings
from app.db.init_db import init_models
from app.db.session import AsyncSessionLocal
from app.models import Card
from app.services.card_importer import CardImporter


@pytest.mark.asyncio
async def test_card_importer(tmp_path: Path) -> None:
    settings = get_settings()
    url = make_url(settings.database_url)
    if url.database:
        db_path = Path(url.database)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        if db_path.exists():
            db_path.unlink()

    await init_models()
    csv_path = tmp_path / "cards.csv"
    df = pd.DataFrame(
        [
            {
                "cardmarketId": 1,
                "name": "Pikachu",
                "collectorNumber": "025",
                "rarity": "Common",
                "expansion": "Base Set",
                "expansionCode": "BS",
                "scryfallId": "abc",
                "tcgplayerId": "123",
            },
            {
                "cardmarketId": 2,
                "name": "Charizard",
                "collectorNumber": "004",
                "rarity": "Rare",
                "expansion": "Base Set",
                "expansionCode": "BS",
                "scryfallId": "def",
                "tcgplayerId": "456",
            },
        ]
    )
    df.to_csv(csv_path, index=False)

    async with AsyncSessionLocal() as session:
        importer = CardImporter(session)
        result = await importer.import_file(csv_path)
        assert result == {"created": 2, "updated": 0, "total": 2}

    async with AsyncSessionLocal() as session:
        scalars = await session.scalars(select(Card))
        cards = list(scalars)
        assert len(cards) == 2
        assert sorted(card.name for card in cards) == ["Charizard", "Pikachu"]
