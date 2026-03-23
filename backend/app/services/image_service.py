"""Image file serving service."""

import mimetypes
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import Article


async def get_image_path(article_id: int, filename: str, session: AsyncSession) -> Path:
    """Resolve the filesystem path for an article's image.

    Raises 404 if article or image not found.
    """
    result = await session.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    # file_path is like "posts/26-03-18-title/content.md"
    article_dir = Path(article.file_path).parent
    image_path = settings.posts_path.parent / article_dir / "images" / filename

    if not image_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="图片不存在")

    return image_path


def guess_media_type(filename: str) -> str:
    """Guess MIME type from filename extension."""
    mime, _ = mimetypes.guess_type(filename)
    return mime or "application/octet-stream"

