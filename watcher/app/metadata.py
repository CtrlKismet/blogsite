"""Read leading article metadata without treating body text as configuration."""

import json
import re
from pathlib import Path

from app.publication import parse_publication_time

_FIELD_RE = re.compile(r"^(summary|tags|published_at)\s*[:：]\s*(.*)$", re.IGNORECASE)
_DATE_RE = re.compile(r"^\d{4}[/\-]\d{2}[/\-]\d{2}$")


def split_tags(value: str) -> list[str]:
    return list(dict.fromkeys(tag.strip() for tag in re.split(r"[,，、;；]", value) if tag.strip()))


def parse_metadata(content: str) -> tuple[str, dict]:
    fields: dict = {}
    lines = content.splitlines(keepends=True)
    end = 0
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if _DATE_RE.fullmatch(stripped):
            end = index + 1
            continue
        match = _FIELD_RE.fullmatch(stripped)
        if match is None:
            break
        key, value = match.groups()
        key = key.lower()
        value = value.strip()
        if key == "tags":
            fields[key] = split_tags(value)
        elif key == "published_at":
            fields[key] = parse_publication_time(value).isoformat() if value else None
        else:
            fields[key] = value
        end = index + 1
    return ("".join(lines[end:]).lstrip("\n") if end else content), fields


def load_metadata(path: Path) -> dict:
    if not path.is_file():
        return {}
    fields = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(fields, dict):
        raise ValueError("Article metadata must be a JSON object")
    if "summary" in fields and not isinstance(fields["summary"], str):
        raise ValueError("summary must be a string")
    if "tags" in fields:
        tags = fields["tags"]
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise ValueError("tags must be an array of strings")
        fields["tags"] = list(dict.fromkeys(tag.strip() for tag in tags if tag.strip()))
    value = fields.get("published_at")
    if value is not None:
        if not isinstance(value, str):
            raise ValueError("published_at must be a datetime string or null")
        fields["published_at"] = parse_publication_time(value).isoformat() if value.strip() else None
    return fields
