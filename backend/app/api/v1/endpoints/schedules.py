from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.api.deps import get_current_user, CurrentUser
from app.services.schedule_service import ScheduleService
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse,
    ScheduleListResponse,
)

router = APIRouter(prefix="/schedules", tags=["Schedules"])


@router.get("/medication/{medication_id}", response_model=ScheduleListResponse)
async def get_medication_schedules(
    medication_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = ScheduleService(db)
    return await service.get_by_medication(medication_id)


@router.post("", response_model=ScheduleResponse, status_code=201)
async def create_schedule(
    data: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = ScheduleService(db)
    schedule = await service.create(data, current_user.id)
    return ScheduleResponse.model_validate(schedule)


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: UUID,
    data: ScheduleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = ScheduleService(db)
    schedule = await service.update(schedule_id, data, current_user.id)
    return ScheduleResponse.model_validate(schedule)


@router.delete("/{schedule_id}", status_code=204)
async def delete_schedule(
    schedule_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = ScheduleService(db)
    await service.delete(schedule_id)
