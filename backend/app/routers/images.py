"""Public image serving route."""

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.dependencies import SessionDep
from app.services.image_service import get_image_path, guess_media_type

router = APIRouter(prefix="/images", tags=["images"])


@router.get("/{article_id}/{filename}")
async def serve_image(article_id: int, filename: str, session: SessionDep):
    """Serve an article's image file."""
    path = await get_image_path(article_id, filename, session)
    return FileResponse(path, media_type=guess_media_type(filename))
