"""Download external images from markdown and localize them."""

import logging
import re
from pathlib import Path
from urllib.parse import urlparse

import httpx

logger = logging.getLogger(__name__)

# Match markdown image: ![alt](http://...)
_MD_IMG_RE = re.compile(
    r'(!\[[^\]]*\]\()'           # prefix: ![alt](
    r'(https?://[^\s\)]+)'       # URL
    r'(\))',                       # suffix: )
)

# Match HTML img tag: <img src="http://..." ... />
_HTML_IMG_RE = re.compile(
    r'(<img\s[^>]*?src=["\'])'   # prefix: <img ... src="
    r'(https?://[^\s"\']+)'      # URL
    r'(["\'][^>]*?>)',            # suffix: "...>
)

_IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif",
    ".webp", ".svg", ".bmp", ".ico",
}


def _is_image_url(url: str) -> bool:
    """Check if URL looks like an image (by extension or path pattern)."""
    parsed = urlparse(url)
    path = parsed.path.lower()
    return any(path.endswith(ext) for ext in _IMAGE_EXTENSIONS)


def _download_image(url: str, dest: Path) -> bool:
    """Download an image from URL to local path. Returns True on success."""
    try:
        with httpx.Client(timeout=30, follow_redirects=True) as client:
            resp = client.get(url)
            resp.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(resp.content)
            logger.info("Downloaded: %s → %s", url, dest.name)
            return True
    except Exception as e:
        logger.error("Failed to download %s: %s", url, e)
        return False


def process_images(article_id: int, article_dir: Path) -> int:
    """Download external images in content.md and rewrite URLs.

    Args:
        article_id: DB article ID (for /api/v1/images/{id}/... URLs)
        article_dir: Absolute path to the article directory

    Returns:
        Number of images successfully processed.
    """
    content_md = article_dir / "content.md"
    if not content_md.is_file():
        return 0

    text = content_md.read_text(encoding="utf-8")
    images_dir = article_dir / "images"
    count = 0

    def _replace(match: re.Match, prefix_idx: int = 1,
                 url_idx: int = 2, suffix_idx: int = 3) -> str:
        nonlocal count
        url = match.group(url_idx)

        # Skip already-local URLs
        if url.startswith("/api/") or url.startswith("images/"):
            return match.group(0)

        if not _is_image_url(url):
            return match.group(0)

        # Extract filename from URL
        parsed = urlparse(url)
        filename = Path(parsed.path).name
        if not filename:
            return match.group(0)

        dest = images_dir / filename
        if dest.exists() or _download_image(url, dest):
            local_url = f"/api/v1/images/{article_id}/{filename}"
            count += 1
            return match.group(prefix_idx) + local_url + match.group(suffix_idx)

        return match.group(0)  # keep original on failure

    # Process both markdown and HTML image patterns
    text = _MD_IMG_RE.sub(lambda m: _replace(m), text)
    text = _HTML_IMG_RE.sub(lambda m: _replace(m), text)

    if count > 0:
        content_md.write_text(text, encoding="utf-8")
        logger.info("Processed %d images in article %d", count, article_id)

    return count
