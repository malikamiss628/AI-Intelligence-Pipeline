from src.entity_resolution.entity_store import get_all_entities
from src.entity_resolution.type_standardizer import standardize_entity_type

def generate_correction_preview():
    entities = get_all_entities()

    corrections = []

    for entity in entities:
        name = entity.get("name", "")
        old_type = entity.get("entity_type", "UNKNOWN")

        new_type = standardize_entity_type(name, old_type)

        if old_type != new_type:
            corrections.append({
                "name": name,
                "old_type": old_type,
                "new_type": new_type,
            })

    print("\n" + "=" * 70)
    print("ENTITY TYPE CORRECTION PREVIEW")
    print("=" * 70)

    if not corrections:
        print("No corrections required.")
        return

    for index, item in enumerate(corrections, start=1):
        print(f"\n{index}. Entity: {item['name']}")
        print(f"   Old Type: {item['old_type']}")
        print(f"   New Type: {item['new_type']}")

    print("\n" + "-" * 70)
    print(f"Total records requiring correction: {len(corrections)}")
    print("Preview only — database was NOT modified.")
    print("=" * 70)


if __name__ == "__main__":
    generate_correction_preview()