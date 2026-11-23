from src.utils.embeddings import generate_embedding, generate_embeddings


def main():
    text = "Artificial intelligence enables machines to learn."

    # Single embedding
    embedding = generate_embedding(text)

    print("\n--- SINGLE EMBEDDING ---")
    print("Vector dimensions:", len(embedding))
    print("First 10 values:", embedding[:10])

    # Multiple embeddings
    chunks = [
        "Artificial intelligence enables machines to learn.",
        "Machine learning is a subset of artificial intelligence.",
        "Python is a programming language."
    ]

    results = generate_embeddings(chunks)

    print("\n--- MULTIPLE EMBEDDINGS ---")
    print("Number of embeddings:", len(results))
    print("Dimensions per embedding:", len(results[0]))


if __name__ == "__main__":
    main()