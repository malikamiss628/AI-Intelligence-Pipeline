from src.utils.chunking import chunk_text

sample_text = """
Artificial intelligence is the simulation of human intelligence
by machines. Machine learning is a subset of artificial intelligence.
Deep learning uses neural networks to learn complex patterns.
"""

chunks = chunk_text(
    sample_text,
    chunk_size=100,
    overlap=20
)

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- CHUNK {i} ---")
    print(chunk)