from uuid import UUID
from datetime import date
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.infusion import Infusion, InfusionStatus
from app.schemas.infusion import InfusionCreate, InfusionUpdate, InfusionResponse, InfusionListResponse
from app.repositories.infusion_repo import InfusionRepository
from app.core.exceptions import NotFoundError


class InfusionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = InfusionRepository(session)

    async def create(self, data: InfusionCreate) -> Infusion:
        end_date = data.end_date
        if not end_date and data.duration_days and data.start_date:
            from datetime import timedelta
            end_date = data.start_date + timedelta(days=data.duration_days)

        infusion = Infusion(
            name=data.name,
            solution=data.solution,
            volume=data.volume,
            frequency=data.frequency,
            time=data.time,
            clinic=data.clinic,
            doctor=data.doctor,
            status=InfusionStatus.ACTIVE,
            start_date=data.start_date,
            end_date=end_date,
            duration_days=data.duration_days,
            total_sessions=data.total_sessions,
            completed_sessions=0,
            notes=data.notes,
            user_id=data.user_id,
            created_by=data.user_id,
            updated_by=data.user_id,
        )
        return await self.repo.create(infusion)

    async def get(self, infusion_id: UUID) -> Infusion:
        infusion = await self.repo.get_by_id(infusion_id)
        if not infusion:
            raise NotFoundError("Infusion")
        return infusion

    async def get_by_user(
        self,
        user_id: UUID,
        status: Optional[InfusionStatus] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> InfusionListResponse:
        skip = (page - 1) * page_size
        infusions = await self.repo.get_by_user(user_id, status, skip, page_size)
        total = await self.repo.count_by_user(user_id, status)
        return InfusionListResponse(
            items=[InfusionResponse.model_validate(i) for i in infusions],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_active_for_date(self, user_id: UUID, target_date: date) -> list[Infusion]:
        return list(await self.repo.get_active_for_date(user_id, target_date))

    async def update(self, infusion_id: UUID, data: InfusionUpdate, user_id: UUID) -> Infusion:
        infusion = await self.get(infusion_id)
        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by"] = user_id
        return await self.repo.update(infusion, update_data)

    async def delete(self, infusion_id: UUID) -> bool:
        await self.get(infusion_id)
        return await self.repo.delete(infusion_id)

    async def mark_session_complete(self, infusion_id: UUID, user_id: UUID) -> Infusion:
        infusion = await self.get(infusion_id)
        infusion.completed_sessions += 1
        if infusion.total_sessions and infusion.completed_sessions >= infusion.total_sessions:
            infusion.status = InfusionStatus.COMPLETED
        infusion.updated_by = user_id
        await self.session.flush()
        await self.session.refresh(infusion)
        return infusion
