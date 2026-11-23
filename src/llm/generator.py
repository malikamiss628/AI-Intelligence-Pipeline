
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=API_KEY)


def generate_answer(question: str, context: str) -> str:
    """
    Generate a context-grounded answer with source citations.
    """

    prompt = f"""
Answer the question using ONLY the provided context.

Rules:
- Do not invent facts.
- If the context does not answer the question, say you don't have
  enough information in the provided sources.
- Add citations like [Source 1] after claims using that source.
- Only cite source labels that appear in the context.
- Do not remove or alter source labels.
- Keep the answer clear and concise.

CONTEXT:
{context}

QUESTION:
{question}
"""

    try:
        print("Sending request to Groq...")

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise AI research assistant. Ground every factual claim in the supplied context and cite sources."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_completion_tokens=1024
        )

        answer = response.choices[0].message.content

        if answer:
            return answer.strip()

        return "Groq returned an empty response."

    except Exception as e:
        return f"Groq API Error: {e}"
