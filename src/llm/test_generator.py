
from src.llm.generator import generate_answer


context = """
Artificial Intelligence is the simulation of human intelligence
by machines.

Machine learning is a subset of Artificial Intelligence.

Deep learning uses neural networks to learn complex patterns.
"""

question = "What is Artificial Intelligence?"

answer = generate_answer(question, context)

print("\n--- AI GENERATED ANSWER ---")
print(answer)
