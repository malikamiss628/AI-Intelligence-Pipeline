
import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=API_KEY)


# Generic terms that should not be stored as entities
GENERIC_TERMS = {
    "art", "music", "audio", "images", "projects",
    "approaches", "applications", "industry", "government",
    "finance", "physics", "philosophy", "military",
    "translation", "open source", "open-source",
    "systems integration", "symbolic", "computer",
    "software", "data", "information", "research",
    "methods", "techniques", "problems", "solutions"
}


ALLOWED_TYPES = {
    "PERSON",
    "ORGANIZATION",
    "LOCATION",
    "DATE",
    "EVENT",
    "TECHNOLOGY",
    "CONCEPT"
}


def normalize_name(name: str) -> str:
    """Normalize entity name for duplicate detection."""
    name = name.lower().strip()
    name = re.sub(r"\s+", " ", name)
    name = re.sub(r"[^\w\s-]", "", name)
    return name


def is_valid_entity(name: str, entity_type: str, description: str) -> bool:
    """Filter generic, invalid, and low-quality entities."""

    normalized = normalize_name(name)

    if not normalized or len(normalized) < 3:
        return False

    if entity_type not in ALLOWED_TYPES:
        return False

    if normalized in GENERIC_TERMS:
        return False

    if len(name.split()) > 8:
        return False

    if not description:
        return False

    return True


def extract_entities(text: str) -> list:
    """Extract meaningful entities from text using Groq."""

    if not text or not text.strip():
        return []

    # Prompt stays INSIDE the function
    prompt = f"""
Extract up to 10 important named entities from the text.

Allowed types:
PERSON, ORGANIZATION, LOCATION, DATE, EVENT, TECHNOLOGY, CONCEPT

Rules:
- Only extract entities explicitly mentioned.
- Focus on specific and meaningful entities.
- Ignore generic words like art, music, projects, applications.
- Do not invent information.
- Descriptions must be maximum 8 words.
- Do not repeat entities.
- Return an empty entities array if nothing meaningful is found.

Return JSON only:
{{
  "entities": [
    {{
      "name": "Entity name",
      "type": "CONCEPT",
      "description": "Short description"
    }}
  ]
}}

TEXT:
{text[:500]}
"""

    try:
        print("Extracting entities with Groq...")

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise named-entity extraction engine. "
                        "Return only valid JSON and avoid generic entities."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            max_completion_tokens=2048
        )

        raw_output = response.choices[0].message.content

        if not raw_output:
            print("Empty response from Groq.")
            print("Finish reason:", response.choices[0].finish_reason)
            return []

        raw_output = raw_output.strip()

        # Remove markdown code fences
        raw_output = re.sub(r"^```(?:json)?\s*", "", raw_output)
        raw_output = re.sub(r"\s*```$", "", raw_output)

        # Locate JSON object
        start = raw_output.find("{")
        end = raw_output.rfind("}")

        if start == -1 or end == -1:
            print("No JSON object found.")
            return []

        data = json.loads(raw_output[start:end + 1])
        entities = data.get("entities", [])

        valid_entities = []
        seen = set()

        for entity in entities:

            if not isinstance(entity, dict):
                continue

            name = str(entity.get("name", "")).strip()
            entity_type = str(entity.get("type", "")).upper().strip()
            description = str(entity.get("description", "")).strip()

            normalized = normalize_name(name)

            # Deduplicate across types
            if normalized in seen:
                continue

            if is_valid_entity(name, entity_type, description):
                seen.add(normalized)

                valid_entities.append({
                    "name": name,
                    "type": entity_type,
                    "description": description
                })

        print(f"Entities extracted: {len(valid_entities)}")
        return valid_entities

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return []

    except Exception as e:
        print(f"Entity extraction error: {e}")
        return []
