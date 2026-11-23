
from src.entity_resolution.extractor import extract_entities
from src.entity_resolution.entity_store import (
    store_entities,
    get_all_entities,
    search_entities,
    get_entity_count
)

sample_text = """
Artificial Intelligence is a field of computer science.
Geoffrey Hinton is known for his work on neural networks.
Google DeepMind develops AI technologies.
Machine learning is a subset of Artificial Intelligence.
Neural networks are widely used in deep learning.
"""

TEST_SOURCE = "LOCAL_ENTITY_TEST"

# 1. Extract
entities = extract_entities(sample_text)

print(f"\nExtracted {len(entities)} entities.")

# 2. Store
store_entities(
    entities=entities,
    source_url=TEST_SOURCE
)

# 3. Show count
print("\nTotal stored entity records:", get_entity_count())

# 4. Show all
print("\n--- ALL STORED ENTITIES ---")

for entity in get_all_entities():
    print(
        f"{entity['name']} | "
        f"{entity['entity_type']} | "
        f"{entity['source_url']}"
    )

# 5. Test entity search
print("\n--- SEARCH: Neural ---")

matches = search_entities("Neural")

for entity in matches:
    print(entity)
