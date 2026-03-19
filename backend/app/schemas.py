"""Pydantic request/response schemas."""

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# ─── Generic response wrappers ───────────────────────────────────────


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response envelope."""

    code: int = 200
    message: str = "success"
    data: T | None = None


class PaginatedData(BaseModel, Generic[T]):
    """Paginated list wrapper."""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


# ─── Tag schemas ─────────────────────────────────────────────────────


class TagOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class TagWithCount(BaseModel):
    id: int
    name: str
    article_count: int

    model_config = {"from_attributes": True}


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


# ─── Article schemas ─────────────────────────────────────────────────


class ArticleSummaryOut(BaseModel):
    """Article list item (no content)."""

    id: int
    title: str
    summary: str | None = None
    tags: list[TagOut] = []
    created_at: datetime
    published_at: datetime | None = None

    model_config = {"from_attributes": True}


class ArticleNav(BaseModel):
    """Minimal article info for prev/next navigation."""

    id: int
    title: str


class ArticleDetailOut(BaseModel):
    """Full article detail with rendered HTML."""

    id: int
    title: str
    summary: str | None = None
    content_html: str
    content_raw: str
    header_image: str | None = None
    tags: list[TagOut] = []
    prev_article: ArticleNav | None = None
    next_article: ArticleNav | None = None
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None = None


class AboutOut(BaseModel):
    """About page response."""

    id: int = 0
    title: str
    content_html: str
    content_raw: str
    updated_at: datetime


# ─── Archive schemas ─────────────────────────────────────────────────


class ArchiveArticle(BaseModel):
    id: int
    title: str
    published_at: datetime | None = None


class ArchiveGroup(BaseModel):
    year: int
    count: int
    articles: list[ArchiveArticle]


# ─── Auth schemas ────────────────────────────────────────────────────


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    expires_at: datetime


class VerifyResponse(BaseModel):
    valid: bool
    username: str
    expires_at: datetime


# ─── Admin article schemas ───────────────────────────────────────────


class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    summary: str | None = None
    content: str = ""
    header_image: str | None = None
    tag_ids: list[int] = []
    status: str = Field(default="published", pattern="^(draft|published)$")


class ArticleUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    summary: str | None = None
    content: str | None = None
    header_image: str | None = None
    tag_ids: list[int] | None = None
    status: str | None = Field(default=None, pattern="^(draft|published)$")


class ArticleCreateOut(BaseModel):
    id: int
    file_path: str


class ArticleUpdateOut(BaseModel):
    id: int
    updated_at: datetime


# ─── Image schemas ───────────────────────────────────────────────────


class ImageUploadOut(BaseModel):
    url: str
    filename: str
    size: int


# ─── Site schemas ────────────────────────────────────────────────────


class SiteInfo(BaseModel):
    site_title: str
    site_description: str


class SiteInfoUpdate(BaseModel):
    site_title: str | None = None
    site_description: str | None = None
