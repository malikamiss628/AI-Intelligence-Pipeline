from src.entity_resolution.resolver import resolve_name
from src.utils.date_parser import parse_relative_date, is_within_last_24_hours
from datetime import datetime, timezone



if __name__ == "__main__":
    print("AI Intelligence Pipeline — Phase 1 setup check")
    for name in ["Open AI", "OpenAI Inc.", "Anthropic", "Unknown AI Labs"]:
        print(f"{name} => {resolve_name(name)}")
    parsed = parse_relative_date("2 hours ago")
    print("Parsed relative date:", parsed)
    if parsed:
        print("Fresh (24h):", is_within_last_24_hours(parsed, datetime.now(timezone.utc)))
