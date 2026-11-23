
from src.database.vector_store import search_chunks
from src.utils.embeddings import generate_embedding


def semantic_search(query: str, top_k: int = 3):
    """
    Search the vector database and return results with source metadata.
    """

    query_embedding = generate_embedding(query)

    results = search_chunks(
        query_embedding=query_embedding,
        top_k=top_k
    )

    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    ids = results.get("ids", [[]])[0]

    search_results = []

    for rank, (document, distance, metadata, chunk_id) in enumerate(
        zip(documents, distances, metadatas, ids),
        start=1
    ):
        metadata = metadata or {}

        search_results.append({
            "source_id": f"S{rank}",
            "citation": f"[Source {rank}]",
            "text": document,
            "distance": distance,
            "chunk_id": chunk_id,
            "source_url": metadata.get("source", "Unknown source"),
            "chunk_index": metadata.get("chunk_index", -1),
            "metadata": metadata
        })

    return search_results
