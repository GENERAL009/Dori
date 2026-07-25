import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class LogStatus(str, enum.Enum):
    TAKEN = "taken"
    MISSED = "missed"
    SKIPPED = "skipped"
    DELAYED = "delayed"


class MedicationLog(BaseModel):
    __tablename__ = "medication_logs"

    medication_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("medications.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    scheduled_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    taken_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[LogStatus] = mapped_column(Enum(LogStatus), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    medication: Mapped["Medication"] = relationship(back_populates="logs")


class InfusionLog(BaseModel):
    __tablename__ = "infusion_logs"

    infusion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("infusions.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    scheduled_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[LogStatus] = mapped_column(Enum(LogStatus), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    infusion: Mapped["Infusion"] = relationship(back_populates="logs")


from app.models.medication import Medication  # noqa: E402
from app.models.infusion import Infusion  # noqa: E402
