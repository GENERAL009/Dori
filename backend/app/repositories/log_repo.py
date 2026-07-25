from typing import Sequence, Optional
from uuid import UUID
from datetime import datetime, date, timezone
from sqlalchemy import select, and_, func, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.log import MedicationLog, InfusionLog, LogStatus
from app.repositories.base import BaseRepository


class MedicationLogRepository(BaseRepository[MedicationLog]):
    def __init__(self, session: AsyncSession):
        super().__init__(MedicationLog, session)

    async def get_by_user_and_date(
        self, user_id: UUID, target_date: date
    ) -> Sequence[MedicationLog]:
        query = select(MedicationLog).where(
            and_(
                MedicationLog.user_id == user_id,
                cast(MedicationLog.scheduled_time, Date) == target_date,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_medication(
        self, medication_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[MedicationLog]:
        query = (
            select(MedicationLog)
            .where(MedicationLog.medication_id == medication_id)
            .order_by(MedicationLog.scheduled_time.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_user_date_range(
        self, user_id: UUID, start_date: date, end_date: date
    ) -> Sequence[MedicationLog]:
        query = select(MedicationLog).where(
            and_(
                MedicationLog.user_id == user_id,
                cast(MedicationLog.scheduled_time, Date) >= start_date,
                cast(MedicationLog.scheduled_time, Date) <= end_date,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_by_status(
        self, user_id: UUID, target_date: date, status: LogStatus
    ) -> int:
        query = select(func.count()).select_from(MedicationLog).where(
            and_(
                MedicationLog.user_id == user_id,
                cast(MedicationLog.scheduled_time, Date) == target_date,
                MedicationLog.status == status,
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def exists_for_schedule(
        self, medication_id: UUID, scheduled_time: datetime
    ) -> bool:
        query = select(func.count()).select_from(MedicationLog).where(
            and_(
                MedicationLog.medication_id == medication_id,
                MedicationLog.scheduled_time == scheduled_time,
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one() > 0


class InfusionLogRepository(BaseRepository[InfusionLog]):
    def __init__(self, session: AsyncSession):
        super().__init__(InfusionLog, session)

    async def get_by_user_and_date(
        self, user_id: UUID, target_date: date
    ) -> Sequence[InfusionLog]:
        query = select(InfusionLog).where(
            and_(
                InfusionLog.user_id == user_id,
                cast(InfusionLog.scheduled_time, Date) == target_date,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_infusion(
        self, infusion_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[InfusionLog]:
        query = (
            select(InfusionLog)
            .where(InfusionLog.infusion_id == infusion_id)
            .order_by(InfusionLog.scheduled_time.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_completed(self, infusion_id: UUID) -> int:
        query = select(func.count()).select_from(InfusionLog).where(
            and_(
                InfusionLog.infusion_id == infusion_id,
                InfusionLog.status == LogStatus.TAKEN,
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one()
