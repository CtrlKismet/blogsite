"""Image file serving service."""

import hashlib
import logging
import mimetypes
import os
import tempfile
from pathlib import Path

from fastapi import HTTPException, status
from PIL import Image, ImageOps
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import Article


def get_preview_path(path: Path, width: int) -> Path:
    """Cache bounded WebP previews; preserve animations and original files."""
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".avif"}:
        return path
    temporary = None
    try:
        stat = path.stat()
        key = hashlib.sha256(
            f"v1:{path}:{stat.st_mtime_ns}:{stat.st_size}:{width}".encode()
        ).hexdigest()
        cache = Path(settings.IMAGE_CACHE_DIR)
        target = cache / f"{key}.webp"
        if target.is_file():
            return target
        with Image.open(path) as image:
            if getattr(image, "is_animated", False):
                return path
            image = ImageOps.exif_transpose(image)
            image.thumbnail((width, width * 8), Image.Resampling.LANCZOS)
            has_alpha = "A" in image.getbands() or "transparency" in image.info
            image = image.convert("RGBA" if has_alpha else "RGB")
            cache.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=cache, suffix=".webp", delete=False) as file:
                temporary = Path(file.name)
            image.save(temporary, "WEBP", quality=80, method=4)
            if temporary.stat().st_size >= stat.st_size:
                return path
            os.replace(temporary, target)
            return target
    except (OSError, ValueError, Image.DecompressionBombError):
        logging.getLogger(__name__).warning("Could not generate preview for %s", path)
        return path
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


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
    images_base = (settings.posts_path.parent / article_dir / "images").resolve()
    image_path = (images_base / filename).resolve()

    # Prevent path traversal attacks
    if not image_path.is_relative_to(images_base):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="非法文件名")

    if not image_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="图片不存在")

    return image_path


def guess_media_type(filename: str) -> str:
    """Guess MIME type from filename extension."""
    # Minimal container images may lack WebP/AVIF entries in their MIME database.
    modern_types = {".webp": "image/webp", ".avif": "image/avif"}
    if media_type := modern_types.get(Path(filename).suffix.lower()):
        return media_type
    mime, _ = mimetypes.guess_type(filename)
    return mime or "application/octet-stream"

