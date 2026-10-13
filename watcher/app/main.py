"""Blog watcher — full sync + remote-file-notifier consumer.

Receives filesystem change events from remote-file-notifier via HTTP callback,
debounces them, and triggers article sync / image processing / meta extraction.
"""

from __future__ import annotations

import json
import logging
import signal
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from queue import Queue
from urllib.parse import urlparse

import httpx

from app.config import settings
from app.database import Article, SessionLocal
from app.image_processor import process_images
from app.intake import intake_loose_files
from app.sync import find_articles_without_meta, full_sync, sync_single, update_article_meta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("watcher")

# ── Event queue for callback → main-thread communication ──
_event_queue: Queue[dict] = Queue()
_stop_event = threading.Event()


# ── Metadata extraction (extracted from main thread) ──

def _extract_meta_from_content(content: str) -> tuple[str, list[str], str]:
    """Extract summary and tags from article content lines.

    Looks for lines starting with '简介：' and 'tag：' (anywhere in the file).
    Tags are comma-separated.
    Returns (summary, tags, cleaned_content) where cleaned_content has those lines removed.
    """
    summary = ""
    tags: list[str] = []
    kept_lines: list[str] = []
    for line in content.splitlines(keepends=True):
        stripped = line.strip()
        if not summary and stripped.startswith("简介："):
            summary = stripped[len("简介："):].strip()
            continue
        if not tags and stripped.lower().startswith("tag："):
            raw = stripped[len("tag："):].strip()
            tags = [t.strip() for t in raw.replace("，", ",").split(",") if t.strip()]
            continue
        kept_lines.append(line)
    return summary, tags, "".join(kept_lines)


def _process_new_article(article_id: int, title: str) -> None:
    """Extract summary and tags from article content and update the DB."""
    with SessionLocal() as session:
        article = session.get(Article, article_id)
        if article is None:
            return
        file_path = article.file_path

    rel = file_path.removeprefix("posts/")
    actual_path = Path(settings.posts_mount) / rel

    if not actual_path.is_file():
        logger.warning("Content file not found: %s", actual_path)
        return

    content = actual_path.read_text(encoding="utf-8")
    summary, tags, cleaned = _extract_meta_from_content(content)

    if summary or tags:
        logger.info("Extracted meta for [%d]: summary=%r, tags=%s", article_id, summary, tags)
        update_article_meta(article_id, summary, tags)
        if cleaned != content:
            actual_path.write_text(cleaned, encoding="utf-8")
            logger.info("Removed 简介/tag lines from: %s", actual_path)
    else:
        logger.info("No 简介/tag lines found for article [%d], skipping meta update.", article_id)


def _process_images_for_article(article_id: int) -> None:
    """Look up article dir from DB and process external images."""
    with SessionLocal() as session:
        article = session.get(Article, article_id)
        if article is None:
            return
        dir_name = article.file_path.removeprefix("posts/").rsplit("/", 1)[0]
        article_dir = Path(settings.posts_mount) / dir_name
    process_images(article_id, article_dir)


# ── Event processing ──

def _to_local(callback_path: str) -> str:
    """Translate callback path (posts_dir prefix) → container mount (posts_mount)."""
    src = settings.posts_dir.rstrip("/")
    dst = settings.posts_mount.rstrip("/")
    if src == dst:
        return callback_path
    if callback_path == src or callback_path.startswith(src + "/"):
        return dst + callback_path[len(src):]
    return callback_path


