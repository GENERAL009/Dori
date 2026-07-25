from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.api.deps import get_current_user, CurrentUser
from app.services.infusion_service import InfusionService
from app.schemas.infusion import (
    InfusionCreate,
    InfusionUpdate,
    InfusionResponse,
    InfusionListResponse,
)
from app.models.infusion import InfusionStatus

router = APIRouter(prefix="/infusions", tags=["Infusions"])


@router.get("", response_model=InfusionListResponse)
async def list_infusions(
    user_id: Optional[UUID] = None,
    status: Optional[InfusionStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = InfusionService(db)
    target_user_id = user_id or current_user.id
    return await service.get_by_user(target_user_id, status, page, page_size)


@router.post("", response_model=InfusionResponse, status_code=201)
async def create_infusion(
    data: InfusionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = InfusionService(db)
    infusion = await service.create(data)
    return InfusionResponse.model_validate(infusion)


@router.get("/{infusion_id}", response_model=InfusionResponse)
async def get_infusion(
    infusion_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = InfusionService(db)
    infusion = await service.get(infusion_id)
    return InfusionResponse.model_validate(infusion)


@router.put("/{infusion_id}", response_model=InfusionResponse)
async def update_infusion(
    infusion_id: UUID,
    data: InfusionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = InfusionService(db)
    infusion = await service.update(infusion_id, data, current_user.id)
    return InfusionResponse.model_validate(infusion)


@router.delete("/{infusion_id}", status_code=204)
async def delete_infusion(
    infusion_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = InfusionService(db)
    await service.delete(infusion_id)


@router.post("/{infusion_id}/complete-session", response_model=InfusionResponse)
async def complete_session(
    infusion_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = InfusionService(db)
    infusion = await service.mark_session_complete(infusion_id, current_user.id)
    return InfusionResponse.model_validate(infusion)
