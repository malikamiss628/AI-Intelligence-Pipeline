from src.entity_resolution.type_standardizer import standardize_entity_type

test_entities = [
    ("Artificial general intelligence", "TECHNOLOGY"),
    ("Deep learning", "CONCEPT"),
    ("Machine learning", "CONCEPT"),
    ("Recursive self-improvement", "TECHNOLOGY"),
    ("Superintelligence", "TECHNOLOGY"),
]

print("\n" + "=" * 60)
print("ENTITY TYPE STANDARDIZATION TEST")
print("=" * 60)

for name, old_type in test_entities:
    new_type = standardize_entity_type(name, old_type)

    print(f"\nEntity: {name}")
    print(f"Original Type: {old_type}")
    print(f"Standardized Type: {new_type}")

    if old_type != new_type:
        print("Status: TYPE CORRECTED")
    else:
        print("Status: TYPE RETAINED")

print("\nTest completed.")