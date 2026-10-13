"""Public image serving route."""

from typing import Literal

from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool

from app.dependencies import SessionDep
from app.services.image_service import get_image_path, get_preview_path, guess_media_type

router = APIRouter(prefix="/images", tags=["images"])


@router.get("/{article_id}/{filename}")
async def serve_image(
    article_id: int, filename: str, session: SessionDep,
    w: Literal["640", "1280", "1920"] | None = None,
):
    """Serve an article's image file."""
    path = await get_image_path(article_id, filename, session)
    if w is not None:
        path = await run_in_threadpool(get_preview_path, path, int(w))
    return FileResponse(
        path, media_type=guess_media_type(path.name),
        headers={"Cache-Control": "public, max-age=3600"},
    )
