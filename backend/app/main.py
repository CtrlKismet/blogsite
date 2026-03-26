"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

from app.database import init_db
from app.routers import articles, images, site, tags
from app.schemas import ApiResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application startup/shutdown lifecycle."""
    # Startup: initialize database tables and default data
    await init_db()
    yield
    # Shutdown: nothing to clean up


app = FastAPI(
    title="CtrlKismet's Blog API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — restrict to known origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://blog.ctrlkismet.com",
        "http://localhost:5173",  # Vite dev server
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ─── Global exception handler ───────────────────────────────────────


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions and return standard JSON."""
    from fastapi import HTTPException

    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiResponse(
                code=exc.status_code, message=exc.detail, data=None
            ).model_dump(),
        )
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=ApiResponse(code=500, message="服务器内部错误", data=None).model_dump(),
    )


# ─── Register routers ───────────────────────────────────────────────

API_PREFIX = "/api/v1"

app.include_router(articles.router, prefix=API_PREFIX)
app.include_router(tags.router, prefix=API_PREFIX)
app.include_router(images.router, prefix=API_PREFIX)
app.include_router(site.router, prefix=API_PREFIX)


# ─── Health check ────────────────────────────────────────────────────


@app.get("/health")
async def health_check():
    return {"status": "ok"}
