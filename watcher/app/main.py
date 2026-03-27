"""Blog watcher service — startup sync + real-time file monitoring."""

import json
import logging
import signal
import sys
import time
from pathlib import Path

from watchdog.observers.polling import PollingObserver

from app.ai_service import generate_article_meta, get_existing_tags
from app.config import settings
from app.image_processor import process_images
from app.intake import intake_loose_files
from app.sync import delete_single, find_articles_without_meta, full_sync, sync_single, update_article_meta
from app.watcher import PostsEventHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("watcher")


def _read_manual_meta(article_id: int) -> tuple[str | None, list[str] | None]:
    """Read .meta file for manual summary/tags. Returns (summary, tags)."""
    from app.database import Article, SessionLocal

    with SessionLocal() as session:
        article = session.get(Article, article_id)
        if article is None:
            return None, None
        dir_name = article.file_path.removeprefix("posts/").rsplit("/", 1)[0]

    meta_file = Path(settings.posts_dir) / dir_name / ".meta"
    if not meta_file.is_file():
        return None, None

    try:
        data = json.loads(meta_file.read_text(encoding="utf-8"))
        return data.get("summary"), data.get("tags")
    except (json.JSONDecodeError, OSError):
        return None, None


def _process_new_article(article_id: int, title: str) -> None:
    """Apply manual meta or generate AI meta for a new article."""
    manual_summary, manual_tags = _read_manual_meta(article_id)

    if manual_summary and manual_tags:
        logger.info("Using manual meta for [%d]: summary=%s, tags=%s",
                     article_id, manual_summary, manual_tags)
        update_article_meta(article_id, manual_summary, manual_tags)
        return

    # Need AI for at least some fields
    from app.database import Article, SessionLocal

    with SessionLocal() as session:
        article = session.get(Article, article_id)
        if article is None:
            return
        file_path = article.file_path

    rel = file_path.removeprefix("posts/")
    actual_path = Path(settings.posts_dir) / rel

    if not actual_path.is_file():
        logger.warning("Content file not found: %s", actual_path)
        return

    content = actual_path.read_text(encoding="utf-8")
    existing_tags = get_existing_tags()

    result = generate_article_meta(content, title, existing_tags)
    if result:
        ai_summary, ai_tags = result
        final_summary = manual_summary or ai_summary
        final_tags = manual_tags or ai_tags
        update_article_meta(article_id, final_summary, final_tags)
    elif manual_summary or manual_tags:
        # AI failed but we have partial manual data
        update_article_meta(
            article_id,
            manual_summary or "",
            manual_tags or [],
        )


def _process_images_for_article(article_id: int) -> None:
    """Look up article dir from DB and process external images."""
    from app.database import Article, SessionLocal

    with SessionLocal() as session:
        article = session.get(Article, article_id)
        if article is None:
            return
        dir_name = article.file_path.removeprefix("posts/").rsplit("/", 1)[0]
        article_dir = Path(settings.posts_dir) / dir_name
    process_images(article_id, article_dir)


def _on_change(dir_name: str) -> None:
    """Handle article create/modify event."""
    posts_dir = Path(settings.posts_dir)

    # Handle loose markdown files in the posts root
    candidate = posts_dir / dir_name
    if candidate.is_file() and candidate.suffix.lower() == ".md":
        created = intake_loose_files(posts_dir)
        for new_dir in created:
            result = sync_single(new_dir)
            if result:
                article_id, title = result
                article_dir = posts_dir / new_dir
                process_images(article_id, article_dir)
                _process_new_article(article_id, title)
        return

    result = sync_single(dir_name)
    if result:
        article_id, title = result
        # Process external images before AI (so AI sees final content)
        article_dir = posts_dir / dir_name
        process_images(article_id, article_dir)
        _process_new_article(article_id, title)


def _on_delete(dir_name: str) -> None:
    """Handle article delete event."""
    delete_single(dir_name)


def main() -> None:
    logger.info("Blog Watcher starting...")
    logger.info("Posts dir: %s", settings.posts_dir)
    logger.info("DB path:   %s", settings.db_path)

    posts_dir = Path(settings.posts_dir)
    if not posts_dir.is_dir():
        logger.error("Posts directory does not exist: %s", posts_dir)
        sys.exit(1)

    # ── Phase 0: Intake loose files ──
    created_dirs = intake_loose_files(posts_dir)
    if created_dirs:
        logger.info("Intake: organized %d loose file(s).", len(created_dirs))

    # ── Phase 1: Full sync ──
    logger.info("Running full sync...")
    new_articles = full_sync()
    logger.info("Full sync done. %d new articles found.", len(new_articles))

    # Process images + AI for new articles
    for article_id, title in new_articles:
        _process_images_for_article(article_id)
        _process_new_article(article_id, title)

    # ── Phase 1.5: Backfill missing AI meta ──
    backfill = find_articles_without_meta()
    if backfill:
        logger.info("Backfilling AI meta for %d articles...", len(backfill))
        for article_id, title in backfill:
            _process_new_article(article_id, title)
        logger.info("Backfill complete.")

    # ── Phase 2: Start watchdog ──
    handler = PostsEventHandler(on_change=_on_change, on_delete=_on_delete)
    observer = PollingObserver(timeout=settings.poll_interval)
    observer.schedule(handler, str(posts_dir), recursive=True)
    observer.start()
    logger.info("Watchdog started (polling, interval=%ds), monitoring: %s",
                settings.poll_interval, posts_dir)

    # Graceful shutdown
    stop = False

    def _signal_handler(signum, frame):
        nonlocal stop
        stop = True
        logger.info("Received signal %d, shutting down...", signum)

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    try:
        while not stop:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
        logger.info("Watcher stopped.")


if __name__ == "__main__":
    main()
