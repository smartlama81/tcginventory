"""create cards table

Revision ID: 20250211_01
Revises:
Create Date: 2025-02-11
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20250211_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cards",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("cardmarket_id", sa.Integer(), nullable=True, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("collector_number", sa.String(length=50), nullable=True),
        sa.Column("rarity", sa.String(length=50), nullable=True),
        sa.Column("expansion", sa.String(length=100), nullable=True),
        sa.Column("expansion_code", sa.String(length=20), nullable=True),
        sa.Column("scryfall_id", sa.String(length=64), nullable=True),
        sa.Column("tcgplayer_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_cards_cardmarket_id"), "cards", ["cardmarket_id"], unique=True)
    op.create_index(op.f("ix_cards_collector_number"), "cards", ["collector_number"], unique=False)
    op.create_index(op.f("ix_cards_expansion"), "cards", ["expansion"], unique=False)
    op.create_index(op.f("ix_cards_expansion_code"), "cards", ["expansion_code"], unique=False)
    op.create_index(op.f("ix_cards_name"), "cards", ["name"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_cards_name"), table_name="cards")
    op.drop_index(op.f("ix_cards_expansion_code"), table_name="cards")
    op.drop_index(op.f("ix_cards_expansion"), table_name="cards")
    op.drop_index(op.f("ix_cards_collector_number"), table_name="cards")
    op.drop_index(op.f("ix_cards_cardmarket_id"), table_name="cards")
    op.drop_table("cards")