class DebounceProcessor:
    """Debounces incoming file events and triggers sync when settled."""

    def __init__(self):
        self._timers: dict[str, threading.Timer] = {}
        self._lock = threading.Lock()

    def _get_dir_name(self, path: str) -> str | None:
        """Extract the article directory name from any path under posts_mount."""
        try:
            rel = Path(path).relative_to(settings.posts_mount)
            parts = rel.parts
            if parts:
                return parts[0]
        except ValueError:
            pass
        return None

    def _on_change(self, dir_name: str) -> None:
        """Handle article create/modify event."""
        mount = Path(settings.posts_mount)

        # Handle loose markdown files in the posts root
        candidate = mount / dir_name
        if candidate.is_file() and candidate.suffix.lower() == ".md":
            created = intake_loose_files(mount)
            for new_dir in created:
                result = sync_single(new_dir)
                if result:
                    article_id, title = result
                    article_dir = mount / new_dir
                    process_images(article_id, article_dir)
                    _process_new_article(article_id, title)
            return

        result = sync_single(dir_name)
        if result:
            article_id, title = result
            article_dir = mount / dir_name
            process_images(article_id, article_dir)
            _process_new_article(article_id, title)

    def enqueue(self, event: dict) -> None:
        """Enqueue a callback event for debounced processing.

        event dict has: event_type, path, is_directory, dest_path (optional)
        Paths arrive with posts_dir prefix, translated to posts_mount for local access.
        """
        event_type = event.get("event_type", "")
        event_path = _to_local(event.get("path", ""))
        dest_path = _to_local(event.get("dest_path", "")) if event.get("dest_path") else ""

        # For moved events, handle as: delete old + create new
        if event_type == "moved" and dest_path:
            old_dir = self._get_dir_name(event_path)
            new_dir = self._get_dir_name(dest_path)
            if new_dir:
                logger.info("Event: moved → %s", new_dir)
                self._debounce(new_dir, self._on_change, new_dir)
            elif old_dir:
                logger.debug("Event: moved away — %s", old_dir)
            return

        if event_type == "deleted":
            logger.debug("Ignoring delete event for: %s", event_path)
            return

        # created / closed / modified
        mount = Path(settings.posts_mount)
        p = Path(event_path)

        # Loose markdown file in the posts root: let intake_loose_files organize
        # it into a proper article directory (handled by _on_change).
        if p.parent == mount and p.suffix.lower() == ".md":
            logger.debug("Loose file event: %s", p.name)
            self._debounce(f"loose:{p.name}", self._on_change, p.name)
            return

        dir_name = self._get_dir_name(event_path)
        if dir_name is None:
            return

        # Only act if content.md exists (for the article dir)
        content_md = mount / dir_name / "content.md"
        if content_md.is_file():
            logger.debug("Event: %s → %s", event_type, dir_name)
            self._debounce(dir_name, self._on_change, dir_name)
        else:
            # A markdown file dropped directly inside the article dir (and not
            # named content.md) is adopted as the article content.
            if (
                p.suffix.lower() == ".md"
                and p.name != "content.md"
                and p.parent == mount / dir_name
                and not content_md.exists()
            ):
                try:
                    p.rename(content_md)
                    logger.info("Renamed %s → content.md in %s", p.name, dir_name)
                    self._debounce(dir_name, self._on_change, dir_name)
                except OSError as e:
                    logger.error("Failed to rename %s: %s", p.name, e)

    def _debounce(self, key: str, callback, *args) -> None:
        """Debounce rapid events for the same key."""
        with self._lock:
            if key in self._timers:
                self._timers[key].cancel()
            timer = threading.Timer(settings.debounce_seconds, callback, args=args)
            self._timers[key] = timer
            timer.start()


# ── HTTP callback server ──

