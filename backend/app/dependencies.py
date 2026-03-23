"""FastAPI dependency injection helpers."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session

# Typed alias for DB session dependency
SessionDep = Annotated[AsyncSession, Depends(get_session)]

