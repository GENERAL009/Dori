import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, BigInteger, DateTime, Enum as SAEnum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TelegramRole(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    PARENT = "parent"


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[TelegramRole | None] = mapped_column(SAEnum(TelegramRole), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class SentReminder(Base):
    __tablename__ = "sent_reminders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    medication_name: Mapped[str] = mapped_column(String(200), nullable=False)
    scheduled_time: Mapped[str] = mapped_column(String(10), nullable=False)
    sent_date: Mapped[str] = mapped_column(String(10), nullable=False)
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
