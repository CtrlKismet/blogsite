"""Watcher service configuration."""

import os
from dataclasses import dataclass, field


def _parse_url_rewrites(raw: str) -> list[tuple[str, str]]:
    """Parse comma-separated "public_origin=internal_base" pairs."""
    rewrites: list[tuple[str, str]] = []
    for item in raw.split(","):
        item = item.strip()
        if "=" not in item:
            continue
        public, internal = (part.strip().rstrip("/") for part in item.split("=", 1))
        if public and internal:
            rewrites.append((public, internal))
    return rewrites


@dataclass(frozen=True)
class Settings:
    timezone: str = os.environ.get("TZ", "Asia/Shanghai")
    db_path: str = os.environ.get("DB_PATH", "/data/db/blog.db")
    # Host path — also the watch path registered with notifier client
    posts_dir: str = os.environ.get("POSTS_DIR", "/data/posts")
    # Container mount target — where files are actually readable
    posts_mount: str = os.environ.get("POSTS_MOUNT", "/data/posts")

    # ── remote-file-notifier integration ──
    notifier_api: str = os.environ.get(
        "NOTIFIER_API", "http://remote-file-notifier-client:9877"
    )
    callback_host: str = os.environ.get("CALLBACK_HOST", "0.0.0.0")
    callback_port: int = int(os.environ.get("CALLBACK_PORT", "8080"))
    self_url: str = os.environ.get(
        "SELF_URL", f"http://blog-watcher:{os.environ.get('CALLBACK_PORT', '8080')}"
    )

    # Watch registration parameters
    watch_events: list[str] = field(default_factory=lambda: [
        e.strip()
        for e in os.environ.get("WATCH_EVENTS", "closed,created,moved").split(",")
        if e.strip()
    ])
    watch_pattern: str = os.environ.get("WATCH_PATTERN", r"\.md$")
    watch_exclude: list[str] = field(default_factory=lambda: [
        e.strip()
        for e in os.environ.get("WATCH_EXCLUDE", ".meta,.title").split(",")
        if e.strip()
    ])

    # ── Internal image host rewrites ──
    # Self-hosted image hosts are reached through the host's reverse proxy,
    # which container traffic cannot always reach (hairpin NAT / host firewall).
    # Map their public origin to the internal service address instead.
    image_url_rewrites: list[tuple[str, str]] = field(default_factory=lambda: _parse_url_rewrites(
        os.environ.get("IMAGE_URL_REWRITES", "")
    ))

    # Processing
    debounce_seconds: float = float(os.environ.get("DEBOUNCE_SECONDS", "5"))

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_path}"


settings = Settings()
