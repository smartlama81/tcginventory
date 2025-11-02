from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Card


class CardImporter:
    """Service that synchronises the master card list into the database."""

    EXPECTED_COLUMNS = {
        "cardmarketId": "cardmarket_id",
        "name": "name",
        "collectorNumber": "collector_number",
        "rarity": "rarity",
        "expansion": "expansion",
        "expansionCode": "expansion_code",
        "scryfallId": "scryfall_id",
        "tcgplayerId": "tcgplayer_id",
    }

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def import_file(self, csv_path: Path) -> dict[str, Any]:
        df = self._load_dataframe(csv_path)
        created = 0
        updated = 0

        for record in df.to_dict(orient="records"):
            payload = self._normalise_record(record)
            card = await self._find_existing(payload["cardmarket_id"])
            if card:
                for key, value in payload.items():
                    setattr(card, key, value)
                updated += 1
            else:
                card = Card(**payload)
                self.session.add(card)
                created += 1

        await self.session.commit()
        return {"created": created, "updated": updated, "total": int(df.shape[0])}

    async def _find_existing(self, cardmarket_id: int | None) -> Card | None:
        if cardmarket_id is None:
            return None
        stmt = select(Card).where(Card.cardmarket_id == cardmarket_id)
        result = await self.session.scalars(stmt)
        return result.first()

    def _load_dataframe(self, csv_path: Path) -> pd.DataFrame:
        if not csv_path.exists():
            raise FileNotFoundError(csv_path)
        df = pd.read_csv(csv_path)
        missing_columns = set(self.EXPECTED_COLUMNS).difference(df.columns)
        if missing_columns:
            raise ValueError(f"CSV file is missing required columns: {', '.join(sorted(missing_columns))}")
        return df[list(self.EXPECTED_COLUMNS.keys())]

    def _normalise_record(self, record: dict[str, Any]) -> dict[str, Any]:
        normalised: dict[str, Any] = {}
        for csv_key, model_key in self.EXPECTED_COLUMNS.items():
            value = record.get(csv_key)
            if pd.isna(value):
                value = None
            if model_key == "cardmarket_id" and value is not None:
                value = int(value)
            normalised[model_key] = value
        normalised.setdefault("name", "Unknown")
        return normalised
