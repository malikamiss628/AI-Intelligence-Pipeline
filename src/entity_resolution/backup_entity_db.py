import sqlite3
from datetime import datetime
from pathlib import Path

# Original database
DB_PATH = Path("data/entities.db")

# Backup directory
BACKUP_DIR = Path("data/backups")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def backup_entity_database():
    if not DB_PATH.exists():
        print("ERROR: Database file not found.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_path = BACKUP_DIR / f"entities_backup_{timestamp}.db"

    # Safely copy SQLite database using SQLite's backup API
    with sqlite3.connect(DB_PATH) as source_conn:
        with sqlite3.connect(backup_path) as backup_conn:
            source_conn.backup(backup_conn)

    # Verify backup
    with sqlite3.connect(backup_path) as conn:
        result = conn.execute(
            "SELECT COUNT(*) FROM entities"
        ).fetchone()

    print("=" * 60)
    print("ENTITY DATABASE BACKUP")
    print("=" * 60)
    print(f"Original database: {DB_PATH}")
    print(f"Backup created: {backup_path}")
    print(f"Records backed up: {result[0]}")
    print("Backup status: SUCCESS")
    print("=" * 60)


if __name__ == "__main__":
    backup_entity_database()