from uuid import UUID
from datetime import date, timedelta, datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.log import MedicationLog, LogStatus
from app.schemas.statistics import (
    DailyStats,
    WeeklyStats,
    MonthlyStats,
    MedicationStats,
    StatisticsResponse,
)
from app.repositories.log_repo import MedicationLogRepository
from app.repositories.medication_repo import MedicationRepository


class StatisticsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.log_repo = MedicationLogRepository(session)
        self.med_repo = MedicationRepository(session)

    async def get_daily_stats(self, user_id: UUID, target_date: date) -> DailyStats:
        logs = await self.log_repo.get_by_user_and_date(user_id, target_date)
        total = len(logs)
        taken = sum(1 for l in logs if l.status == LogStatus.TAKEN)
        missed = sum(1 for l in logs if l.status == LogStatus.MISSED)
        skipped = sum(1 for l in logs if l.status == LogStatus.SKIPPED)
        delayed = sum(1 for l in logs if l.status == LogStatus.DELAYED)

        on_time = sum(
            1 for l in logs
            if l.status == LogStatus.TAKEN
            and l.taken_time
            and abs((l.taken_time - l.scheduled_time).total_seconds()) <= 1800
        )

        return DailyStats(
            date=target_date,
            total_scheduled=total,
            taken=taken,
            missed=missed,
            skipped=skipped,
            delayed=delayed,
            completion_rate=taken / total * 100 if total > 0 else 0,
            on_time_rate=on_time / taken * 100 if taken > 0 else 0,
        )

    async def get_weekly_stats(self, user_id: UUID, week_start: date) -> WeeklyStats:
        week_end = week_start + timedelta(days=6)
        daily_breakdown = []
        total_scheduled = 0
        total_taken = 0
        total_missed = 0
        total_skipped = 0
        total_on_time = 0

        for i in range(7):
            day = week_start + timedelta(days=i)
            daily = await self.get_daily_stats(user_id, day)
            daily_breakdown.append(daily)
            total_scheduled += daily.total_scheduled
            total_taken += daily.taken
            total_missed += daily.missed
            total_skipped += daily.skipped

        logs = await self.log_repo.get_by_user_date_range(user_id, week_start, week_end)
        total_on_time = sum(
            1 for l in logs
            if l.status == LogStatus.TAKEN
            and l.taken_time
            and abs((l.taken_time - l.scheduled_time).total_seconds()) <= 1800
        )

        return WeeklyStats(
            week_start=week_start,
            week_end=week_end,
            total_scheduled=total_scheduled,
            taken=total_taken,
            missed=total_missed,
            skipped=total_skipped,
            completion_rate=total_taken / total_scheduled * 100 if total_scheduled > 0 else 0,
            on_time_rate=total_on_time / total_taken * 100 if total_taken > 0 else 0,
            daily_breakdown=daily_breakdown,
        )

    async def get_statistics(
        self, user_id: UUID, period: str, start_date: date, end_date: date
    ) -> StatisticsResponse:
        logs = await self.log_repo.get_by_user_date_range(user_id, start_date, end_date)
        total = len(logs)
        taken = sum(1 for l in logs if l.status == LogStatus.TAKEN)
        on_time = sum(
            1 for l in logs
            if l.status == LogStatus.TAKEN
            and l.taken_time
            and abs((l.taken_time - l.scheduled_time).total_seconds()) <= 1800
        )

        daily_stats = []
        current = start_date
        while current <= end_date:
            daily = await self.get_daily_stats(user_id, current)
            daily_stats.append(daily)
            current += timedelta(days=1)

        medication_breakdown = await self._get_medication_breakdown(user_id, logs)

        medications = await self.med_repo.get_by_user(user_id)

        return StatisticsResponse(
            user_id=user_id,
            period=period,
            start_date=start_date,
            end_date=end_date,
            overall_completion_rate=taken / total * 100 if total > 0 else 0,
            overall_on_time_rate=on_time / taken * 100 if taken > 0 else 0,
            total_medications_tracked=len(medications),
            daily_stats=daily_stats,
            medication_breakdown=medication_breakdown,
        )

    async def _get_medication_breakdown(
        self, user_id: UUID, logs: list[MedicationLog]
    ) -> list[MedicationStats]:
        med_logs: dict = {}
        for log in logs:
            if log.medication_id not in med_logs:
                med_logs[log.medication_id] = []
            med_logs[log.medication_id].append(log)

        breakdown = []
        for med_id, med_log_list in med_logs.items():
            med = await self.med_repo.get_by_id(med_id)
            if not med:
                continue
            total = len(med_log_list)
            taken = sum(1 for l in med_log_list if l.status == LogStatus.TAKEN)
            missed = sum(1 for l in med_log_list if l.status == LogStatus.MISSED)
            skipped = sum(1 for l in med_log_list if l.status == LogStatus.SKIPPED)
            on_time = sum(
                1 for l in med_log_list
                if l.status == LogStatus.TAKEN
                and l.taken_time
                and abs((l.taken_time - l.scheduled_time).total_seconds()) <= 1800
            )
            delays = [
                abs((l.taken_time - l.scheduled_time).total_seconds()) / 60
                for l in med_log_list
                if l.status == LogStatus.TAKEN and l.taken_time
            ]
            avg_delay = sum(delays) / len(delays) if delays else None

            breakdown.append(
                MedicationStats(
                    medication_id=med_id,
                    medication_name=med.name,
                    total_doses=total,
                    taken=taken,
                    missed=missed,
                    skipped=skipped,
                    completion_rate=taken / total * 100 if total > 0 else 0,
                    on_time_rate=on_time / taken * 100 if taken > 0 else 0,
                    average_delay_minutes=avg_delay,
                )
            )
        return breakdown
