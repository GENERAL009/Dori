from datetime import datetime, date, timezone, timedelta, time
from zoneinfo import ZoneInfo
from sqlalchemy import select, and_, cast, Date
from app.database.session import AsyncSessionLocal
from app.models.user import User
from app.models.medication import Medication, MedicationStatus
from app.models.notification import Notification, NotificationType, NotificationStatus
from app.models.log import MedicationLog, LogStatus
from app.notifications.manager import connection_manager
from app.notifications.channels.websocket import WebSocketNotificationChannel
from app.core.config import settings


async def check_medication_reminders():
    async with AsyncSessionLocal() as session:
        try:
            now = datetime.now(ZoneInfo("Asia/Tashkent"))
            today = now.date()
            current_time = now.time()
            advance = timedelta(minutes=settings.NOTIFICATION_ADVANCE_MINUTES)
            window_end_time = (now + advance).time()

            result = await session.execute(select(User).where(User.is_active == True))
            users = result.scalars().all()

            for user in users:
                meds_result = await session.execute(
                    select(Medication).where(
                        and_(
                            Medication.user_id == user.id,
                            Medication.status == MedicationStatus.ACTIVE,
                            Medication.start_date <= today,
                            (Medication.end_date >= today) | (Medication.end_date.is_(None)),
                        )
                    )
                )
                medications = meds_result.scalars().all()

                for med in medications:
                    for time_str in med.times:
                        parts = time_str.split(":")
                        med_time = time(int(parts[0]), int(parts[1]))

                        if current_time <= med_time <= window_end_time or (
                            current_time <= med_time
                            and (
                                datetime.combine(today, med_time) - now
                            ).total_seconds()
                            <= advance.total_seconds()
                        ):
                            scheduled_dt = datetime.combine(today, med_time, tzinfo=timezone.utc)

                            existing = await session.execute(
                                select(Notification).where(
                                    and_(
                                        Notification.medication_id == med.id,
                                        Notification.scheduled_time == scheduled_dt,
                                        Notification.user_id == user.id,
                                    )
                                )
                            )
                            if existing.scalar_one_or_none():
                                continue

                            notification = Notification(
                                type=NotificationType.MEDICATION_REMINDER,
                                message=f"Time to take {med.name} ({med.dosage})",
                                scheduled_time=scheduled_dt,
                                status=NotificationStatus.PENDING,
                                medication_id=med.id,
                                user_id=user.id,
                                created_by=user.id,
                                updated_by=user.id,
                            )
                            session.add(notification)

                            channel = WebSocketNotificationChannel()
                            await channel.send(
                                str(user.id),
                                "Medication Reminder",
                                f"Time to take {med.name} ({med.dosage})",
                                {
                                    "medication_id": str(med.id),
                                    "medication_name": med.name,
                                    "dosage": med.dosage,
                                    "scheduled_time": time_str,
                                },
                            )

            await session.commit()
        except Exception:
            await session.rollback()


async def check_missed_doses():
    async with AsyncSessionLocal() as session:
        try:
            now = datetime.now(timezone.utc)
            today = date.today()
            grace_period = timedelta(minutes=30)

            result = await session.execute(select(User).where(User.is_active == True))
            users = result.scalars().all()

            for user in users:
                meds_result = await session.execute(
                    select(Medication).where(
                        and_(
                            Medication.user_id == user.id,
                            Medication.status == MedicationStatus.ACTIVE,
                            Medication.start_date <= today,
                            (Medication.end_date >= today) | (Medication.end_date.is_(None)),
                        )
                    )
                )
                medications = meds_result.scalars().all()

                for med in medications:
                    for time_str in med.times:
                        parts = time_str.split(":")
                        med_time = time(int(parts[0]), int(parts[1]))
                        scheduled_dt = datetime.combine(today, med_time, tzinfo=timezone.utc)

                        if now - scheduled_dt < grace_period:
                            continue

                        existing_log = await session.execute(
                            select(MedicationLog).where(
                                and_(
                                    MedicationLog.medication_id == med.id,
                                    MedicationLog.user_id == user.id,
                                    MedicationLog.scheduled_time == scheduled_dt,
                                )
                            )
                        )
                        if existing_log.scalar_one_or_none():
                            continue

                        missed_log = MedicationLog(
                            medication_id=med.id,
                            user_id=user.id,
                            scheduled_time=scheduled_dt,
                            status=LogStatus.MISSED,
                            created_by=user.id,
                            updated_by=user.id,
                        )
                        session.add(missed_log)

                        notification = Notification(
                            type=NotificationType.MISSED_DOSE,
                            message=f"Missed dose: {med.name} ({med.dosage}) at {time_str}",
                            scheduled_time=now,
                            status=NotificationStatus.PENDING,
                            medication_id=med.id,
                            user_id=user.id,
                            created_by=user.id,
                            updated_by=user.id,
                        )
                        session.add(notification)

            await session.commit()
        except Exception:
            await session.rollback()


async def reactivate_snoozed():
    async with AsyncSessionLocal() as session:
        try:
            now = datetime.now(timezone.utc)
            result = await session.execute(
                select(Notification).where(
                    and_(
                        Notification.status == NotificationStatus.SNOOZED,
                        Notification.snoozed_until <= now,
                    )
                )
            )
            snoozed = result.scalars().all()

            for notification in snoozed:
                notification.status = NotificationStatus.SENT
                notification.snoozed_until = None

                channel = WebSocketNotificationChannel()
                await channel.send(
                    str(notification.user_id),
                    "Reminder (Snoozed)",
                    notification.message,
                    {
                        "notification_id": str(notification.id),
                        "medication_id": str(notification.medication_id) if notification.medication_id else None,
                    },
                )

            await session.commit()
        except Exception:
            await session.rollback()
