
from src.entity_resolution.extractor import extract_entities


sample_text = """
Artificial Intelligence is a field of computer science.
Geoffrey Hinton is known for his work on neural networks.
Google DeepMind developed many AI technologies.
Machine learning is a subset of Artificial Intelligence.
Neural networks are widely used in deep learning.
"""


entities = extract_entities(sample_text)

print("\n" + "=" * 50)
print("EXTRACTED ENTITIES")
print("=" * 50)

for entity in entities:
    print(f"\nName: {entity['name']}")
    print(f"Type: {entity['type']}")
    print(f"Description: {entity['description']}")
