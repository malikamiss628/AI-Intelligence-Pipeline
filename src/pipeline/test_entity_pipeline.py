
from src.database.vector_store import get_all_chunks
from src.entity_resolution.extractor import extract_entities
from src.entity_resolution.entity_store import store_entities, get_all_entities

print("\n[1] Loading chunks from ChromaDB...")

chunks = get_all_chunks()
print(f"Available chunks: {len(chunks)}")

if not chunks:
    print("No chunks found.")
    raise SystemExit

# Small test batch
test_chunks = chunks[:1]

total_extracted = 0

print("\n[2] Processing chunks individually...")

for index, chunk in enumerate(test_chunks, start=1):

    print(f"\n{'=' * 50}")
    print(f"Processing chunk {index}/{len(test_chunks)}")
    print(f"{'=' * 50}")

    text = chunk["text"][:800]
    source_url = chunk["source_url"]

    print(f"Text length: {len(text)} characters")

    # Extract entities from one chunk only
    entities = extract_entities(text)

    print(f"Entities found: {len(entities)}")

    # Store immediately
    if entities:
        store_entities(
            entities=entities,
            source_url=source_url
        )
        total_extracted += len(entities)

print("\n" + "=" * 50)
print("ENTITY PIPELINE SUMMARY")
print("=" * 50)

print(f"Chunks processed: {len(test_chunks)}")
print(f"Entities extracted this run: {total_extracted}")

all_entities = get_all_entities()

print(f"Total entity records in database: {len(all_entities)}")

print("\n--- RECENT ENTITY PREVIEW ---")

for entity in all_entities[-15:]:
    print(
        f"{entity['name']} | "
        f"{entity['entity_type']} | "
        f"{entity['source_url']}"
    )

print("\nPipeline completed.")
