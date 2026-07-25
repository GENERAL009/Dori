import uuid
import enum
from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class UserRole(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    pin_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False, lazy="selectin")
    medications: Mapped[list["Medication"]] = relationship(back_populates="user", lazy="selectin")
    infusions: Mapped[list["Infusion"]] = relationship(back_populates="user", lazy="selectin")
    prescriptions: Mapped[list["Prescription"]] = relationship(back_populates="user", lazy="selectin")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user", lazy="selectin")


class Profile(BaseModel):
    __tablename__ = "profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )
    display_name: Mapped[str] = mapped_column(String(100), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="ru")
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Tashkent")

    user: Mapped["User"] = relationship(back_populates="profile")


from app.models.medication import Medication  # noqa: E402
from app.models.infusion import Infusion  # noqa: E402
from app.models.prescription import Prescription  # noqa: E402
from app.models.notification import Notification  # noqa: E402
