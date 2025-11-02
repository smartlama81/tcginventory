from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.init_db import init_models
from app.db.session import AsyncSessionLocal
from app.services.card_importer import CardImporter


async def _run_import(csv_path: Path) -> None:
    await init_models()
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        importer = CardImporter(session)
        result = await importer.import_file(csv_path)
        print(
            "Imported cards from", csv_path,
            "-> created:", result["created"],
            "updated:", result["updated"],
            "rows:", result["total"],
        )


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Management commands for the TCG inventory backend")
    subparsers = parser.add_subparsers(dest="command")

    import_parser = subparsers.add_parser("import-cards", help="Import master card data from a CSV file")
    import_parser.add_argument("csv_path", type=Path, help="Path to the CSV file")

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    if args.command == "import-cards":
        asyncio.run(_run_import(Path(args.csv_path)))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
