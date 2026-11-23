
from src.entity_resolution.entity_store import get_all_entities
from src.entity_resolution.resolver import (
    find_duplicate_candidates,
    similarity_score,
    normalize_entity_name
)


# ==========================================
# TEST 1: CONTROLLED SIMILARITY TEST
# ==========================================

test_pairs = [
    ("Superintelligence", "superintelligence"),
    ("Open AI", "OpenAI"),
    ("Neural Networks", "Neural Network"),
    ("Machine Learning", "Deep Learning"),
    ("Python", "Java"),
]

print("\n" + "=" * 60)
print("CONTROLLED ENTITY SIMILARITY TEST")
print("=" * 60)

for name1, name2 in test_pairs:
    score = similarity_score(name1, name2)
    print(f"\n{name1} <-> {name2}")
    print(f"Similarity Score: {score}")


# ==========================================
# TEST 2: LOAD DATABASE
# ==========================================

entities = get_all_entities()

print(f"\nLoaded {len(entities)} entity records.")


# ==========================================
# TEST 3: SAME-TYPE DUPLICATE DETECTION
# ==========================================

candidates = find_duplicate_candidates(
    entities,
    threshold=0.88
)

print("\n" + "=" * 60)
print("SAME-TYPE DUPLICATE CANDIDATES")
print("=" * 60)

if not candidates:
    print("No duplicate candidates found.")
else:
    for candidate in candidates:
        print(f"\nEntity 1: {candidate['entity_1']}")
        print(f"Entity 2: {candidate['entity_2']}")
        print(f"Type: {candidate['type']}")
        print(f"Similarity: {candidate['similarity']}")
        print(f"Status: {candidate['status']}")


# ==========================================
# TEST 4: CROSS-TYPE ENTITY AUDIT
# ==========================================

print("\n" + "=" * 60)
print("CROSS-TYPE ENTITY AUDIT")
print("=" * 60)

groups = {}

for entity in entities:
    name = entity.get("name", "")
    entity_type = entity.get("entity_type", "UNKNOWN")

    normalized = normalize_entity_name(name)

    if not normalized:
        continue

    if normalized not in groups:
        groups[normalized] = []

    groups[normalized].append({
        "name": name,
        "type": entity_type
    })


cross_type_found = False

for normalized_name, records in groups.items():

    types = set(record["type"] for record in records)

    if len(types) > 1:
        cross_type_found = True

        print(f"\nEntity Name: {normalized_name}")
        print("Conflicting types:")

        for record in records:
            print(f"  - {record['name']} | {record['type']}")

if not cross_type_found:
    print("No cross-type conflicts found.")

print("\nAudit completed. Database was not modified.")
