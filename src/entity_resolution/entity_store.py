
import sqlite3
from pathlib import Path

DB_PATH = Path("data/entities.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def initialize_entity_db():
    """Create the entity database and table if they don't exist."""

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                description TEXT,
                source_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name, entity_type, source_url)
            )
        """)

    print("Entity database initialized.")


def store_entities(entities: list, source_url: str):
    """Store extracted entities and associate them with their source."""

    initialize_entity_db()

    saved_count = 0

    with sqlite3.connect(DB_PATH) as conn:
        for entity in entities:
            conn.execute("""
                INSERT INTO entities
                    (name, entity_type, description, source_url)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(name, entity_type, source_url)
                DO UPDATE SET description = excluded.description
            """, (
                entity.get("name", ""),
                entity.get("type", "UNKNOWN"),
                entity.get("description", ""),
                source_url
            ))

            saved_count += 1

    print(f"Stored/updated {saved_count} entities.")


def get_all_entities():
    """Return all stored entities."""

    initialize_entity_db()

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT * FROM entities
            ORDER BY name
        """).fetchall()

    return [dict(row) for row in rows]


def search_entities(name: str):
    """Search entities by name."""

    initialize_entity_db()

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT * FROM entities
            WHERE name LIKE ?
            ORDER BY name
        """, (f"%{name}%",)).fetchall()

    return [dict(row) for row in rows]


def get_entity_count():
    """Return total number of entity records."""

    initialize_entity_db()

    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute(
            "SELECT COUNT(*) FROM entities"
        ).fetchone()

    return result[0]
