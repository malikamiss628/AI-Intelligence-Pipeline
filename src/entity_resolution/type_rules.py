ENTITY_TYPE_RULES = {
    "PERSON": "Individual people",
    "ORGANIZATION": "Companies, institutions, and groups",
    "TECHNOLOGY": "Technical methods, algorithms, systems, and technical approaches",
    "CONCEPT": "Abstract ideas, theories, principles, and general terms",
    "PRODUCT": "Named software products and services",
    "LOCATION": "Geographic places",
}

# Known entity type corrections
ENTITY_TYPE_OVERRIDES = {
    "artificial general intelligence": "CONCEPT",
    "deep learning": "TECHNOLOGY",
    "machine learning": "TECHNOLOGY",
    "recursive self improvement": "CONCEPT",
    "superintelligence": "CONCEPT",
}