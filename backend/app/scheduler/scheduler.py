from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.core.config import settings

scheduler = AsyncIOScheduler()


def start_scheduler():
    from app.scheduler.tasks import check_medication_reminders, check_missed_doses, reactivate_snoozed

    scheduler.add_job(
        check_medication_reminders,
        IntervalTrigger(seconds=settings.NOTIFICATION_CHECK_INTERVAL_SECONDS),
        id="check_medication_reminders",
        replace_existing=True,
    )
    scheduler.add_job(
        check_missed_doses,
        IntervalTrigger(seconds=settings.NOTIFICATION_CHECK_INTERVAL_SECONDS * 5),
        id="check_missed_doses",
        replace_existing=True,
    )
    scheduler.add_job(
        reactivate_snoozed,
        IntervalTrigger(seconds=30),
        id="reactivate_snoozed",
        replace_existing=True,
    )
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()
