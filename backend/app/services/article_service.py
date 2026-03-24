"""Article business logic service."""

import math
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models import Article, ArticleTag
from app.schemas import (
    ArticleDetailOut,
    ArticleNav,
    ArticleSummaryOut,
    ArchiveArticle,
    ArchiveGroup,
)
from app.services.markdown_service import render_markdown


def _read_markdown_file(file_path: str) -> str:
    """Read markdown content from posts directory."""
    full_path = settings.posts_path.parent / file_path
    if not full_path.is_file():
        return ""
    return full_path.read_text(encoding="utf-8")


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
    # prev = older article (smaller id), next = newer article (larger id)
    prev_result = await session.execute(
        select(Article)
        .where(Article.id < article_id, Article.id > 0, Article.status == "published")
        .order_by(Article.id.desc())
        .limit(1)
    )
    prev_article = prev_result.scalar_one_or_none()

    next_result = await session.execute(
        select(Article)
        .where(Article.id > article_id, Article.id > 0, Article.status == "published")
        .order_by(Article.id.asc())
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


