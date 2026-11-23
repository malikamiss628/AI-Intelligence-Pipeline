
from src.pipeline.rag import answer_question


def main():
    question = input("\nAsk your question: ")

    result = answer_question(
        question=question,
        top_k=3
    )

    print("\n" + "=" * 65)
    print("QUESTION")
    print("=" * 65)
    print(result["question"])

    print("\n" + "=" * 65)
    print("AI ANSWER")
    print("=" * 65)
    print(result["answer"])

    print("\n" + "=" * 65)
    print("SOURCE TRACKING")
    print("=" * 65)

    for source in result["sources"]:
        print(f"\n{source['citation']}")
        print("-" * 50)
        print(f"URL         : {source['source_url']}")
        print(f"Chunk ID    : {source['chunk_id']}")
        print(f"Chunk Index : {source['chunk_index']}")
        print(f"Distance    : {source['distance']:.4f}")
        print("Evidence:")
        print(source["text"][:500])


if __name__ == "__main__":
    main()
