"""Publication timestamps use the site's local wall time, matching existing API dates."""

from datetime import datetime
from zoneinfo import ZoneInfo

from app.config import settings


def local_now() -> datetime:
    return datetime.now(ZoneInfo(settings.timezone)).replace(tzinfo=None)


def parse_publication_time(value: str) -> datetime:
    """Require an explicit clock time; convert offsets to the site's timezone."""
    value = value.strip().replace("/", "-")
    if ":" not in value or not ("T" in value or " " in value):
        raise ValueError("published_at must include a date and time")
    timestamp = datetime.fromisoformat(value)
    if timestamp.tzinfo is not None:
        timestamp = timestamp.astimezone(ZoneInfo(settings.timezone))
    return timestamp.replace(tzinfo=None)
