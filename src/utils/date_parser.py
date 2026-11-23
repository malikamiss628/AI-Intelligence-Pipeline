from datetime import datetime, timezone, timedelta
import re



def parse_relative_date(text: str, now: datetime | None = None) -> datetime | None:
    """Parse common relative timestamps like '2 hours ago' into UTC.


    Returns None for unsupported or ambiguous text rather than guessing.
    """
    if not text:
        return None
    now = now or datetime.now(timezone.utc)
    text = text.strip().lower()
    if text in {"just now", "now", "today"}:
        return now
    match = re.fullmatch(r"(\d+)\s+(minute|minutes|min|mins|hour|hours|day|days|week|weeks)\s+ago", text)
    if not match:
        return None
    amount = int(match.group(1))
    unit = match.group(2)
    if unit in {"minute", "minutes", "min", "mins"}:
        delta = timedelta(minutes=amount)
    elif unit in {"hour", "hours"}:
        delta = timedelta(hours=amount)
    elif unit in {"day", "days"}:
        delta = timedelta(days=amount)
    else:
        delta = timedelta(weeks=amount)
    return now - delta


def is_within_last_24_hours(published_at: datetime, now: datetime | None = None) -> bool:
    now = now or datetime.now(timezone.utc)
    if published_at.tzinfo is None:
        published_at = published_at.replace(tzinfo=timezone.utc)
    return now - timedelta(hours=24) <= published_at <= now
