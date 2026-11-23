import sqlite3

from src.entity_resolution.entity_store import DB_PATH

SAFE_CORRECTIONS = [
    (7, "CONCEPT", "TECHNOLOGY"),
    (8, "CONCEPT", "TECHNOLOGY"),
    (11, "TECHNOLOGY", "CONCEPT"),
]


def apply_safe_corrections():
    conn = sqlite3.connect(DB_PATH)

    try:
        # Start a protected transaction
        conn.execute("BEGIN IMMEDIATE")

        print("=" * 65)
        print("APPLYING ENTITY TYPE CORRECTIONS")
        print("=" * 65)

        for entity_id, old_type, new_type in SAFE_CORRECTIONS:

            row = conn.execute("""
                SELECT id, name, entity_type, source_url
                FROM entities
                WHERE id = ?
            """, (entity_id,)).fetchone()

            if row is None:
                raise RuntimeError(
                    f"Entity ID {entity_id} not found. Aborting."
                )

            record_id, name, current_type, source_url = row

            # Ensure record has the expected original type
            if current_type != old_type:
                raise RuntimeError(
                    f"Unexpected type for ID {entity_id}: "
                    f"{current_type}. Expected {old_type}."
                )

            # Check for uniqueness conflict
            conflict = conn.execute("""
                SELECT id
                FROM entities
                WHERE name = ?
                  AND entity_type = ?
                  AND source_url IS ?
                  AND id != ?
            """, (
                name,
                new_type,
                source_url,
                entity_id
            )).fetchone()

            if conflict:
                raise RuntimeError(
                    f"Conflict detected for ID {entity_id}. "
                    f"Existing target ID: {conflict[0]}. Aborting."
                )

            # Apply correction
            conn.execute("""
                UPDATE entities
                SET entity_type = ?
                WHERE id = ?
                  AND entity_type = ?
            """, (
                new_type,
                entity_id,
                old_type
            ))

            print(
                f"UPDATED ID {record_id}: {name} | "
                f"{old_type} -> {new_type}"
            )

        # Verify changes before commit
        print("\n--- VERIFYING UPDATES ---")

        for entity_id, old_type, new_type in SAFE_CORRECTIONS:
            result = conn.execute("""
                SELECT name, entity_type
                FROM entities
                WHERE id = ?
            """, (entity_id,)).fetchone()

            if result is None or result[1] != new_type:
                raise RuntimeError(
                    f"Verification failed for ID {entity_id}. "
                    "Rolling back."
                )

            print(
                f"VERIFIED ID {entity_id}: "
                f"{result[0]} | {result[1]}"
            )

        # Commit only if every update and verification succeeded
        conn.commit()

        print("\n" + "=" * 65)
        print("SUCCESS: All 3 corrections committed.")
        print("Transaction completed successfully.")
        print("=" * 65)

    except Exception as error:
        conn.rollback()

        print("\n" + "=" * 65)
        print("UPDATE FAILED — TRANSACTION ROLLED BACK")
        print(f"Reason: {error}")
        print("Database changes were reverted.")
        print("=" * 65)

    finally:
        conn.close()


if __name__ == "__main__":
    apply_safe_corrections()