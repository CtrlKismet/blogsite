"""Sync logic: scan posts directory, compare with DB, create/update/delete."""

import hashlib
import logging
import re
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import select, text

from app.config import settings
from app.database import Article, ArticleTag, SessionLocal, Tag

logger = logging.getLogger(__name__)

# Folder name pattern: {yy-mm-dd}-{title}
_DIR_PATTERN = re.compile(r"^(\d{2})-(\d{2})-(\d{2})-(.+)$")


def _parse_dir_name(name: str) -> tuple[datetime, str] | None:
    """Parse folder name → (published_at, title). Returns None for non-matching."""
    m = _DIR_PATTERN.match(name)
    if not m:
        return None
    yy, mm, dd, title = m.groups()
    try:
        dt = datetime(2000 + int(yy), int(mm), int(dd), tzinfo=UTC)
    except ValueError:
        return None
    return dt, title


def _file_hash(path: Path) -> str:
    """SHA-256 hash of file content for change detection."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scan_posts_dir() -> dict[str, Path]:
    """Scan posts directory. Returns {dir_name: content.md path}."""
    posts_dir = Path(settings.posts_dir)
    result: dict[str, Path] = {}
    if not posts_dir.is_dir():
        logger.warning("Posts directory not found: %s", posts_dir)
        return result

    for child in sorted(posts_dir.iterdir()):
        if not child.is_dir():
            continue
        content_file = child / "content.md"
        if content_file.is_file():
            result[child.name] = content_file

    return result


def full_sync() -> list[tuple[int, str]]:
    """Full sync: compare filesystem with DB.

    Returns list of (article_id, title) for NEW articles that need AI processing.
    """
    fs_dirs = scan_posts_dir()
    new_articles: list[tuple[int, str]] = []

    with SessionLocal() as session:
        # Get all articles from DB
        db_articles = {
            a.file_path: a
            for a in session.execute(select(Article)).scalars().all()
        }

        # Track which DB entries are still on disk
        seen_paths: set[str] = set()

        for dir_name, content_path in fs_dirs.items():
            file_path = f"posts/{dir_name}/content.md"
            seen_paths.add(file_path)

            if dir_name == "about":
                # Special: about page (id=0)
                if file_path not in db_articles:
                    _ensure_about(session)
                else:
                    article = db_articles[file_path]
                    article.updated_at = datetime.now(UTC)
                continue

            parsed = _parse_dir_name(dir_name)
            if parsed is None:
                logger.warning("Skipping unrecognized dir: %s", dir_name)
                continue

            published_at, title = parsed

            if file_path in db_articles:
                # Existing article — update timestamp if content changed
                article = db_articles[file_path]
                current_hash = _file_hash(content_path)
                stored_hash = _get_hash(session, article.id)
                if stored_hash != current_hash:
                    article.updated_at = datetime.now(UTC)
                    _set_hash(session, article.id, current_hash)
                    logger.info("Updated: [%d] %s", article.id, title)
            else:
                # New article — insert into DB
                now = datetime.now(UTC)
                article = Article(
                    title=title,
                    file_path=file_path,
                    status="published",
                    created_at=published_at,
                    updated_at=now,
                    published_at=published_at,
                )
                session.add(article)
                session.flush()  # get id
                _set_hash(session, article.id, _file_hash(content_path))
                new_articles.append((article.id, title))
                logger.info("Added: [%d] %s", article.id, title)

        # Delete articles whose folders no longer exist (skip about)
        for file_path, article in db_articles.items():
            if file_path not in seen_paths and article.id != 0:
                logger.info("Deleted: [%d] %s", article.id, article.title)
                session.delete(article)

        session.commit()

    return new_articles


def sync_single(dir_name: str) -> tuple[int, str] | None:
    """Sync a single article directory. Returns (id, title) if NEW."""
    content_path = Path(settings.posts_dir) / dir_name / "content.md"
    if not content_path.is_file():
        return None

    file_path = f"posts/{dir_name}/content.md"

    with SessionLocal() as session:
        existing = session.execute(
            select(Article).where(Article.file_path == file_path)
        ).scalar_one_or_none()

        if dir_name == "about":
            if existing is None:
                _ensure_about(session)
            else:
                existing.updated_at = datetime.now(UTC)
            session.commit()
            return None

        parsed = _parse_dir_name(dir_name)
        if parsed is None:
            return None
        published_at, title = parsed

        if existing:
            current_hash = _file_hash(content_path)
            stored_hash = _get_hash(session, existing.id)
            if stored_hash != current_hash:
                existing.updated_at = datetime.now(UTC)
                _set_hash(session, existing.id, current_hash)
                logger.info("Updated: [%d] %s", existing.id, title)
            session.commit()
            return None
        else:
            now = datetime.now(UTC)
            article = Article(
                title=title,
                file_path=file_path,
                status="published",
                created_at=published_at,
                updated_at=now,
                published_at=published_at,
            )
            session.add(article)
            session.flush()
            _set_hash(session, article.id, _file_hash(content_path))
            session.commit()
            logger.info("Added: [%d] %s", article.id, title)
            return (article.id, title)


def delete_single(dir_name: str) -> None:
    """Remove an article from DB when its folder is deleted."""
    file_path = f"posts/{dir_name}/content.md"
    with SessionLocal() as session:
        article = session.execute(
            select(Article).where(Article.file_path == file_path)
        ).scalar_one_or_none()
        if article and article.id != 0:
            logger.info("Deleted: [%d] %s", article.id, article.title)
            session.delete(article)
            session.commit()


def update_article_meta(article_id: int, summary: str, tag_names: list[str]) -> None:
    """Update article summary and tags from AI results."""
    with SessionLocal() as session:
        article = session.get(Article, article_id)
        if article is None:
            return

        # Update summary
        article.summary = summary

        # Resolve tags — create if not exists
        tag_ids: list[int] = []
        for name in tag_names:
            name = name.strip()
            if not name:
                continue
            tag = session.execute(
                select(Tag).where(Tag.name == name)
            ).scalar_one_or_none()
            if tag is None:
                tag = Tag(name=name)
                session.add(tag)
                session.flush()
                logger.info("Created tag: %s (id=%d)", name, tag.id)
            tag_ids.append(tag.id)

        # Replace article-tag associations
        session.execute(
            text("DELETE FROM article_tags WHERE article_id = :aid"),
            {"aid": article_id},
        )
        for tid in tag_ids:
            session.add(ArticleTag(article_id=article_id, tag_id=tid))

        session.commit()
        logger.info(
            "Meta updated: [%d] summary=%s, tags=%s",
            article_id,
            summary[:40],
            tag_names,
        )


# ─── Helpers ─────────────────────────────────────────────


def _ensure_about(session) -> None:
    """Create about article (id=0) if missing."""
    session.execute(
        text(
            "INSERT OR IGNORE INTO articles (id, title, summary, file_path, status, published_at) "
            "VALUES (0, 'about', '关于我的介绍', 'posts/about/content.md', 'published', "
            "datetime('now'))"
        )
    )


def _get_hash(session, article_id: int) -> str | None:
    """Get stored content hash from settings table."""
    key = f"hash:{article_id}"
    row = session.execute(
        text("SELECT value FROM settings WHERE key = :k"), {"k": key}
    ).first()
    return row[0] if row else None


def _set_hash(session, article_id: int, hash_value: str) -> None:
    """Store content hash in settings table."""
    key = f"hash:{article_id}"
    session.execute(
        text(
            "INSERT INTO settings (key, value, updated_at) VALUES (:k, :v, datetime('now')) "
            "ON CONFLICT(key) DO UPDATE SET value = :v, updated_at = datetime('now')"
        ),
        {"k": key, "v": hash_value},
    )

