import sqlite3

from src.entity_resolution.entity_store import DB_PATH

CONFLICT_IDS = [10, 53, 14, 57]


def inspect_conflicts():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        print("=" * 75)
        print("DUPLICATE ENTITY INSPECTION")
        print("=" * 75)

        for entity_id in CONFLICT_IDS:
            row = conn.execute("""
                SELECT id, name, entity_type, description, source_url, created_at
                FROM entities
                WHERE id = ?
            """, (entity_id,)).fetchone()

            if not row:
                print(f"\nID {entity_id}: NOT FOUND")
                continue

            print(f"\nID: {row['id']}")
            print(f"Name: {row['name']}")
            print(f"Type: {row['entity_type']}")
            print(f"Description: {row['description']}")
            print(f"Source URL: {row['source_url']}")
            print(f"Created At: {row['created_at']}")
            print("-" * 75)

    print("\nInspection complete. Database was NOT modified.")


if __name__ == "__main__":
    inspect_conflicts()