import sqlite3
from pathlib import Path
from collections import defaultdict

DB_PATH = Path("data/entities.db")


def normalize(name):
    return " ".join(name.lower().strip().split())


def audit_duplicates():
    print("=" * 65)
    print("DUPLICATE ENTITY AUDIT")
    print("=" * 65)

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT id, name, entity_type, description, source_url
            FROM entities
            ORDER BY name
        """).fetchall()

    groups = defaultdict(list)

    for row in rows:
        key = (normalize(row["name"]), row["entity_type"].upper().strip())
        groups[key].append(dict(row))

    duplicate_groups = [
        records for records in groups.values()
        if len(records) > 1
    ]

    if not duplicate_groups:
        print("\nNo duplicate entities found.")
        return

    total_duplicate_records = 0

    for group_number, records in enumerate(duplicate_groups, start=1):
        print(f"\n--- DUPLICATE GROUP {group_number} ---")

        for record in records:
            print(f"ID          : {record['id']}")
            print(f"Name        : {record['name']}")
            print(f"Type        : {record['entity_type']}")
            print(f"Description : {record['description']}")
            print(f"Source URL  : {record['source_url']}")
            print("-" * 45)

        total_duplicate_records += len(records)

    print("\n" + "=" * 65)
    print(f"Duplicate groups found : {len(duplicate_groups)}")
    print(f"Records in groups      : {total_duplicate_records}")
    print("Database modified      : NO")
    print("Audit completed.")
    print("=" * 65)


if __name__ == "__main__":
    audit_duplicates()