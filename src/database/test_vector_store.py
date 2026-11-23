from src.database.vector_store import store_chunks, search_chunks, get_collection_count
from src.utils.embeddings import generate_embeddings

# Sample text chunks
chunks = [
    "Artificial Intelligence is the simulation of human intelligence by machines.",
    "Machine Learning is a subset of Artificial Intelligence.",
    "Deep Learning uses neural networks to learn complex patterns."
]

# Generate embeddings
embeddings = generate_embeddings(chunks)

# Store embeddings
store_chunks(
    chunks=chunks,
    embeddings=embeddings,
    source_url="https://example.com"
)

# Test search
query = "What is machine learning?"

query_embedding = generate_embeddings([query])[0]

results = search_chunks(query_embedding, top_k=2)

print("\n--- SEARCH RESULTS ---")

for document, distance in zip(
    results["documents"][0],
    results["distances"][0]
):
    print(f"\nDistance: {distance}")
    print(f"Text: {document}")

print("\nTotal stored chunks:", get_collection_count())