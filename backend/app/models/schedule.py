import uuid
import datetime as dt
from sqlalchemy import ForeignKey, Time, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class MedicationSchedule(BaseModel):
    __tablename__ = "medication_schedules"

    medication_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("medications.id"), nullable=False
    )
    scheduled_time: Mapped[dt.time] = mapped_column(Time, nullable=False)
    day_of_week: Mapped[int | None] = mapped_column(Integer, nullable=True)

    medication: Mapped["Medication"] = relationship(back_populates="schedules")


from app.models.medication import Medication  # noqa: E402
