from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import verify_pin, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import AuthenticationError
from app.schemas.auth import TokenResponse


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def authenticate_pin(self, pin: str) -> list[User]:
        result = await self.session.execute(
            select(User).where(User.is_active == True)
        )
        users = result.scalars().all()
        matching_users = [u for u in users if verify_pin(pin, u.pin_hash)]
        if not matching_users:
            raise AuthenticationError("Invalid PIN")
        return matching_users

    async def select_profile(self, user_id: UUID) -> TokenResponse:
        result = await self.session.execute(
            select(User).where(User.id == user_id, User.is_active == True)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise AuthenticationError("User not found")

        token_data = {"sub": str(user.id), "role": user.role.value, "name": user.name}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            user_name=user.name,
            role=user.role.value,
        )

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationError("Invalid refresh token")

        user_id = UUID(payload["sub"])
        result = await self.session.execute(
            select(User).where(User.id == user_id, User.is_active == True)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise AuthenticationError("User not found")

        token_data = {"sub": str(user.id), "role": user.role.value, "name": user.name}
        new_access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            user_id=user.id,
            user_name=user.name,
            role=user.role.value,
        )

    async def get_user(self, user_id: UUID) -> User:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise AuthenticationError("User not found")
        return user
