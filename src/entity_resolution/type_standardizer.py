import re

from src.entity_resolution.type_rules import (
    ENTITY_TYPE_RULES,
    ENTITY_TYPE_OVERRIDES,
)


def normalize_entity_name(name: str) -> str:
    """Normalize an entity name for consistent matching."""
    if not name:
        return ""

    name = name.lower().strip()
    name = re.sub(r"[^\w\s]", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name


def standardize_entity_type(name: str, current_type: str) -> str:
    """
    Apply known entity type corrections.

    If an override exists, return the standardized type.
    Otherwise, preserve the existing type.
    """

    normalized_name = normalize_entity_name(name)

    # Apply known type overrides
    if normalized_name in ENTITY_TYPE_OVERRIDES:
        return ENTITY_TYPE_OVERRIDES[normalized_name]

    # Preserve existing type if it is valid
    if current_type in ENTITY_TYPE_RULES:
        return current_type

    # If type is unknown, retain it for now
    return current_type