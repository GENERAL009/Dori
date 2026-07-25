import uuid
import enum
from datetime import date
from sqlalchemy import String, Enum, ForeignKey, Date, Integer, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
import datetime as dt


class InfusionStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Infusion(BaseModel):
    __tablename__ = "infusions"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    solution: Mapped[str | None] = mapped_column(String(200), nullable=True)
    volume: Mapped[str | None] = mapped_column(String(50), nullable=True)
    frequency: Mapped[str] = mapped_column(String(100), nullable=False)
    time: Mapped[dt.time | None] = mapped_column(Time, nullable=True)
    clinic: Mapped[str | None] = mapped_column(String(200), nullable=True)
    doctor: Mapped[str | None] = mapped_column(String(200), nullable=True)
    status: Mapped[InfusionStatus] = mapped_column(
        Enum(InfusionStatus), default=InfusionStatus.ACTIVE
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_sessions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completed_sessions: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="infusions")
    logs: Mapped[list["InfusionLog"]] = relationship(
        back_populates="infusion", lazy="selectin", cascade="all, delete-orphan"
    )


from app.models.user import User  # noqa: E402
from app.models.log import InfusionLog  # noqa: E402
