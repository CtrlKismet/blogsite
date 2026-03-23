"""Blog watcher service — startup sync + real-time file monitoring."""

import logging
import signal
import sys
import time
from pathlib import Path

from watchdog.observers import Observer

from app.ai_service import generate_article_meta, get_existing_tags
from app.config import settings
from app.sync import delete_single, full_sync, sync_single, update_article_meta
from app.watcher import PostsEventHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("watcher")


def _process_new_article(article_id: int, title: str) -> None:
    """Generate AI meta and update DB for a new article."""
    from app.database import Article, SessionLocal

    with SessionLocal() as session:
        article = session.get(Article, article_id)
        if article is None:
            return
        file_path = article.file_path

    # file_path = "posts/{dir_name}/content.md"
    # posts_dir  = "/data/posts" which contains article dirs directly
    # So: /data/posts/{dir_name}/content.md = posts_dir / file_path.removeprefix("posts/")
    rel = file_path.removeprefix("posts/")
    actual_path = Path(settings.posts_dir) / rel

    if not actual_path.is_file():
        logger.warning("Content file not found: %s", actual_path)
        return

    content = actual_path.read_text(encoding="utf-8")
    existing_tags = get_existing_tags()

    result = generate_article_meta(content, title, existing_tags)
    if result:
        summary, tag_names = result
        update_article_meta(article_id, summary, tag_names)


def _on_change(dir_name: str) -> None:
    """Handle article create/modify event."""
    result = sync_single(dir_name)
    if result:
        article_id, title = result
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

    # ── Phase 1: Full sync ──
    logger.info("Running full sync...")
    new_articles = full_sync()
    logger.info("Full sync done. %d new articles found.", len(new_articles))

    # Process AI for new articles
    for article_id, title in new_articles:
        _process_new_article(article_id, title)

    # ── Phase 2: Start watchdog ──
    handler = PostsEventHandler(on_change=_on_change, on_delete=_on_delete)
    observer = Observer()
    observer.schedule(handler, str(posts_dir), recursive=True)
    observer.start()
    logger.info("Watchdog started, monitoring: %s", posts_dir)

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
