from typing import Sequence
from uuid import UUID
from datetime import time
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schedule import MedicationSchedule
from app.repositories.base import BaseRepository


class ScheduleRepository(BaseRepository[MedicationSchedule]):
    def __init__(self, session: AsyncSession):
        super().__init__(MedicationSchedule, session)

    async def get_by_medication(self, medication_id: UUID) -> Sequence[MedicationSchedule]:
        query = select(MedicationSchedule).where(
            MedicationSchedule.medication_id == medication_id
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_upcoming(
        self, medication_ids: list[UUID], current_time: time, day_of_week: int
    ) -> Sequence[MedicationSchedule]:
        query = select(MedicationSchedule).where(
            and_(
                MedicationSchedule.medication_id.in_(medication_ids),
                MedicationSchedule.scheduled_time >= current_time,
                (MedicationSchedule.day_of_week == day_of_week)
                | (MedicationSchedule.day_of_week.is_(None)),
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_by_medication(self, medication_id: UUID) -> None:
        from sqlalchemy import delete

        await self.session.execute(
            delete(MedicationSchedule).where(
                MedicationSchedule.medication_id == medication_id
            )
        )
