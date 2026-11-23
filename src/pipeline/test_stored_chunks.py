from src.database.vector_store import get_all_chunks

chunks = get_all_chunks()

print(f"\nTotal retrieved chunks: {len(chunks)}")

if chunks:
    first = chunks[0]

    print("\n--- FIRST CHUNK ---")
    print("Chunk ID:", first["chunk_id"])
    print("Source:", first["source_url"])
    print("\nText preview:")
    print(first["text"][:500])