from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class PinLogin(BaseModel):
    pin: str = Field(..., min_length=4, max_length=6)


class ProfileSelect(BaseModel):
    user_id: UUID


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: UUID
    user_name: str
    role: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: list[UserResponse]
