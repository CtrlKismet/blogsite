"""Public article API routes."""

from fastapi import APIRouter, Query

from app.dependencies import SessionDep
from app.schemas import (
    AboutOut,
    ApiResponse,
    ArticleDetailOut,
    ArticleSummaryOut,
    ArchiveGroup,
    PaginatedData,
)
from app.services import article_service

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=ApiResponse[PaginatedData[ArticleSummaryOut]])
async def list_articles(
    session: SessionDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    tag_id: int | None = Query(None),
    year: int | None = Query(None),
):
    """Get paginated published article list."""
    data = await article_service.get_article_list(
        session, page=page, page_size=page_size, tag_id=tag_id, year=year
    )
    return ApiResponse(data=data)


@router.get("/archive", response_model=ApiResponse[list[ArchiveGroup]])
async def get_archive(session: SessionDep):
    """Get articles grouped by year."""
    data = await article_service.get_archive_list(session)
    return ApiResponse(data=data)


@router.get("/about", response_model=ApiResponse[AboutOut])
async def get_about(session: SessionDep):
    """Get the About page content."""
    data = await article_service.get_about_article(session)
    return ApiResponse(data=data)


@router.get("/{article_id}", response_model=ApiResponse[ArticleDetailOut])
async def get_article(article_id: int, session: SessionDep):
    """Get full article detail by ID."""
    data = await article_service.get_article_detail(article_id, session)
    return ApiResponse(data=data)
