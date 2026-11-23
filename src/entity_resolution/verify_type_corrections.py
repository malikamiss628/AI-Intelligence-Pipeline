import sqlite3

from src.entity_resolution.entity_store import DB_PATH

EXPECTED_RECORDS = {
    7: ("Machine learning", "TECHNOLOGY"),
    8: ("deep learning", "TECHNOLOGY"),
    11: ("superintelligence", "CONCEPT"),
}


def verify_corrections():
    print("=" * 65)
    print("INDEPENDENT DATABASE VERIFICATION")
    print("=" * 65)

    passed = 0
    failed = 0

    with sqlite3.connect(DB_PATH) as conn:
        for entity_id, expected in EXPECTED_RECORDS.items():

            row = conn.execute("""
                SELECT name, entity_type
                FROM entities
                WHERE id = ?
            """, (entity_id,)).fetchone()

            if row is None:
                print(f"FAIL | ID {entity_id} | Record missing")
                failed += 1
                continue

            actual_name, actual_type = row
            expected_name, expected_type = expected

            if actual_name == expected_name and actual_type == expected_type:
                print(
                    f"PASS | ID {entity_id} | "
                    f"{actual_name} | {actual_type}"
                )
                passed += 1
            else:
                print(
                    f"FAIL | ID {entity_id} | "
                    f"Expected {expected} | Got {row}"
                )
                failed += 1

    print("-" * 65)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("RESULT: ALL CORRECTIONS VERIFIED")
    else:
        print("RESULT: VERIFICATION FAILED")

    print("=" * 65)


if __name__ == "__main__":
    verify_corrections()