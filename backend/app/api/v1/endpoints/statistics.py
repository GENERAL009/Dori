from datetime import date, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.api.deps import get_current_user, CurrentUser
from app.services.statistics_service import StatisticsService
from app.schemas.statistics import DailyStats, WeeklyStats, StatisticsResponse

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("/daily", response_model=DailyStats)
async def get_daily_statistics(
    target_date: date = None,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = StatisticsService(db)
    if target_date is None:
        target_date = date.today()
    return await service.get_daily_stats(current_user.id, target_date)


@router.get("/weekly", response_model=WeeklyStats)
async def get_weekly_statistics(
    week_start: date = None,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = StatisticsService(db)
    if week_start is None:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
    return await service.get_weekly_stats(current_user.id, week_start)


@router.get("/range", response_model=StatisticsResponse)
async def get_range_statistics(
    start_date: date = Query(...),
    end_date: date = Query(...),
    period: str = Query("custom", regex="^(daily|weekly|monthly|custom)$"),
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = StatisticsService(db)
    return await service.get_statistics(current_user.id, period, start_date, end_date)
