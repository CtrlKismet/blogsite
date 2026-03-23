"""Site information routes."""

from fastapi import APIRouter
from sqlalchemy import select

from app.dependencies import SessionDep
from app.models import Setting
from app.schemas import ApiResponse, SiteInfo

router = APIRouter(prefix="/site", tags=["site"])


@router.get("/info", response_model=ApiResponse[SiteInfo])
async def get_site_info(session: SessionDep):
    """Get site title and description."""
    result = await session.execute(select(Setting))
    settings_map = {s.key: s.value for s in result.scalars().all()}

    return ApiResponse(
        data=SiteInfo(
            site_title=settings_map.get("site_title", "Blog"),
            site_description=settings_map.get("site_description", ""),
        )
    )

