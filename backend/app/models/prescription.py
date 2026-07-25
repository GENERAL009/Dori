import uuid
from datetime import date
from sqlalchemy import String, ForeignKey, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class Prescription(BaseModel):
    __tablename__ = "prescriptions"

    doctor: Mapped[str] = mapped_column(String(200), nullable=False)
    hospital: Mapped[str | None] = mapped_column(String(200), nullable=True)
    diagnosis: Mapped[str | None] = mapped_column(Text, nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="prescriptions")


from app.models.user import User  # noqa: E402
