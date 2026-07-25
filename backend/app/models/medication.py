import uuid
import enum
from datetime import date
from sqlalchemy import String, Enum, ForeignKey, Date, Integer, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class MedicationType(str, enum.Enum):
    TABLET = "tablet"
    CAPSULE = "capsule"
    SYRUP = "syrup"
    INJECTION = "injection"
    INFUSION = "infusion"
    VITAMIN = "vitamin"
    DROPS = "drops"
    SUPPOSITORY = "suppository"
    PACKET = "packet"


class MedicationStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Medication(BaseModel):
    __tablename__ = "medications"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[MedicationType] = mapped_column(Enum(MedicationType), nullable=False)
    dosage: Mapped[str] = mapped_column(String(100), nullable=False)
    instruction: Mapped[str | None] = mapped_column(Text, nullable=True)
    frequency: Mapped[str] = mapped_column(String(100), nullable=False)
    times: Mapped[list] = mapped_column(JSON, default=list)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[MedicationStatus] = mapped_column(
        Enum(MedicationStatus), default=MedicationStatus.ACTIVE
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="medications")
    schedules: Mapped[list["MedicationSchedule"]] = relationship(
        back_populates="medication", lazy="selectin", cascade="all, delete-orphan"
    )
    logs: Mapped[list["MedicationLog"]] = relationship(
        back_populates="medication", lazy="selectin", cascade="all, delete-orphan"
    )


from app.models.user import User  # noqa: E402
from app.models.schedule import MedicationSchedule  # noqa: E402
from app.models.log import MedicationLog  # noqa: E402
