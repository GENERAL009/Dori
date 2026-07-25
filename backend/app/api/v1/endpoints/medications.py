from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.api.deps import get_current_user, CurrentUser
from app.services.medication_service import MedicationService
from app.schemas.medication import (
    MedicationCreate,
    MedicationUpdate,
    MedicationResponse,
    MedicationListResponse,
)
from app.models.medication import MedicationStatus, MedicationType

router = APIRouter(prefix="/medications", tags=["Medications"])


@router.get("", response_model=MedicationListResponse)
async def list_medications(
    user_id: Optional[UUID] = None,
    status: Optional[MedicationStatus] = None,
    type: Optional[MedicationType] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = MedicationService(db)
    target_user_id = user_id or current_user.id
    return await service.get_by_user(target_user_id, status, type, page, page_size)


@router.post("", response_model=MedicationResponse, status_code=201)
async def create_medication(
    data: MedicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = MedicationService(db)
    medication = await service.create(data)
    return MedicationResponse.model_validate(medication)


@router.get("/search", response_model=list[MedicationResponse])
async def search_medications(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = MedicationService(db)
    medications = await service.search(current_user.id, q)
    return [MedicationResponse.model_validate(m) for m in medications]


@router.get("/{medication_id}", response_model=MedicationResponse)
async def get_medication(
    medication_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = MedicationService(db)
    medication = await service.get(medication_id)
    return MedicationResponse.model_validate(medication)


@router.put("/{medication_id}", response_model=MedicationResponse)
async def update_medication(
    medication_id: UUID,
    data: MedicationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = MedicationService(db)
    medication = await service.update(medication_id, data, current_user.id)
    return MedicationResponse.model_validate(medication)


@router.delete("/{medication_id}", status_code=204)
async def delete_medication(
    medication_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = MedicationService(db)
    await service.delete(medication_id)
