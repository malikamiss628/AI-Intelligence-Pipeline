import chromadb
from pathlib import Path

# Persistent local database directory
DB_PATH = Path("data/vector_db")

# Initialize ChromaDB
client = chromadb.PersistentClient(path=str(DB_PATH))

# Create or load collection
collection = client.get_or_create_collection(
    name="ai_intelligence_pipeline"
)


def store_chunks(chunks, embeddings, source_url):
    """
    Store text chunks and their embeddings in ChromaDB.
    """

    documents = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        documents.append(chunk)

        metadatas.append({
            "source": source_url,
            "chunk_index": i
        })

        ids.append(f"{source_url}_{i}")

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist() if hasattr(embeddings, "tolist") else embeddings,
        metadatas=metadatas
    )

    print(f"Successfully stored {len(chunks)} chunks!")


def search_chunks(query_embedding, top_k=3):
    """
    Search the vector database using an embedding.
    """

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
            if hasattr(query_embedding, "tolist")
            else query_embedding
        ],
        n_results=top_k
    )

    return results


def get_collection_count():
    return collection.count()

def list_stored_sources():
    data = collection.get(include=["metadatas"])

    sources = {}

    for metadata in data.get("metadatas", []):
        url = metadata.get("source", "Unknown")
        sources[url] = sources.get(url, 0) + 1

    print("\n--- STORED SOURCES ---")
    for url, count in sources.items():
        print(f"{url} | {count} chunks")

    print(f"\nTotal chunks: {collection.count()}")
    
    
def delete_source(source_url: str):
    """
    Delete records belonging to one exact source URL only.
    """

    matching_records = collection.get(
        where={"source": source_url},
        include=["metadatas"]
    )

    ids_to_delete = matching_records.get("ids", [])

    if not ids_to_delete:
        print(f"No records found for: {source_url}")
        return 0

    print(f"Found {len(ids_to_delete)} chunks for:")
    print(source_url)

    collection.delete(ids=ids_to_delete)

    print(f"Deleted {len(ids_to_delete)} chunks.")
    return len(ids_to_delete)

def get_all_chunks():
    """
    Retrieve all stored documents with their IDs and metadata.
    """

    data = collection.get(
        include=["documents", "metadatas"]
    )

    documents = data.get("documents", [])
    metadatas = data.get("metadatas", [])
    ids = data.get("ids", [])

    chunks = []

    for chunk_id, document, metadata in zip(ids, documents, metadatas):
        chunks.append({
            "chunk_id": chunk_id,
            "text": document,
            "metadata": metadata or {},
            "source_url": (metadata or {}).get("source", "Unknown")
        })

    return chunks