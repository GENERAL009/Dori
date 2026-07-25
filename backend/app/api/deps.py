from uuid import UUID
from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.core.security import decode_token
from app.core.exceptions import AuthenticationError

security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UUID:
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise AuthenticationError("Invalid or expired token")
    try:
        return UUID(payload["sub"])
    except (KeyError, ValueError):
        raise AuthenticationError("Invalid token payload")


async def get_current_user_role(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    payload = decode_token(credentials.credentials)
    if not payload:
        raise AuthenticationError("Invalid or expired token")
    return payload.get("role", "")


class CurrentUser:
    def __init__(self, user_id: UUID, role: str):
        self.id = user_id
        self.role = role


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUser:
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise AuthenticationError("Invalid or expired token")
    try:
        user_id = UUID(payload["sub"])
        role = payload.get("role", "")
        return CurrentUser(user_id=user_id, role=role)
    except (KeyError, ValueError):
        raise AuthenticationError("Invalid token payload")
