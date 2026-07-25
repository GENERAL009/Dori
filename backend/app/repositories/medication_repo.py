from typing import Sequence, Optional
from uuid import UUID
from datetime import date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.medication import Medication, MedicationStatus, MedicationType
from app.repositories.base import BaseRepository


class MedicationRepository(BaseRepository[Medication]):
    def __init__(self, session: AsyncSession):
        super().__init__(Medication, session)

    async def get_by_user(
        self,
        user_id: UUID,
        status: Optional[MedicationStatus] = None,
        med_type: Optional[MedicationType] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Medication]:
        query = select(Medication).where(Medication.user_id == user_id)
        if status:
            query = query.where(Medication.status == status)
        if med_type:
            query = query.where(Medication.type == med_type)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_active_for_date(self, user_id: UUID, target_date: date) -> Sequence[Medication]:
        query = select(Medication).where(
            and_(
                Medication.user_id == user_id,
                Medication.status == MedicationStatus.ACTIVE,
                Medication.start_date <= target_date,
                (Medication.end_date >= target_date) | (Medication.end_date.is_(None)),
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_by_user(
        self,
        user_id: UUID,
        status: Optional[MedicationStatus] = None,
        med_type: Optional[MedicationType] = None,
    ) -> int:
        from sqlalchemy import func

        query = select(func.count()).select_from(Medication).where(
            Medication.user_id == user_id
        )
        if status:
            query = query.where(Medication.status == status)
        if med_type:
            query = query.where(Medication.type == med_type)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def search(self, user_id: UUID, query_str: str) -> Sequence[Medication]:
        query = select(Medication).where(
            and_(
                Medication.user_id == user_id,
                Medication.name.ilike(f"%{query_str}%"),
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()
