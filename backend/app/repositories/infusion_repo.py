from typing import Sequence, Optional
from uuid import UUID
from datetime import date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.infusion import Infusion, InfusionStatus
from app.repositories.base import BaseRepository


class InfusionRepository(BaseRepository[Infusion]):
    def __init__(self, session: AsyncSession):
        super().__init__(Infusion, session)

    async def get_by_user(
        self,
        user_id: UUID,
        status: Optional[InfusionStatus] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Infusion]:
        query = select(Infusion).where(Infusion.user_id == user_id)
        if status:
            query = query.where(Infusion.status == status)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_active_for_date(self, user_id: UUID, target_date: date) -> Sequence[Infusion]:
        query = select(Infusion).where(
            and_(
                Infusion.user_id == user_id,
                Infusion.status == InfusionStatus.ACTIVE,
                Infusion.start_date <= target_date,
                (Infusion.end_date >= target_date) | (Infusion.end_date.is_(None)),
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_by_user(
        self, user_id: UUID, status: Optional[InfusionStatus] = None
    ) -> int:
        from sqlalchemy import func

        query = select(func.count()).select_from(Infusion).where(
            Infusion.user_id == user_id
        )
        if status:
            query = query.where(Infusion.status == status)
        result = await self.session.execute(query)
        return result.scalar_one()
