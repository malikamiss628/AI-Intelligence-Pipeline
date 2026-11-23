import sqlite3

from src.entity_resolution.entity_store import DB_PATH

MERGE_PAIRS = [
    {"keep_id": 53, "duplicate_id": 10},
    {"keep_id": 57, "duplicate_id": 14},
]


def preview_merges():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        print("=" * 75)
        print("ENTITY MERGE PREVIEW")
        print("=" * 75)

        for pair in MERGE_PAIRS:
            keep_id = pair["keep_id"]
            duplicate_id = pair["duplicate_id"]

            keep = conn.execute(
                "SELECT * FROM entities WHERE id = ?",
                (keep_id,)
            ).fetchone()

            duplicate = conn.execute(
                "SELECT * FROM entities WHERE id = ?",
                (duplicate_id,)
            ).fetchone()

            if not keep or not duplicate:
                print(f"\nERROR: Missing record for pair {keep_id}/{duplicate_id}")
                continue

            print(f"\nKEEP ID: {keep['id']}")
            print(f"Name: {keep['name']}")
            print(f"Type: {keep['entity_type']}")
            print(f"Description: {keep['description']}")

            print(f"\nMERGE FROM ID: {duplicate['id']}")
            print(f"Name: {duplicate['name']}")
            print(f"Type: {duplicate['entity_type']}")
            print(f"Description: {duplicate['description']}")

            print("\nPlanned action:")
            print("- Combine both descriptions")
            print("- Keep the correct CONCEPT record")
            print("- Preserve source URL")
            print("- Delete duplicate only after successful merge")
            print("- Keep everything inside one transaction")

            print("-" * 75)

    print("\nPreview complete. Database was NOT modified.")


if __name__ == "__main__":
    preview_merges()