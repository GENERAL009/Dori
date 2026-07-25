import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class NotificationType(str, enum.Enum):
    MEDICATION_REMINDER = "medication_reminder"
    INFUSION_REMINDER = "infusion_reminder"
    MISSED_DOSE = "missed_dose"
    REFILL_REMINDER = "refill_reminder"
    TREATMENT_COMPLETE = "treatment_complete"


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    READ = "read"
    SNOOZED = "snoozed"
    DISMISSED = "dismissed"


class Notification(BaseModel):
    __tablename__ = "notifications"

    type: Mapped[NotificationType] = mapped_column(Enum(NotificationType), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    scheduled_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus), default=NotificationStatus.PENDING
    )
    medication_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("medications.id"), nullable=True
    )
    infusion_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("infusions.id"), nullable=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    snoozed_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["User"] = relationship(back_populates="notifications")


class NotificationLog(BaseModel):
    __tablename__ = "notification_logs"

    notification_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("notifications.id"), nullable=False
    )
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)


from app.models.user import User  # noqa: E402
