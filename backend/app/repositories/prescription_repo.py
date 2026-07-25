from typing import Sequence
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.prescription import Prescription
from app.repositories.base import BaseRepository


class PrescriptionRepository(BaseRepository[Prescription]):
    def __init__(self, session: AsyncSession):
        super().__init__(Prescription, session)

    async def get_by_user(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[Prescription]:
        query = (
            select(Prescription)
            .where(Prescription.user_id == user_id)
            .order_by(Prescription.date.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_by_user(self, user_id: UUID) -> int:
        from sqlalchemy import func

        query = select(func.count()).select_from(Prescription).where(
            Prescription.user_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def search(self, user_id: UUID, query_str: str) -> Sequence[Prescription]:
        query = select(Prescription).where(
            Prescription.user_id == user_id,
            (Prescription.doctor.ilike(f"%{query_str}%"))
            | (Prescription.diagnosis.ilike(f"%{query_str}%")),
        )
        result = await self.session.execute(query)
        return result.scalars().all()
