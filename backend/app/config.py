"""Application configuration via environment variables."""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DB_PATH: str = "./data/blog.db"

    # Posts storage
    POSTS_DIR: str = "./data/posts"

    # JWT
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24

    # Admin credentials
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD_HASH: str = ""

    # Server
    DEBUG: bool = False

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def db_url(self) -> str:
        """SQLAlchemy async database URL."""
        db_path = Path(self.DB_PATH).resolve()
        return f"sqlite+aiosqlite:///{db_path}"

    @property
    def posts_path(self) -> Path:
        """Resolved posts directory path."""
        return Path(self.POSTS_DIR).resolve()


settings = Settings()
