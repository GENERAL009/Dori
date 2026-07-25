from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import (
    PinLogin,
    ProfileSelect,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse,
    UserListResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=UserListResponse)
async def login_with_pin(data: PinLogin, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    users = await service.authenticate_pin(data.pin)
    return UserListResponse(
        users=[UserResponse.model_validate(u) for u in users]
    )


@router.post("/select-profile", response_model=TokenResponse)
async def select_profile(data: ProfileSelect, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.select_profile(data.user_id)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.refresh_tokens(data.refresh_token)
