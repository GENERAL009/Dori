from uuid import UUID
from datetime import date, time
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.medication import Medication, MedicationStatus, MedicationType
from app.models.schedule import MedicationSchedule
from app.schemas.medication import MedicationCreate, MedicationUpdate, MedicationResponse, MedicationListResponse
from app.repositories.medication_repo import MedicationRepository
from app.repositories.schedule_repo import ScheduleRepository
from app.core.exceptions import NotFoundError


class MedicationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = MedicationRepository(session)
        self.schedule_repo = ScheduleRepository(session)

    async def create(self, data: MedicationCreate) -> Medication:
        end_date = data.end_date
        if not end_date and data.duration_days and data.start_date:
            from datetime import timedelta
            end_date = data.start_date + timedelta(days=data.duration_days)

        medication = Medication(
            name=data.name,
            type=data.type,
            dosage=data.dosage,
            instruction=data.instruction,
            frequency=data.frequency,
            times=data.times,
            start_date=data.start_date,
            end_date=end_date,
            duration_days=data.duration_days,
            status=MedicationStatus.ACTIVE,
            notes=data.notes,
            user_id=data.user_id,
            created_by=data.user_id,
            updated_by=data.user_id,
        )
        medication = await self.repo.create(medication)

        for time_str in data.times:
            parts = time_str.split(":")
            sched_time = time(int(parts[0]), int(parts[1]))
            schedule = MedicationSchedule(
                medication_id=medication.id,
                scheduled_time=sched_time,
                created_by=data.user_id,
                updated_by=data.user_id,
            )
            await self.schedule_repo.create(schedule)

        return medication

    async def get(self, medication_id: UUID) -> Medication:
        medication = await self.repo.get_by_id(medication_id)
        if not medication:
            raise NotFoundError("Medication")
        return medication

    async def get_by_user(
        self,
        user_id: UUID,
        status: Optional[MedicationStatus] = None,
        med_type: Optional[MedicationType] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> MedicationListResponse:
        skip = (page - 1) * page_size
        medications = await self.repo.get_by_user(user_id, status, med_type, skip, page_size)
        total = await self.repo.count_by_user(user_id, status, med_type)
        return MedicationListResponse(
            items=[MedicationResponse.model_validate(m) for m in medications],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_active_for_date(self, user_id: UUID, target_date: date) -> list[Medication]:
        return list(await self.repo.get_active_for_date(user_id, target_date))

    async def update(self, medication_id: UUID, data: MedicationUpdate, user_id: UUID) -> Medication:
        medication = await self.get(medication_id)
        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by"] = user_id

        if "times" in update_data and update_data["times"] is not None:
            await self.schedule_repo.delete_by_medication(medication_id)
            for time_str in update_data["times"]:
                parts = time_str.split(":")
                sched_time = time(int(parts[0]), int(parts[1]))
                schedule = MedicationSchedule(
                    medication_id=medication_id,
                    scheduled_time=sched_time,
                    created_by=user_id,
                    updated_by=user_id,
                )
                await self.schedule_repo.create(schedule)

        return await self.repo.update(medication, update_data)

    async def delete(self, medication_id: UUID) -> bool:
        await self.get(medication_id)
        return await self.repo.delete(medication_id)

    async def search(self, user_id: UUID, query: str) -> list[Medication]:
        return list(await self.repo.search(user_id, query))
