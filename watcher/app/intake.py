"""Intake: pick up loose markdown files and organize into article directories."""

import json
import logging
import re
from datetime import UTC, datetime
from pathlib import Path

from app.metadata import parse_metadata
from app.publication import local_now, parse_publication_time

logger = logging.getLogger(__name__)

# Date pattern at the start of file content: YYYY/MM/DD or YYYY-MM-DD
_DATE_RE = re.compile(r"^(\d{4})[/\-](\d{2})[/\-](\d{2})\s*$")

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
        try:
            content_clean, meta = parse_metadata(content)
            published_at = (
                parse_publication_time(meta["published_at"]) if meta.get("published_at") else None
            )
        except ValueError:
            logger.warning("Invalid published_at in %s; leaving file for correction", f.name)
            continue
        dt = published_at or _parse_date_from_content(content)
        if dt is None:
            dt = local_now()
            logger.info("No date found in %s, using today", f.name)

        # Build directory name: YY-MM-DD-title
        dir_name = f"{dt.strftime('%y-%m-%d')}-{title}"
        article_dir = posts_dir / dir_name

        if article_dir.exists():
            logger.warning("Directory already exists: %s, skipping", dir_name)
            continue

        # Create directory and move file
        article_dir.mkdir(parents=True)
        target = article_dir / "content.md"
        target.write_text(content_clean, encoding="utf-8")

        # Save original filename as display title
        title_file = article_dir / ".title"
        title_file.write_text(f.stem, encoding="utf-8")

        # Keep recognized header fields available for the database sync.
        if meta:
            (article_dir / ".meta").write_text(
                json.dumps(meta, ensure_ascii=False), encoding="utf-8"
            )

        f.unlink()  # remove original loose file

        logger.info(
            "Intake: %s → %s/content.md (date=%s)",
            f.name, dir_name, dt.strftime("%Y-%m-%d"),
        )
        created_dirs.append(dir_name)

    return created_dirs
