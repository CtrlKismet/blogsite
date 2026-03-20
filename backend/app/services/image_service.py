"""Image file management service."""

import mimetypes
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
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


async def save_uploaded_image(
    article_id: int, file: UploadFile, session: AsyncSession
) -> tuple[str, str, int]:
    """Save an uploaded image to the article's images directory.

    Returns (url, filename, size).
    """
    result = await session.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    # Generate unique filename
    ext = Path(file.filename or "image.png").suffix.lower()
    unique_name = f"{uuid.uuid4().hex[:8]}{ext}"

    # Determine save path
    article_dir = Path(article.file_path).parent
    images_dir = settings.posts_path.parent / article_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    save_path = images_dir / unique_name

    # Write file
    content = await file.read()
    save_path.write_bytes(content)

    url = f"/api/v1/images/{article_id}/{unique_name}"
    return url, unique_name, len(content)
