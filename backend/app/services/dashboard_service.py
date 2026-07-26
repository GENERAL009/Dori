from uuid import UUID
from datetime import date, datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.medication import MedicationType, MedicationStatus
from app.models.log import LogStatus
from app.schemas.dashboard import DashboardResponse, MedicationSummaryItem, InfusionSummaryItem
from app.services.medication_service import MedicationService
from app.services.infusion_service import InfusionService
from app.services.log_service import LogService
from app.services.auth_service import AuthService


class DashboardService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.med_service = MedicationService(session)
        self.inf_service = InfusionService(session)
        self.log_service = LogService(session)
        self.auth_service = AuthService(session)

    async def get_dashboard(self, user_id: UUID, target_date: date = None) -> DashboardResponse:
        if target_date is None:
            target_date = datetime.now(ZoneInfo("Asia/Tashkent")).date()

        user = await self.auth_service.get_user(user_id)
        active_meds = await self.med_service.get_active_for_date(user_id, target_date)
        active_infusions = await self.inf_service.get_active_for_date(user_id, target_date)
        today_logs = await self.log_service.get_logs_by_user_and_date(user_id, target_date)
        infusion_logs = await self.log_service.get_infusion_logs_by_date(user_id, target_date)

        total_med_doses = sum(len(m.times) for m in active_meds)
        completed_meds = sum(1 for l in today_logs if l.status == LogStatus.TAKEN)
        missed_meds = sum(1 for l in today_logs if l.status == LogStatus.MISSED)
        remaining_meds = total_med_doses - completed_meds - missed_meds
        if remaining_meds < 0:
            remaining_meds = 0

        total_infusions = len(active_infusions)
        completed_infusions = sum(1 for l in infusion_logs if l.status == LogStatus.TAKEN)
        remaining_infusions = total_infusions - completed_infusions

        vitamins = [m for m in active_meds if m.type == MedicationType.VITAMIN]
        injections = [m for m in active_meds if m.type == MedicationType.INJECTION]

        end_dates = [m.end_date for m in active_meds if m.end_date]
        if end_dates:
            latest_end = max(end_dates)
            days_until_end = (latest_end - target_date).days
        else:
            days_until_end = None

        all_start_dates = [m.start_date for m in active_meds]
        if all_start_dates and end_dates:
            earliest_start = min(all_start_dates)
            latest_end = max(end_dates)
            total_duration = (latest_end - earliest_start).days
            elapsed = (target_date - earliest_start).days
            progress = (elapsed / total_duration * 100) if total_duration > 0 else 0
            progress = min(100.0, max(0.0, progress))
        else:
            progress = 0.0

        tz = ZoneInfo("Asia/Tashkent")
        upcoming_meds = []
        for med in active_meds:
            for t in med.times:
                med_logged = any(
                    l.medication_id == med.id
                    and (
                        l.scheduled_time.astimezone(tz).strftime("%H:%M") == t[:5]
                        if l.scheduled_time.tzinfo
                        else l.scheduled_time.strftime("%H:%M") == t[:5]
                    )
                    for l in today_logs
                )
                status = "completed" if med_logged else "pending"
                upcoming_meds.append(
                    MedicationSummaryItem(
                        id=med.id,
                        name=med.name,
                        type=med.type.value,
                        dosage=med.dosage,
                        time=t,
                        status=status,
                        instruction=med.instruction,
                    )
                )
        upcoming_meds.sort(key=lambda x: x.time)

        upcoming_infusions = []
        for inf in active_infusions:
            inf_logged = any(l.infusion_id == inf.id for l in infusion_logs if l.status == LogStatus.TAKEN)
            upcoming_infusions.append(
                InfusionSummaryItem(
                    id=inf.id,
                    name=inf.name,
                    volume=inf.volume,
                    session_number=inf.completed_sessions + 1,
                    total_sessions=inf.total_sessions,
                    status="completed" if inf_logged else "pending",
                )
            )

        return DashboardResponse(
            date=target_date,
            user_name=user.name,
            user_role=user.role.value,
            total_medications_today=total_med_doses,
            completed_medications=completed_meds,
            remaining_medications=remaining_meds,
            missed_medications=missed_meds,
            total_infusions_today=total_infusions,
            completed_infusions=completed_infusions,
            remaining_infusions=remaining_infusions,
            vitamins_count=len(vitamins),
            injections_count=len(injections),
            days_until_treatment_ends=days_until_end,
            treatment_progress_percentage=round(progress, 1),
            upcoming_medications=upcoming_meds,
            upcoming_infusions=upcoming_infusions,
        )
