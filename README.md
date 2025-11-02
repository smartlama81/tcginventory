# TCG Inventory Platform

Dieses Repository enthält die Grundlagen für ein internes Werkzeug zur Verwaltung eines Pokémon-Karten-Inventars. Der aktuelle Stand liefert einen ersten FastAPI-Backend-Service mit Datenbankanbindung, Migrationen und einem Import-Workflow für die vollständige Kartenliste.

## Struktur

- `backend/` – Python-Projekt (FastAPI + SQLAlchemy + Alembic)
  - `app/` – Anwendungscode
  - `alembic/` – Datenbankmigrationen
- `export-Pokemon-02-11-2025.csv` – Ausgangsdatensatz mit allen Karten (Masterliste)
- `pflichtenheft.docx` – Entwurfs-Pflichtenheft

## Erste Schritte (Backend)

1. Erstelle und aktiviere eine virtuelle Umgebung, installiere die Abhängigkeiten über `pip install -e .[dev]` innerhalb von `backend/`.
2. Lege optional eine `.env` im Ordner `backend/` an (eine Vorlage findest du unter `backend/.env.example`), um Konfigurationen wie die Datenbank-URL (`TCGINV_DATABASE_URL`) zu überschreiben. Standard ist eine lokale SQLite-Datei `data/app.db`.
3. Starte den Server mit:

   ```bash
   uvicorn app.main:app --reload
   ```

   Der Healthcheck ist dann unter `http://localhost:8000/health` erreichbar, die API unter `http://localhost:8000/api/v1/cards`.

## Import der Karten-Stammdaten

Um die große CSV mit der Masterliste in die Datenbank zu importieren:

```bash
cd backend
python -m app.cli import-cards ../export-Pokemon-02-11-2025.csv
```

Der Befehl erstellt bei Bedarf die Tabellen, liest die CSV ein und legt neue Einträge an bzw. aktualisiert bestehende (Matching über `cardmarketId`).

## Datenbankmigrationen

Für Schemaänderungen können Alembic-Migrationen verwendet werden:

```bash
cd backend
alembic upgrade head
```

Neue Migrationen erzeugst du mit `alembic revision --autogenerate -m "Beschreibung"`.

## Tests

Pytest-Tests liegen im Verzeichnis `backend/app/tests` und können mit folgendem Befehl ausgeführt werden:

```bash
cd backend
pytest
```

## Ausblick

Die Backend-Grundlage ist so aufgebaut, dass in weiteren Schritten Authentifizierung, zusätzliche Domänenmodelle (Lots, Sales, Shipments etc.), Frontend und Reporting ergänzt werden können. Der Import-Service wird später erweitert, um weitere Attribute (z. B. Bilder, Sprachvarianten) zu verarbeiten.
