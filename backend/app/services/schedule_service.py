from uuid import UUID
from datetime import time
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schedule import MedicationSchedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse, ScheduleListResponse
from app.repositories.schedule_repo import ScheduleRepository
from app.core.exceptions import NotFoundError


class ScheduleService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ScheduleRepository(session)

    async def create(self, data: ScheduleCreate, user_id: UUID) -> MedicationSchedule:
        schedule = MedicationSchedule(
            medication_id=data.medication_id,
            scheduled_time=data.scheduled_time,
            day_of_week=data.day_of_week,
            created_by=user_id,
            updated_by=user_id,
        )
        return await self.repo.create(schedule)

    async def get(self, schedule_id: UUID) -> MedicationSchedule:
        schedule = await self.repo.get_by_id(schedule_id)
        if not schedule:
            raise NotFoundError("Schedule")
        return schedule

    async def get_by_medication(self, medication_id: UUID) -> ScheduleListResponse:
        schedules = await self.repo.get_by_medication(medication_id)
        return ScheduleListResponse(
            items=[ScheduleResponse.model_validate(s) for s in schedules],
            total=len(schedules),
        )

    async def update(self, schedule_id: UUID, data: ScheduleUpdate, user_id: UUID) -> MedicationSchedule:
        schedule = await self.get(schedule_id)
        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by"] = user_id
        return await self.repo.update(schedule, update_data)

    async def delete(self, schedule_id: UUID) -> bool:
        await self.get(schedule_id)
        return await self.repo.delete(schedule_id)

    async def get_upcoming(
        self, medication_ids: list[UUID], current_time: time, day_of_week: int
    ) -> list[MedicationSchedule]:
        return list(await self.repo.get_upcoming(medication_ids, current_time, day_of_week))
