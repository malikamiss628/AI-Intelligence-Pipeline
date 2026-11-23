from src.search.semantic_search import semantic_search


queries = [
    "What is artificial intelligence?",
    "How do machines learn?",
    "Explain neural networks."
]

for query in queries:
    print("\n" + "=" * 50)
    print("QUERY:", query)
    print("=" * 50)

    results = semantic_search(query, top_k=2)

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Distance:", result["distance"])
        print("Text:", result["text"])