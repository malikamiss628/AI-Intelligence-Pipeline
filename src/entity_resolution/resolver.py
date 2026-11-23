
import re
from difflib import SequenceMatcher


def normalize_entity_name(name: str) -> str:
    """Normalize entity names for comparison."""

    if not name:
        return ""

    name = name.lower().strip()
    name = re.sub(r"[^\w\s]", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name


def normalize_words(name: str) -> list:
    """Normalize words and handle basic plural variations."""

    normalized = normalize_entity_name(name)
    words = normalized.split()

    cleaned_words = []

    for word in words:
        # Basic plural normalization
        if len(word) > 4 and word.endswith("ies"):
            word = word[:-3] + "y"
        elif len(word) > 4 and word.endswith("s"):
            word = word[:-1]

        cleaned_words.append(word)

    return cleaned_words


def similarity_score(name1: str, name2: str) -> float:
    """Calculate improved similarity using multiple comparison methods."""

    n1 = normalize_entity_name(name1)
    n2 = normalize_entity_name(name2)

    if not n1 or not n2:
        return 0.0

    # 1. Standard character similarity
    char_score = SequenceMatcher(None, n1, n2).ratio()

    # 2. Ignore spaces to handle Open AI vs OpenAI
    compact1 = n1.replace(" ", "")
    compact2 = n2.replace(" ", "")

    compact_score = SequenceMatcher(
        None, compact1, compact2
    ).ratio()

    # 3. Word similarity with basic plural normalization
    words1 = set(normalize_words(name1))
    words2 = set(normalize_words(name2))

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    word_score = len(intersection) / len(union) if union else 0.0

    # Combined score
    combined_score = max(
        char_score,
        compact_score,
        (char_score * 0.4) + (word_score * 0.6)
    )

    return round(combined_score, 4)


def find_duplicate_candidates(
    entities: list,
    threshold: float = 0.88
) -> list:
    """Find possible duplicates without automatically merging."""

    candidates = []

    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):

            entity1 = entities[i]
            entity2 = entities[j]

            type1 = str(
                entity1.get("entity_type", "")
            ).upper().strip()

            type2 = str(
                entity2.get("entity_type", "")
            ).upper().strip()

            # Same entity type only
            if not type1 or type1 != type2:
                continue

            name1 = entity1.get("name", "")
            name2 = entity2.get("name", "")

            if not name1 or not name2:
                continue

            score = similarity_score(name1, name2)

            if score >= threshold:
                candidates.append({
                    "entity_1": name1,
                    "entity_2": name2,
                    "type": type1,
                    "similarity": score,
                    "status": "REVIEW_REQUIRED"
                })

    candidates.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return candidates


def resolve_name(name: str) -> str:
    """Resolve common entity name variations to a canonical name."""

    if not name:
        return ""

    normalized = normalize_entity_name(name)

    aliases = {
        "open ai": "OpenAI",
        "openai inc": "OpenAI",
        "openai": "OpenAI",
        "anthropic": "Anthropic",
    }

    return aliases.get(normalized, name.strip())