def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into word-based chunks with overlap.

    chunk_size: Number of words per chunk
    overlap: Number of overlapping words
    """

    if not text:
        return []

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks