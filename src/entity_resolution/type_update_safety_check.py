import sqlite3

from src.entity_resolution.entity_store import DB_PATH
from src.entity_resolution.type_standardizer import (
    standardize_entity_type,
    normalize_entity_name,
)


def check_update_conflicts():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        entities = conn.execute(
            "SELECT * FROM entities ORDER BY name"
        ).fetchall()

        conflicts = []
        corrections = []

        for entity in entities:
            name = entity["name"]
            old_type = entity["entity_type"]
            new_type = standardize_entity_type(name, old_type)

            if old_type == new_type:
                continue

            # Check whether the target record already exists
            existing = conn.execute("""
                SELECT id
                FROM entities
                WHERE name = ?
                  AND entity_type = ?
                  AND source_url IS ?
                  AND id != ?
            """, (
                name,
                new_type,
                entity["source_url"],
                entity["id"]
            )).fetchone()

            correction = {
                "id": entity["id"],
                "name": name,
                "old_type": old_type,
                "new_type": new_type,
                "source_url": entity["source_url"],
            }

            if existing:
                correction["conflict_with_id"] = existing["id"]
                conflicts.append(correction)
            else:
                corrections.append(correction)

    print("\n" + "=" * 70)
    print("ENTITY TYPE UPDATE SAFETY CHECK")
    print("=" * 70)

    print(f"\nSafe corrections: {len(corrections)}")
    print(f"Potential conflicts: {len(conflicts)}")

    if corrections:
        print("\n--- SAFE TO UPDATE ---")
        for item in corrections:
            print(
                f"ID {item['id']}: {item['name']} | "
                f"{item['old_type']} -> {item['new_type']}"
            )

    if conflicts:
        print("\n--- CONFLICTS — DO NOT UPDATE AUTOMATICALLY ---")
        for item in conflicts:
            print(
                f"ID {item['id']}: {item['name']} | "
                f"{item['old_type']} -> {item['new_type']} | "
                f"Existing target ID: {item['conflict_with_id']}"
            )

    print("\nDatabase was NOT modified.")
    print("=" * 70)


if __name__ == "__main__":
    check_update_conflicts()