class CallbackHandler(BaseHTTPRequestHandler):
    """Minimal HTTP handler for notifier callbacks and health checks."""

    def log_message(self, format, *args):
        """Route to our logger instead of stderr."""
        logger.debug("HTTP: %s", format % args)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._json_response(200, {"status": "ok"})
        else:
            self._json_response(404, {"error": "not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/events":
            self._json_response(404, {"error": "not found"})
            return

        # Read body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b""

        try:
            event = json.loads(body)
        except json.JSONDecodeError:
            self._json_response(400, {"error": "invalid json"})
            return

        # Validate
        if "path" not in event or "event_type" not in event:
            self._json_response(400, {"error": "missing required fields"})
            return

        _event_queue.put(event)
        self._json_response(200, {"status": "ok"})

    def _json_response(self, status: int, data: dict) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


# ── Notifier client integration ──

class NotifierClient:
    """Manages watch registration with the remote-file-notifier client."""

    def __init__(self):
        self._watch_id: str | None = None
        self._client = httpx.Client(timeout=httpx.Timeout(10.0))

    @property
    def watch_id(self) -> str | None:
        return self._watch_id

    def register(self) -> bool:
        """Register a watch with the remote-file-notifier client.

        Retries up to 10 times with 3s delay.
        """
        payload = {
            "path": settings.posts_dir,
            "callback_url": f"{settings.self_url}/events",
            "events": settings.watch_events,
            "pattern": settings.watch_pattern,
            "exclude": settings.watch_exclude,
        }

        for attempt in range(1, 11):
            try:
                resp = self._client.post(
                    f"{settings.notifier_api}/api/v1/watches",
                    json=payload,
                )
                if resp.status_code == 201:
                    data = resp.json()
                    self._watch_id = data.get("watch_id")
                    logger.info(
                        "Watch registered — id=%s  path=%s  events=%s  pattern=%s",
                        self._watch_id,
                        settings.posts_dir,
                        settings.watch_events or "*",
                        settings.watch_pattern or "*",
                    )
                    return True

                logger.warning(
                    "Notifier returned %d on attempt %d/10: %s",
                    resp.status_code, attempt, resp.text[:200],
                )
            except Exception as exc:
                logger.warning("Notifier registration attempt %d/10 failed: %s", attempt, exc)

            if attempt < 10:
                time.sleep(3)

        logger.error("Failed to register watch after 10 attempts")
        return False

    def deregister(self) -> None:
        """Deregister the watch on shutdown."""
        if not self._watch_id:
            return
        try:
            resp = self._client.delete(
                f"{settings.notifier_api}/api/v1/watches/{self._watch_id}"
            )
            if resp.status_code == 200:
                logger.info("Watch deregistered — id=%s", self._watch_id)
            else:
                logger.warning("Deregister returned %d: %s", resp.status_code, resp.text[:200])
        except Exception as exc:
            logger.warning("Failed to deregister watch: %s", exc)

    def close(self) -> None:
        self._client.close()


# ── Main ──

def main() -> None:
    logger.info("Blog Watcher starting (remote-file-notifier mode)...")
    logger.info("Watch path: %s", settings.posts_dir)
    logger.info("Posts dir:  %s", settings.posts_mount)
    logger.info("DB path:    %s", settings.db_path)
    logger.info("Notifier:   %s", settings.notifier_api)
    logger.info("Callback:   %s/events", settings.self_url)

    posts_dir = Path(settings.posts_mount)
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

    for article_id, title in new_articles:
        _process_images_for_article(article_id)
        _process_new_article(article_id, title)

    # ── Phase 1.5: Backfill missing meta ──
    backfill = find_articles_without_meta()
    if backfill:
        logger.info("Backfilling meta for %d articles...", len(backfill))
        for article_id, title in backfill:
            _process_new_article(article_id, title)
        logger.info("Backfill complete.")

    # ── Phase 2: Start HTTP callback server ──
    server = HTTPServer((settings.callback_host, settings.callback_port), CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever, name="callback-server")
    server_thread.daemon = True
    server_thread.start()
    logger.info("Callback server listening on %s:%d", settings.callback_host, settings.callback_port)

    # ── Phase 3: Register with remote-file-notifier ──
    notifier = NotifierClient()
    notifier.register()

    # ── Phase 4: Event processing loop ──
    processor = DebounceProcessor()
    logger.info("Watcher ready — waiting for events...")

    def _shutdown() -> None:
        """Graceful shutdown."""
        logger.info("Shutting down...")
        _stop_event.set()
        notifier.deregister()
        notifier.close()
        server.shutdown()
        logger.info("Watcher stopped.")

    def _signal_handler(signum, frame):
        # Run in a thread to avoid deadlock with server
        threading.Thread(target=_shutdown, name="shutdown").start()

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    try:
        while not _stop_event.is_set():
            try:
                event = _event_queue.get(timeout=1)
                processor.enqueue(event)
            except Exception:
                # Queue.get timeout — just loop to check stop_event
                pass
    finally:
        if not _stop_event.is_set():
            _shutdown()


if __name__ == "__main__":
    main()
