"""Article business logic service."""

import math
import re
import shutil
from datetime import UTC, datetime
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models import Article, ArticleTag, Tag
from app.schemas import (
    ArticleCreate,
    ArticleDetailOut,
    ArticleNav,
    ArticleSummaryOut,
    ArticleUpdate,
    ArchiveArticle,
    ArchiveGroup,
)
from app.services.markdown_service import render_markdown

# Characters not allowed in article titles (filesystem-unsafe)
_TITLE_ILLEGAL_RE = re.compile(r'[/\\:*?"<>|]')


def _validate_title(title: str) -> None:
    """Ensure title contains only filesystem-safe characters."""
    if _TITLE_ILLEGAL_RE.search(title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="标题包含非法字符：/\\:*?\"<>|",
        )


def _read_markdown_file(file_path: str) -> str:
    """Read markdown content from posts directory."""
    full_path = settings.posts_path.parent / file_path
    if not full_path.is_file():
        return ""
    return full_path.read_text(encoding="utf-8")


def _write_markdown_file(file_path: str, content: str) -> None:
    """Write markdown content to posts directory."""
    full_path = settings.posts_path.parent / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding="utf-8")


# ─── Public API query functions ──────────────────────────────────────


async def get_article_list(
    session: AsyncSession,
    page: int = 1,
    page_size: int = 10,
    tag_id: int | None = None,
    year: int | None = None,
) -> dict:
    """Get paginated published article list (excludes About article id=0)."""
    page_size = min(page_size, 50)

    # Base query: published articles, id > 0
    query = select(Article).where(Article.id > 0, Article.status == "published")

    if tag_id is not None:
        query = query.join(ArticleTag).where(ArticleTag.tag_id == tag_id)

    if year is not None:
        query = query.where(func.strftime("%Y", Article.published_at) == str(year))

    # Count total
    count_q = select(func.count()).select_from(query.subquery())
    total = (await session.execute(count_q)).scalar() or 0

    # Fetch page
    query = (
        query.options(selectinload(Article.tags))
        .order_by(Article.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await session.execute(query)
    articles = result.scalars().all()

    items = [ArticleSummaryOut.model_validate(a) for a in articles]

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if page_size > 0 else 0,
    }


async def get_article_detail(article_id: int, session: AsyncSession) -> ArticleDetailOut:
    """Get a single article with rendered content and prev/next navigation."""
    result = await session.execute(
        select(Article).options(selectinload(Article.tags)).where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()
    if article is None or (article.status != "published" and article_id != 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    # Read and render markdown
    content_raw = _read_markdown_file(article.file_path)
    content_html = render_markdown(content_raw)

    # Get prev/next articles (only published, id > 0)
    prev_result = await session.execute(
        select(Article)
        .where(Article.id > article_id, Article.id > 0, Article.status == "published")
        .order_by(Article.id.asc())
        .limit(1)
    )
    prev_article = prev_result.scalar_one_or_none()

    next_result = await session.execute(
        select(Article)
        .where(Article.id < article_id, Article.id > 0, Article.status == "published")
        .order_by(Article.id.desc())
        .limit(1)
    )
    next_article = next_result.scalar_one_or_none()

    return ArticleDetailOut(
        id=article.id,
        title=article.title,
        summary=article.summary,
        content_html=content_html,
        content_raw=content_raw,
        header_image=article.header_image,
        tags=[{"id": t.id, "name": t.name} for t in article.tags],
        prev_article=ArticleNav(id=prev_article.id, title=prev_article.title)
        if prev_article
        else None,
        next_article=ArticleNav(id=next_article.id, title=next_article.title)
        if next_article
        else None,
        created_at=article.created_at,
        updated_at=article.updated_at,
        published_at=article.published_at,
    )


async def get_about_article(session: AsyncSession) -> dict:
    """Get the About page (article id=0)."""
    result = await session.execute(select(Article).where(Article.id == 0))
    article = result.scalar_one_or_none()
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="About 页面不存在")

    content_raw = _read_markdown_file(article.file_path)
    content_html = render_markdown(content_raw)

    return {
        "id": 0,
        "title": article.title,
        "content_html": content_html,
        "content_raw": content_raw,
        "updated_at": article.updated_at,
    }


async def get_archive_list(session: AsyncSession) -> list[ArchiveGroup]:
    """Get articles grouped by year for archive view."""
    result = await session.execute(
        select(Article)
        .where(Article.id > 0, Article.status == "published")
        .order_by(Article.published_at.desc())
    )
    articles = result.scalars().all()

    groups: dict[int, list[ArchiveArticle]] = {}
    for a in articles:
        year = a.published_at.year if a.published_at else a.created_at.year
        if year not in groups:
            groups[year] = []
        groups[year].append(
            ArchiveArticle(id=a.id, title=a.title, published_at=a.published_at)
        )

    return [
        ArchiveGroup(year=year, count=len(articles), articles=articles)
        for year, articles in sorted(groups.items(), reverse=True)
    ]


# ─── Admin CRUD functions ───────────────────────────────────────────


async def create_article(data: ArticleCreate, session: AsyncSession) -> dict:
    """Create a new article with markdown file."""
    _validate_title(data.title)

    now = datetime.now(UTC)
    date_prefix = now.strftime("%y-%m-%d")
    dir_name = f"{date_prefix}-{data.title}"
    file_path = f"posts/{dir_name}/content.md"

    article = Article(
        title=data.title,
        summary=data.summary,
        file_path=file_path,
        header_image=data.header_image,
        status=data.status,
        created_at=now,
        updated_at=now,
        published_at=now if data.status == "published" else None,
    )
    session.add(article)
    await session.flush()  # Get auto-generated id

    # Set tags
    if data.tag_ids:
        for tag_id in data.tag_ids:
            session.add(ArticleTag(article_id=article.id, tag_id=tag_id))

    # Write markdown file
    _write_markdown_file(file_path, data.content)

    # Create images directory
    images_dir = settings.posts_path.parent / f"posts/{dir_name}/images"
    images_dir.mkdir(parents=True, exist_ok=True)

    return {"id": article.id, "file_path": file_path}


async def update_article(
    article_id: int, data: ArticleUpdate, session: AsyncSession
) -> dict:
    """Update an existing article."""
    result = await session.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    now = datetime.now(UTC)

    if data.title is not None:
        _validate_title(data.title)
        article.title = data.title

    if data.summary is not None:
        article.summary = data.summary

    if data.header_image is not None:
        article.header_image = data.header_image

    # For non-about articles, update status and tags
    if article_id != 0:
        if data.status is not None:
            article.status = data.status
            if data.status == "published" and article.published_at is None:
                article.published_at = now

        if data.tag_ids is not None:
            # Remove existing tags
            await session.execute(
                select(ArticleTag).where(ArticleTag.article_id == article_id)
            )
            from sqlalchemy import delete

            await session.execute(
                delete(ArticleTag).where(ArticleTag.article_id == article_id)
            )
            for tag_id in data.tag_ids:
                session.add(ArticleTag(article_id=article_id, tag_id=tag_id))

    if data.content is not None:
        _write_markdown_file(article.file_path, data.content)

    article.updated_at = now

    return {"id": article.id, "updated_at": now}


async def delete_article(article_id: int, session: AsyncSession) -> None:
    """Delete an article and its files."""
    if article_id == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="不允许删除 About 页面"
        )

    result = await session.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    # Delete files
    article_dir = settings.posts_path.parent / Path(article.file_path).parent
    if article_dir.is_dir():
        shutil.rmtree(article_dir)

    await session.delete(article)

