"""Watcher service configuration."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    db_path: str = os.environ.get("DB_PATH", "/data/db/blog.db")
    posts_dir: str = os.environ.get("POSTS_DIR", "/data/posts")

    # AI service (OpenAI-compatible)
    ai_base_url: str = os.environ.get("AI_BASE_URL", "https://api.openai.com/v1")
    ai_api_key: str = os.environ.get("AI_API_KEY", "")
    ai_model: str = os.environ.get("AI_MODEL", "gpt-4o-mini")

    # Watcher
    debounce_seconds: float = float(os.environ.get("DEBOUNCE_SECONDS", "5"))

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_path}"


settings = Settings()
