from uuid import UUID
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification, NotificationType, NotificationStatus, NotificationLog
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationResponse, NotificationListResponse
from app.repositories.notification_repo import NotificationRepository
from app.core.config import settings
from app.core.exceptions import NotFoundError


class NotificationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = NotificationRepository(session)

    async def create(self, data: NotificationCreate) -> Notification:
        notification = Notification(
            type=data.type,
            message=data.message,
            scheduled_time=data.scheduled_time,
            status=NotificationStatus.PENDING,
            medication_id=data.medication_id,
            infusion_id=data.infusion_id,
            user_id=data.user_id,
            created_by=data.user_id,
            updated_by=data.user_id,
        )
        return await self.repo.create(notification)

    async def get(self, notification_id: UUID) -> Notification:
        notification = await self.repo.get_by_id(notification_id)
        if not notification:
            raise NotFoundError("Notification")
        return notification

    async def get_by_user(
        self,
        user_id: UUID,
        status: Optional[NotificationStatus] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> NotificationListResponse:
        notifications = await self.repo.get_by_user(user_id, status, skip, limit)
        unread = await self.repo.count_unread(user_id)
        return NotificationListResponse(
            items=[NotificationResponse.model_validate(n) for n in notifications],
            total=len(notifications),
            unread_count=unread,
        )

    async def get_pending(self, user_id: UUID) -> list[Notification]:
        return list(await self.repo.get_pending(user_id))

    async def mark_as_read(self, notification_id: UUID, user_id: UUID) -> Notification:
        notification = await self.get(notification_id)
        notification.status = NotificationStatus.READ
        notification.updated_by = user_id
        await self._log_action(notification_id, "read")
        await self.session.flush()
        await self.session.refresh(notification)
        return notification

    async def snooze(self, notification_id: UUID, user_id: UUID) -> Notification:
        notification = await self.get(notification_id)
        notification.status = NotificationStatus.SNOOZED
        notification.snoozed_until = datetime.now(timezone.utc) + timedelta(
            minutes=settings.SNOOZE_DURATION_MINUTES
        )
        notification.updated_by = user_id
        await self._log_action(notification_id, "snoozed")
        await self.session.flush()
        await self.session.refresh(notification)
        return notification

    async def dismiss(self, notification_id: UUID, user_id: UUID) -> Notification:
        notification = await self.get(notification_id)
        notification.status = NotificationStatus.DISMISSED
        notification.updated_by = user_id
        await self._log_action(notification_id, "dismissed")
        await self.session.flush()
        await self.session.refresh(notification)
        return notification

    async def handle_action(
        self, notification_id: UUID, action: str, user_id: UUID
    ) -> Notification:
        if action == "taken":
            return await self.mark_as_read(notification_id, user_id)
        elif action == "snoozed":
            return await self.snooze(notification_id, user_id)
        elif action == "skipped":
            return await self.dismiss(notification_id, user_id)
        elif action == "dismissed":
            return await self.dismiss(notification_id, user_id)
        else:
            return await self.mark_as_read(notification_id, user_id)

    async def _log_action(self, notification_id: UUID, action: str) -> None:
        log = NotificationLog(
            notification_id=notification_id,
            action=action,
            timestamp=datetime.now(timezone.utc),
        )
        self.session.add(log)

    async def get_due_notifications(self) -> list[Notification]:
        return list(await self.repo.get_due_notifications(settings.NOTIFICATION_ADVANCE_MINUTES))

    async def get_snoozed_ready(self) -> list[Notification]:
        return list(await self.repo.get_snoozed_ready())
