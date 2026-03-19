"""Admin management routes (require authentication)."""

from fastapi import APIRouter, UploadFile
from sqlalchemy import select

from app.dependencies import CurrentUser, SessionDep
from app.models import Tag
from app.schemas import (
    ApiResponse,
    ArticleCreate,
    ArticleCreateOut,
    ArticleUpdate,
    ArticleUpdateOut,
    ImageUploadOut,
    TagCreate,
    TagOut,
)
from app.services import article_service, image_service

router = APIRouter(prefix="/admin", tags=["admin"])


# ─── Article management ──────────────────────────────────────────────


@router.post("/articles", response_model=ApiResponse[ArticleCreateOut])
async def create_article(
    body: ArticleCreate, session: SessionDep, _user: CurrentUser
):
    """Create a new article."""
    data = await article_service.create_article(body, session)
    return ApiResponse(data=data)


@router.put("/articles/{article_id}", response_model=ApiResponse[ArticleUpdateOut])
async def update_article(
    article_id: int, body: ArticleUpdate, session: SessionDep, _user: CurrentUser
):
    """Update an existing article."""
    data = await article_service.update_article(article_id, body, session)
    return ApiResponse(data=data)


@router.delete("/articles/{article_id}", response_model=ApiResponse)
async def delete_article(
    article_id: int, session: SessionDep, _user: CurrentUser
):
    """Delete an article and its files."""
    await article_service.delete_article(article_id, session)
    return ApiResponse(message="文章已删除")


# ─── Tag management ──────────────────────────────────────────────────


@router.post("/tags", response_model=ApiResponse[TagOut])
async def create_tag(body: TagCreate, session: SessionDep, _user: CurrentUser):
    """Create a new tag."""
    tag = Tag(name=body.name)
    session.add(tag)
    await session.flush()
    return ApiResponse(data=TagOut(id=tag.id, name=tag.name))


@router.delete("/tags/{tag_id}", response_model=ApiResponse)
async def delete_tag(tag_id: int, session: SessionDep, _user: CurrentUser):
    """Delete a tag."""
    from fastapi import HTTPException, status

    result = await session.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="标签不存在")
    await session.delete(tag)
    return ApiResponse(message="标签已删除")


# ─── Image management ────────────────────────────────────────────────


@router.post("/images/{article_id}", response_model=ApiResponse[ImageUploadOut])
async def upload_image(
    article_id: int, file: UploadFile, session: SessionDep, _user: CurrentUser
):
    """Upload an image for an article."""
    url, filename, size = await image_service.save_uploaded_image(
        article_id, file, session
    )
    return ApiResponse(data=ImageUploadOut(url=url, filename=filename, size=size))
