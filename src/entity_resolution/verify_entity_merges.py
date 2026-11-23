import sqlite3

from src.entity_resolution.entity_store import DB_PATH

EXPECTED = {
    53: {
        "name": "Artificial general intelligence",
        "type": "CONCEPT",
        "description_parts": [
            "AI aiming human-level cognitive abilities",
            "AI capable of general tasks",
        ],
    },
    57: {
        "name": "Recursive self-improvement",
        "type": "CONCEPT",
        "description_parts": [
            "Iterative enhancement of its own intelligence",
            "AI improving itself iteratively",
        ],
    },
}

DELETED_IDS = [10, 14]


def verify_merges():
    passed = 0
    failed = 0

    with sqlite3.connect(DB_PATH) as conn:
        print("=" * 70)
        print("INDEPENDENT ENTITY MERGE VERIFICATION")
        print("=" * 70)

        # Verify canonical records and descriptions
        for entity_id, expected in EXPECTED.items():
            row = conn.execute("""
                SELECT name, entity_type, description
                FROM entities
                WHERE id = ?
            """, (entity_id,)).fetchone()

            if row is None:
                print(f"FAIL | Canonical ID {entity_id} missing")
                failed += 1
                continue

            name, entity_type, description = row

            checks = (
                name == expected["name"]
                and entity_type == expected["type"]
                and all(part in (description or "") 
                        for part in expected["description_parts"])
            )

            if checks:
                print(f"PASS | ID {entity_id} | {name}")
                print(f"     Type: {entity_type}")
                print(f"     Description: {description}")
                passed += 1
            else:
                print(f"FAIL | ID {entity_id} | Content mismatch")
                failed += 1

        # Verify duplicate records are deleted
        for entity_id in DELETED_IDS:
            row = conn.execute("""
                SELECT id FROM entities WHERE id = ?
            """, (entity_id,)).fetchone()

            if row is None:
                print(f"PASS | Duplicate ID {entity_id} removed")
                passed += 1
            else:
                print(f"FAIL | Duplicate ID {entity_id} still exists")
                failed += 1

        # Verify total count
        total = conn.execute(
            "SELECT COUNT(*) FROM entities"
        ).fetchone()[0]

    print("-" * 70)
    print(f"Total records remaining: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("RESULT: ALL MERGES VERIFIED")
    else:
        print("RESULT: VERIFICATION FAILED")

    print("=" * 70)


if __name__ == "__main__":
    verify_merges()