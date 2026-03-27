"""Watchdog event handler for blog posts directory."""

import logging
import threading
from pathlib import Path

from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    DirMovedEvent,
    FileCreatedEvent,
    FileModifiedEvent,
    FileSystemEventHandler,
)

from app.config import settings

logger = logging.getLogger(__name__)


class PostsEventHandler(FileSystemEventHandler):
    """Debounced handler for content.md changes in posts directory."""

    def __init__(self, on_change: callable, on_delete: callable):
        super().__init__()
        self._on_change = on_change
        self._on_delete = on_delete
        self._timers: dict[str, threading.Timer] = {}
        self._lock = threading.Lock()

    def _debounce(self, key: str, callback: callable, *args):
        """Debounce rapid events for the same key."""
        with self._lock:
            if key in self._timers:
                self._timers[key].cancel()
            timer = threading.Timer(
                settings.debounce_seconds, callback, args=args
            )
            self._timers[key] = timer
            timer.start()

    def _get_dir_name(self, path: str) -> str | None:
        """Extract the article directory name from any path under posts/."""
        try:
            rel = Path(path).relative_to(settings.posts_dir)
            parts = rel.parts
            if parts:
                return parts[0]
        except ValueError:
            pass
        return None

    def _try_rename_md(self, dir_name: str, src_path: str) -> bool:
        """If a non-content.md markdown file is found, rename it to content.md.

        Returns True if a rename occurred.
        """
        p = Path(src_path)
        if p.suffix.lower() != ".md" or p.name == "content.md":
            return False
        article_dir = Path(settings.posts_dir) / dir_name
        content_md = article_dir / "content.md"
        if content_md.exists():
            return False  # already has content.md
        try:
            p.rename(content_md)
            logger.info("Renamed %s → content.md in %s", p.name, dir_name)
            return True
        except OSError as e:
            logger.error("Failed to rename %s: %s", p.name, e)
            return False

    def on_created(self, event):
        if isinstance(event, (FileCreatedEvent, DirCreatedEvent)):
            dir_name = self._get_dir_name(event.src_path)
            if dir_name:
                # Detect loose markdown files in the posts root
                if isinstance(event, FileCreatedEvent):
                    p = Path(event.src_path)
                    if p.parent == Path(settings.posts_dir) and p.suffix.lower() == ".md":
                        logger.debug("Loose file detected: %s", p.name)
                        self._debounce(f"loose:{p.name}", self._on_change, p.name)
                        return
                    # Try rename non-content.md markdown files
                    self._try_rename_md(dir_name, event.src_path)
                content = Path(settings.posts_dir) / dir_name / "content.md"
                if content.is_file():
                    logger.debug("Created: %s", dir_name)
                    self._debounce(dir_name, self._on_change, dir_name)

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            if Path(event.src_path).name == "content.md":
                dir_name = self._get_dir_name(event.src_path)
                if dir_name:
                    logger.debug("Modified: %s", dir_name)
                    self._debounce(dir_name, self._on_change, dir_name)

    def on_deleted(self, event):
        if isinstance(event, DirDeletedEvent):
            dir_name = self._get_dir_name(event.src_path)
            if dir_name:
                logger.debug("Deleted: %s", dir_name)
                self._debounce(f"del:{dir_name}", self._on_delete, dir_name)

    def on_moved(self, event):
        if isinstance(event, DirMovedEvent):
            old_name = self._get_dir_name(event.src_path)
            new_name = self._get_dir_name(event.dest_path)
            if old_name:
                self._debounce(f"del:{old_name}", self._on_delete, old_name)
            if new_name:
                self._debounce(new_name, self._on_change, new_name)
