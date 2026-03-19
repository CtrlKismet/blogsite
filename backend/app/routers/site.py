"""Site information routes."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.dependencies import CurrentUser, SessionDep
from app.models import Setting
from app.schemas import ApiResponse, SiteInfo, SiteInfoUpdate

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


@router.put("/info", response_model=ApiResponse[SiteInfo])
async def update_site_info(
    body: SiteInfoUpdate, session: SessionDep, _user: CurrentUser
):
    """Update site title and description (admin only)."""
    updates = body.model_dump(exclude_unset=True)

    for key, value in updates.items():
        if value is not None:
            result = await session.execute(select(Setting).where(Setting.key == key))
            setting = result.scalar_one_or_none()
            if setting:
                setting.value = value
            else:
                session.add(Setting(key=key, value=value))

    # Return updated values
    result = await session.execute(select(Setting))
    settings_map = {s.key: s.value for s in result.scalars().all()}

    return ApiResponse(
        data=SiteInfo(
            site_title=settings_map.get("site_title", "Blog"),
            site_description=settings_map.get("site_description", ""),
        )
    )
