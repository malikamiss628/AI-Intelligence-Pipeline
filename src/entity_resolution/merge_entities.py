import sqlite3

from src.entity_resolution.entity_store import DB_PATH

MERGE_PAIRS = [
    {
        "keep_id": 53,
        "delete_id": 10,
        "expected_name": "Artificial general intelligence",
        "expected_type": "CONCEPT",
    },
    {
        "keep_id": 57,
        "delete_id": 14,
        "expected_name": "Recursive self-improvement",
        "expected_type": "CONCEPT",
    },
]


def combine_descriptions(desc1, desc2):
    descriptions = []

    for description in (desc1, desc2):
        if description and description.strip():
            cleaned = description.strip()

            if cleaned not in descriptions:
                descriptions.append(cleaned)

    return " | ".join(descriptions)


def merge_entities():
    conn = sqlite3.connect(DB_PATH)

    try:
        conn.execute("BEGIN IMMEDIATE")

        print("=" * 70)
        print("ENTITY MERGE PROCESS")
        print("=" * 70)

        for pair in MERGE_PAIRS:
            keep_id = pair["keep_id"]
            delete_id = pair["delete_id"]
            expected_name = pair["expected_name"]
            expected_type = pair["expected_type"]

            keep = conn.execute("""
                SELECT id, name, entity_type, description, source_url
                FROM entities
                WHERE id = ?
            """, (keep_id,)).fetchone()

            duplicate = conn.execute("""
                SELECT id, name, entity_type, description, source_url
                FROM entities
                WHERE id = ?
            """, (delete_id,)).fetchone()

            # Validate both records exist
            if keep is None or duplicate is None:
                raise RuntimeError(
                    f"Missing record in merge pair "
                    f"{keep_id}/{delete_id}"
                )

            # Validate names
            if keep[1].lower().strip() != expected_name.lower().strip():
                raise RuntimeError(
                    f"Unexpected canonical entity name for ID {keep_id}"
                )

            if duplicate[1].lower().strip() != expected_name.lower().strip():
                raise RuntimeError(
                    f"Duplicate name mismatch for ID {delete_id}"
                )

            # Validate canonical type
            if keep[2] != expected_type:
                raise RuntimeError(
                    f"Canonical type incorrect for ID {keep_id}: {keep[2]}"
                )

            # Verify both records refer to the same source
            if keep[4] != duplicate[4]:
                raise RuntimeError(
                    f"Source URL mismatch for IDs "
                    f"{keep_id}/{delete_id}. Merge cancelled."
                )

            # Combine descriptions without losing either
            merged_description = combine_descriptions(
                keep[3],
                duplicate[3]
            )

            # Update canonical record
            conn.execute("""
                UPDATE entities
                SET description = ?
                WHERE id = ?
            """, (merged_description, keep_id))

            # Delete redundant record after description is merged
            conn.execute("""
                DELETE FROM entities
                WHERE id = ?
            """, (delete_id,))

            print(f"\nMERGED: {expected_name}")
            print(f"Kept ID: {keep_id}")
            print(f"Removed duplicate ID: {delete_id}")
            print(f"Combined description: {merged_description}")

        # Verify canonical records
        print("\n--- FINAL VERIFICATION ---")

        for pair in MERGE_PAIRS:
            keep_id = pair["keep_id"]
            delete_id = pair["delete_id"]

            canonical = conn.execute("""
                SELECT name, entity_type, description
                FROM entities
                WHERE id = ?
            """, (keep_id,)).fetchone()

            duplicate = conn.execute("""
                SELECT id
                FROM entities
                WHERE id = ?
            """, (delete_id,)).fetchone()

            if canonical is None:
                raise RuntimeError(f"Canonical ID {keep_id} missing!")

            if duplicate is not None:
                raise RuntimeError(
                    f"Duplicate ID {delete_id} still exists!"
                )

            print(
                f"VERIFIED: ID {keep_id} | "
                f"{canonical[0]} | {canonical[1]}"
            )

        conn.commit()

        print("\n" + "=" * 70)
        print("SUCCESS: ENTITY MERGES COMPLETED")
        print("All merges verified and committed.")
        print("=" * 70)

    except Exception as error:
        conn.rollback()

        print("\n" + "=" * 70)
        print("MERGE FAILED — TRANSACTION ROLLED BACK")
        print(f"Reason: {error}")
        print("No partial merge was committed.")
        print("=" * 70)

    finally:
        conn.close()


if __name__ == "__main__":
    merge_entities()