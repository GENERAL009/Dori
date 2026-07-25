from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.notification import NotificationType, NotificationStatus


class NotificationCreate(BaseModel):
    type: NotificationType
    message: str
    scheduled_time: datetime
    medication_id: Optional[UUID] = None
    infusion_id: Optional[UUID] = None
    user_id: UUID


class NotificationUpdate(BaseModel):
    status: Optional[NotificationStatus] = None
    snoozed_until: Optional[datetime] = None


class NotificationAction(BaseModel):
    action: str  # "taken", "skipped", "snoozed", "dismissed"
    notes: Optional[str] = None


class NotificationResponse(BaseModel):
    id: UUID
    type: NotificationType
    message: str
    scheduled_time: datetime
    status: NotificationStatus
    medication_id: Optional[UUID]
    infusion_id: Optional[UUID]
    user_id: UUID
    snoozed_until: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
    unread_count: int
