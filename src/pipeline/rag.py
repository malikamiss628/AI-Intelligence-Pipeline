
from src.search.semantic_search import semantic_search
from src.llm.generator import generate_answer


def answer_question(question: str, top_k: int = 3):
    """
    RAG pipeline with source tracking and citations.
    """

    print("\nSearching knowledge base...")

    search_results = semantic_search(
        query=question,
        top_k=top_k
    )

    if not search_results:
        return {
            "question": question,
            "answer": "No relevant information found in the knowledge base.",
            "sources": []
        }

    context_parts = []

    for result in search_results:
        context_parts.append(
            f"""
{result['citation']}
URL: {result['source_url']}
Chunk Index: {result['chunk_index']}

Evidence:
{result['text']}
"""
        )

    context = "\n".join(context_parts)

    print(f"Retrieved {len(search_results)} chunks.")
    print("Generating answer with Groq...")

    answer = generate_answer(
        question=question,
        context=context
    )

    return {
        "question": question,
        "answer": answer,
        "sources": search_results
    }
