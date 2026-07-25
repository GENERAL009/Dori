from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.prescription import Prescription
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionUpdate,
    PrescriptionResponse,
    PrescriptionListResponse,
)
from app.repositories.prescription_repo import PrescriptionRepository
from app.core.exceptions import NotFoundError


class PrescriptionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PrescriptionRepository(session)

    async def create(self, data: PrescriptionCreate) -> Prescription:
        prescription = Prescription(
            doctor=data.doctor,
            hospital=data.hospital,
            diagnosis=data.diagnosis,
            date=data.date,
            notes=data.notes,
            image_path=data.image_path,
            user_id=data.user_id,
            created_by=data.user_id,
            updated_by=data.user_id,
        )
        return await self.repo.create(prescription)

    async def get(self, prescription_id: UUID) -> Prescription:
        prescription = await self.repo.get_by_id(prescription_id)
        if not prescription:
            raise NotFoundError("Prescription")
        return prescription

    async def get_by_user(
        self, user_id: UUID, page: int = 1, page_size: int = 20
    ) -> PrescriptionListResponse:
        skip = (page - 1) * page_size
        prescriptions = await self.repo.get_by_user(user_id, skip, page_size)
        total = await self.repo.count_by_user(user_id)
        return PrescriptionListResponse(
            items=[PrescriptionResponse.model_validate(p) for p in prescriptions],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def update(
        self, prescription_id: UUID, data: PrescriptionUpdate, user_id: UUID
    ) -> Prescription:
        prescription = await self.get(prescription_id)
        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by"] = user_id
        return await self.repo.update(prescription, update_data)

    async def delete(self, prescription_id: UUID) -> bool:
        await self.get(prescription_id)
        return await self.repo.delete(prescription_id)

    async def search(self, user_id: UUID, query: str) -> list[Prescription]:
        return list(await self.repo.search(user_id, query))
