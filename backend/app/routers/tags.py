"""Public tag API routes."""

from fastapi import APIRouter
from sqlalchemy import func, select

from app.dependencies import SessionDep
from app.models import ArticleTag, Tag
from app.schemas import ApiResponse, TagWithCount

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=ApiResponse[list[TagWithCount]])
async def list_tags(session: SessionDep):
    """Get all tags with article counts."""
    query = (
        select(
            Tag.id,
            Tag.name,
            func.count(ArticleTag.article_id).label("article_count"),
        )
        .outerjoin(ArticleTag, Tag.id == ArticleTag.tag_id)
        .group_by(Tag.id)
        .order_by(Tag.name)
    )
    result = await session.execute(query)
    tags = [
        TagWithCount(id=row.id, name=row.name, article_count=row.article_count)
        for row in result.all()
    ]
    return ApiResponse(data=tags)
