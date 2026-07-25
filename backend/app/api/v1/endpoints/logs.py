from uuid import UUID
from datetime import date, datetime, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.api.deps import get_current_user, CurrentUser
from app.services.log_service import LogService
from app.schemas.log import (
    MedicationLogCreate,
    MedicationLogUpdate,
    MedicationLogResponse,
    InfusionLogCreate,
    InfusionLogResponse,
    LogListResponse,
)

router = APIRouter(prefix="/logs", tags=["Medication Logs"])


@router.get("/medication/{medication_id}", response_model=LogListResponse)
async def get_medication_logs(
    medication_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = LogService(db)
    return await service.get_logs_by_medication(medication_id, page, page_size)


@router.get("/today", response_model=list[MedicationLogResponse])
async def get_today_logs(
    target_date: date = None,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = LogService(db)
    if target_date is None:
        target_date = date.today()
    logs = await service.get_logs_by_user_and_date(current_user.id, target_date)
    return [MedicationLogResponse.model_validate(l) for l in logs]


@router.post("/medication", response_model=MedicationLogResponse, status_code=201)
async def create_medication_log(
    data: MedicationLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = LogService(db)
    log = await service.create_medication_log(data)
    return MedicationLogResponse.model_validate(log)


@router.post("/medication/{medication_id}/taken", response_model=MedicationLogResponse)
async def mark_medication_taken(
    medication_id: UUID,
    scheduled_time: datetime,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = LogService(db)
    log = await service.mark_taken(medication_id, current_user.id, scheduled_time)
    return MedicationLogResponse.model_validate(log)


@router.post("/medication/{medication_id}/skip", response_model=MedicationLogResponse)
async def mark_medication_skipped(
    medication_id: UUID,
    scheduled_time: datetime,
    notes: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = LogService(db)
    log = await service.mark_skipped(medication_id, current_user.id, scheduled_time, notes)
    return MedicationLogResponse.model_validate(log)


@router.put("/{log_id}", response_model=MedicationLogResponse)
async def update_medication_log(
    log_id: UUID,
    data: MedicationLogUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = LogService(db)
    log = await service.update_medication_log(log_id, data, current_user.id)
    return MedicationLogResponse.model_validate(log)


@router.post("/infusion", response_model=InfusionLogResponse, status_code=201)
async def create_infusion_log(
    data: InfusionLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = LogService(db)
    log = await service.create_infusion_log(data)
    return InfusionLogResponse.model_validate(log)
