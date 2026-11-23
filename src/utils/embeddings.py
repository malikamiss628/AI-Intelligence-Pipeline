from sentence_transformers import SentenceTransformer


# Load embedding model
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str):
    """
    Generate embedding for a single text.
    """
    embedding = model.encode(text)

    return embedding.tolist()


def generate_embeddings(text_chunks: list[str]):
    """
    Generate embeddings for multiple text chunks.
    """
    embeddings = model.encode(
        text_chunks,
        show_progress_bar=True
    )

    return embeddings.tolist()