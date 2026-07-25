from typing import Sequence
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification, NotificationStatus
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, session: AsyncSession):
        super().__init__(Notification, session)

    async def get_by_user(
        self,
        user_id: UUID,
        status: NotificationStatus = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[Notification]:
        query = select(Notification).where(Notification.user_id == user_id)
        if status:
            query = query.where(Notification.status == status)
        query = query.order_by(Notification.scheduled_time.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_pending(self, user_id: UUID) -> Sequence[Notification]:
        now = datetime.now(timezone.utc)
        query = select(Notification).where(
            and_(
                Notification.user_id == user_id,
                Notification.status.in_([
                    NotificationStatus.PENDING,
                    NotificationStatus.SENT,
                ]),
                Notification.scheduled_time <= now,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_snoozed_ready(self) -> Sequence[Notification]:
        now = datetime.now(timezone.utc)
        query = select(Notification).where(
            and_(
                Notification.status == NotificationStatus.SNOOZED,
                Notification.snoozed_until <= now,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_unread(self, user_id: UUID) -> int:
        query = select(func.count()).select_from(Notification).where(
            and_(
                Notification.user_id == user_id,
                Notification.status.in_([
                    NotificationStatus.PENDING,
                    NotificationStatus.SENT,
                ]),
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def get_due_notifications(self, advance_minutes: int = 5) -> Sequence[Notification]:
        from datetime import timedelta

        now = datetime.now(timezone.utc)
        window_end = now + timedelta(minutes=advance_minutes)
        query = select(Notification).where(
            and_(
                Notification.status == NotificationStatus.PENDING,
                Notification.scheduled_time <= window_end,
                Notification.scheduled_time >= now - timedelta(minutes=1),
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()
