from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.api.deps import get_current_user, CurrentUser
from app.services.prescription_service import PrescriptionService
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionUpdate,
    PrescriptionResponse,
    PrescriptionListResponse,
)

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


@router.get("", response_model=PrescriptionListResponse)
async def list_prescriptions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = PrescriptionService(db)
    return await service.get_by_user(current_user.id, page, page_size)


@router.post("", response_model=PrescriptionResponse, status_code=201)
async def create_prescription(
    data: PrescriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = PrescriptionService(db)
    prescription = await service.create(data)
    return PrescriptionResponse.model_validate(prescription)


@router.get("/search", response_model=list[PrescriptionResponse])
async def search_prescriptions(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = PrescriptionService(db)
    results = await service.search(current_user.id, q)
    return [PrescriptionResponse.model_validate(p) for p in results]


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
async def get_prescription(
    prescription_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = PrescriptionService(db)
    prescription = await service.get(prescription_id)
    return PrescriptionResponse.model_validate(prescription)


@router.put("/{prescription_id}", response_model=PrescriptionResponse)
async def update_prescription(
    prescription_id: UUID,
    data: PrescriptionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = PrescriptionService(db)
    prescription = await service.update(prescription_id, data, current_user.id)
    return PrescriptionResponse.model_validate(prescription)


@router.delete("/{prescription_id}", status_code=204)
async def delete_prescription(
    prescription_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = PrescriptionService(db)
    await service.delete(prescription_id)
