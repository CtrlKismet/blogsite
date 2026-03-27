"""Intake: pick up loose markdown files and organize into article directories."""

import json
import logging
import re
from datetime import UTC, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Date pattern at the start of file content: YYYY/MM/DD or YYYY-MM-DD
_DATE_RE = re.compile(r"^(\d{4})[/\-](\d{2})[/\-](\d{2})\s*$")

# Metadata patterns (support both : and ：)
_SUMMARY_RE = re.compile(r"^summary\s*[:：]\s*(.+)$", re.IGNORECASE)
_TAG_RE = re.compile(r"^tags?\s*[:：]\s*(.+)$", re.IGNORECASE)

# Characters to strip from title for directory naming
_STRIP_CHARS = str.maketrans("", "", "『』「」《》【】")


def _clean_title(title: str) -> str:
    """Clean title for use in directory name."""
    return title.translate(_STRIP_CHARS).strip()


def _parse_date_from_content(text: str) -> datetime | None:
    """Try to parse a date from the first non-empty line of content."""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = _DATE_RE.match(line)
        if m:
            try:
                return datetime(
                    int(m.group(1)), int(m.group(2)), int(m.group(3)),
                    tzinfo=UTC,
                )
            except ValueError:
                pass
        break  # only check first non-empty line
    return None


def _remove_date_line(text: str) -> str:
    """Remove the date line from the beginning of content."""
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if _DATE_RE.match(stripped):
            return "".join(lines[i + 1:]).lstrip("\n")
        break
    return text


def _parse_and_strip_metadata(text: str) -> tuple[str, str | None, list[str] | None]:
    """Parse and strip metadata header (date, summary, tags) from content.

    Returns (cleaned_content, summary_or_None, tags_or_None).
    """
    lines = text.splitlines(keepends=True)
    summary = None
    tags = None
    meta_end = 0  # index of first non-metadata line

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        if _DATE_RE.match(stripped):
            meta_end = i + 1
            continue

        m = _SUMMARY_RE.match(stripped)
        if m:
            summary = m.group(1).strip()
            meta_end = i + 1
            continue

        m = _TAG_RE.match(stripped)
        if m:
            raw_tags = m.group(1).strip()
            tags = [t.strip() for t in re.split(r"[,，、;；]", raw_tags) if t.strip()]
            meta_end = i + 1
            continue

        break  # first non-metadata line

    cleaned = "".join(lines[meta_end:]).lstrip("\n")
    return cleaned, summary, tags


def intake_loose_files(posts_dir: Path) -> list[str]:
    """Find loose .md files in posts_dir root and organize them.

    Returns list of created dir_names for further processing.
    """
    created_dirs: list[str] = []

    for f in sorted(posts_dir.iterdir()):
        if not f.is_file() or f.suffix.lower() != ".md":
            continue

        # This is a loose markdown file in the root
        title = _clean_title(f.stem)
        if not title:
            logger.warning("Skipping file with empty title: %s", f.name)
            continue

        content = f.read_text(encoding="utf-8")
        dt = _parse_date_from_content(content)
        if dt is None:
            dt = datetime.now(UTC)
            logger.info("No date found in %s, using today", f.name)

        # Build directory name: YY-MM-DD-title
        dir_name = f"{dt.strftime('%y-%m-%d')}-{title}"
        article_dir = posts_dir / dir_name

        if article_dir.exists():
            logger.warning("Directory already exists: %s, skipping", dir_name)
            continue

        # Create directory and move file
        article_dir.mkdir(parents=True)
        content_clean, summary, tags = _parse_and_strip_metadata(content)
        target = article_dir / "content.md"
        target.write_text(content_clean, encoding="utf-8")

        # Save original filename as display title
        title_file = article_dir / ".title"
        title_file.write_text(f.stem, encoding="utf-8")

        # Save manual metadata if provided
        if summary or tags:
            meta = {}
            if summary:
                meta["summary"] = summary
            if tags:
                meta["tags"] = tags
            meta_file = article_dir / ".meta"
            meta_file.write_text(
                json.dumps(meta, ensure_ascii=False), encoding="utf-8"
            )
            logger.info("Manual meta: summary=%s, tags=%s", summary, tags)

        f.unlink()  # remove original loose file

        logger.info(
            "Intake: %s → %s/content.md (date=%s)",
            f.name, dir_name, dt.strftime("%Y-%m-%d"),
        )
        created_dirs.append(dir_name)

    return created_dirs
