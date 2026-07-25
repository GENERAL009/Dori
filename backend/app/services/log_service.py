from uuid import UUID
from datetime import date, datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.log import MedicationLog, InfusionLog, LogStatus
from app.schemas.log import (
    MedicationLogCreate,
    MedicationLogUpdate,
    MedicationLogResponse,
    InfusionLogCreate,
    InfusionLogUpdate,
    InfusionLogResponse,
    LogListResponse,
)
from app.repositories.log_repo import MedicationLogRepository, InfusionLogRepository
from app.core.exceptions import NotFoundError


class LogService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.med_log_repo = MedicationLogRepository(session)
        self.inf_log_repo = InfusionLogRepository(session)

    async def create_medication_log(self, data: MedicationLogCreate) -> MedicationLog:
        log = MedicationLog(
            medication_id=data.medication_id,
            user_id=data.user_id,
            scheduled_time=data.scheduled_time,
            taken_time=data.taken_time,
            status=data.status,
            notes=data.notes,
            created_by=data.user_id,
            updated_by=data.user_id,
        )
        return await self.med_log_repo.create(log)

    async def get_medication_log(self, log_id: UUID) -> MedicationLog:
        log = await self.med_log_repo.get_by_id(log_id)
        if not log:
            raise NotFoundError("Medication log")
        return log

    async def update_medication_log(
        self, log_id: UUID, data: MedicationLogUpdate, user_id: UUID
    ) -> MedicationLog:
        log = await self.get_medication_log(log_id)
        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by"] = user_id
        return await self.med_log_repo.update(log, update_data)

    async def get_logs_by_user_and_date(
        self, user_id: UUID, target_date: date
    ) -> list[MedicationLog]:
        return list(await self.med_log_repo.get_by_user_and_date(user_id, target_date))

    async def get_logs_by_medication(
        self, medication_id: UUID, page: int = 1, page_size: int = 20
    ) -> LogListResponse:
        skip = (page - 1) * page_size
        logs = await self.med_log_repo.get_by_medication(medication_id, skip, page_size)
        from sqlalchemy import select, func
        from app.models.log import MedicationLog as ML
        result = await self.session.execute(
            select(func.count()).select_from(ML).where(ML.medication_id == medication_id)
        )
        total = result.scalar_one()
        return LogListResponse(
            items=[MedicationLogResponse.model_validate(l) for l in logs],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_logs_by_date_range(
        self, user_id: UUID, start_date: date, end_date: date
    ) -> list[MedicationLog]:
        return list(await self.med_log_repo.get_by_user_date_range(user_id, start_date, end_date))

    async def mark_taken(
        self, medication_id: UUID, user_id: UUID, scheduled_time: datetime
    ) -> MedicationLog:
        now = datetime.now(timezone.utc)
        log = MedicationLog(
            medication_id=medication_id,
            user_id=user_id,
            scheduled_time=scheduled_time,
            taken_time=now,
            status=LogStatus.TAKEN,
            created_by=user_id,
            updated_by=user_id,
        )
        return await self.med_log_repo.create(log)

    async def mark_skipped(
        self, medication_id: UUID, user_id: UUID, scheduled_time: datetime, notes: str = None
    ) -> MedicationLog:
        log = MedicationLog(
            medication_id=medication_id,
            user_id=user_id,
            scheduled_time=scheduled_time,
            status=LogStatus.SKIPPED,
            notes=notes,
            created_by=user_id,
            updated_by=user_id,
        )
        return await self.med_log_repo.create(log)

    async def create_infusion_log(self, data: InfusionLogCreate) -> InfusionLog:
        log = InfusionLog(
            infusion_id=data.infusion_id,
            user_id=data.user_id,
            scheduled_time=data.scheduled_time,
            completed_time=data.completed_time,
            status=data.status,
            notes=data.notes,
            created_by=data.user_id,
            updated_by=data.user_id,
        )
        return await self.inf_log_repo.create(log)

    async def get_infusion_logs_by_date(
        self, user_id: UUID, target_date: date
    ) -> list[InfusionLog]:
        return list(await self.inf_log_repo.get_by_user_and_date(user_id, target_date))
