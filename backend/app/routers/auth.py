"""Authentication routes."""

from fastapi import APIRouter, HTTPException, status

from app.config import settings
from app.dependencies import CurrentUser
from app.schemas import ApiResponse, LoginRequest, LoginResponse, VerifyResponse
from app.utils.security import create_access_token, decode_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(body: LoginRequest):
    """Authenticate admin user and return JWT token."""
    if not settings.ADMIN_PASSWORD_HASH:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="管理员密码未配置",
        )

    if body.username != settings.ADMIN_USERNAME or not verify_password(
        body.password, settings.ADMIN_PASSWORD_HASH
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    token, expires_at = create_access_token(body.username)
    return ApiResponse(data=LoginResponse(access_token=token, expires_at=expires_at))


@router.get("/verify", response_model=ApiResponse[VerifyResponse])
async def verify_token(current_user: CurrentUser):
    """Verify the current JWT token is valid."""
    # If we reached here, the token is valid (dependency checked it)
    # Get expiry from a fresh decode for display
    from datetime import UTC, datetime

    token_info = {"username": current_user, "valid": True}
    # Approximate expiry
    _, expires_at = create_access_token(current_user)
    return ApiResponse(
        data=VerifyResponse(
            valid=True,
            username=current_user,
            expires_at=expires_at,
        )
    )
