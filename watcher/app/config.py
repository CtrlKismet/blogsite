"""Watcher service configuration."""

import os
from dataclasses import dataclass, field
from pathlib import Path


def _read_secret(env_key: str, default: str = "") -> str:
    """Read value from env var, falling back to _FILE variant (Docker secret)."""
    if val := os.environ.get(env_key):
        return val
    file_path = os.environ.get(f"{env_key}_FILE", "")
    if file_path:
        return Path(file_path).read_text().strip()
    return default


@dataclass(frozen=True)
class Settings:
    db_path: str = os.environ.get("DB_PATH", "/data/db/blog.db")
    posts_dir: str = os.environ.get("POSTS_DIR", "/data/posts")

    # AI service (OpenAI-compatible)
    ai_base_url: str = os.environ.get("AI_BASE_URL", "https://api.openai.com/v1")
    ai_api_key: str = field(default_factory=lambda: _read_secret("AI_API_KEY"))
    ai_model: str = os.environ.get("AI_MODEL", "gpt-4o-mini")

    # Watcher
    debounce_seconds: float = float(os.environ.get("DEBOUNCE_SECONDS", "5"))
    poll_interval: int = int(os.environ.get("POLL_INTERVAL", "5"))

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_path}"


settings = Settings()
