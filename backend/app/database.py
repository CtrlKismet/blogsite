"""Async SQLite database setup with SQLAlchemy."""

from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

engine = create_async_engine(
    settings.db_url,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False},
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@event.listens_for(engine.sync_engine, "connect")
def _set_sqlite_pragma(dbapi_conn, connection_record):
    """Enable WAL mode and foreign keys for SQLite."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Yield an async database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """Create tables and insert default data if not present."""
    from app.models import Base

    # Ensure DB directory exists
    db_path = Path(settings.DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Insert default data
    async with async_session() as session:
        from sqlalchemy import select, text

        from app.models import Article, Setting

        # Default settings
        result = await session.execute(select(Setting).where(Setting.key == "site_title"))
        if result.scalar_one_or_none() is None:
            session.add(Setting(key="site_title", value="CtrlKismet's Blog"))
            session.add(Setting(key="site_description", value="个人博客"))

        # About article (id=0)
        result = await session.execute(select(Article).where(Article.id == 0))
        if result.scalar_one_or_none() is None:
            await session.execute(
                text(
                    "INSERT INTO articles (id, title, summary, file_path, status, published_at) "
                    "VALUES (0, 'about', '关于我的介绍', 'posts/about.md', 'published', "
                    "CURRENT_TIMESTAMP)"
                )
            )

        await session.commit()
