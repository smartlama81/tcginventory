from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models import Card
from app.schemas.card import CardRead

router = APIRouter()


def apply_filters(stmt, name: str | None, expansion: str | None, collector_number: str | None):
    if name:
        stmt = stmt.where(Card.name.ilike(f"%{name}%"))
    if expansion:
        stmt = stmt.where(Card.expansion.ilike(f"%{expansion}%"))
    if collector_number:
        stmt = stmt.where(Card.collector_number == collector_number)
    return stmt


@router.get("/", response_model=list[CardRead])
async def list_cards(
    *,
    session: AsyncSession = Depends(get_session),
    name: str | None = Query(None, description="Filter by partial card name"),
    expansion: str | None = Query(None, description="Filter by partial expansion name"),
    collector_number: str | None = Query(None, description="Filter by collector number"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> Sequence[CardRead]:
    stmt = select(Card).order_by(Card.name).offset(offset).limit(limit)
    stmt = apply_filters(stmt, name, expansion, collector_number)
    result = await session.scalars(stmt)
    return [CardRead.model_validate(card) for card in result]


@router.get("/{card_id}", response_model=CardRead)
async def get_card(card_id: int, session: AsyncSession = Depends(get_session)) -> CardRead:
    card = await session.get(Card, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return CardRead.model_validate(card)
