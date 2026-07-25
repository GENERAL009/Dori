from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID


class DailyStats(BaseModel):
    date: date
    total_scheduled: int
    taken: int
    missed: int
    skipped: int
    delayed: int
    completion_rate: float
    on_time_rate: float


class WeeklyStats(BaseModel):
    week_start: date
    week_end: date
    total_scheduled: int
    taken: int
    missed: int
    skipped: int
    completion_rate: float
    on_time_rate: float
    daily_breakdown: list[DailyStats]


class MonthlyStats(BaseModel):
    month: int
    year: int
    total_scheduled: int
    taken: int
    missed: int
    skipped: int
    completion_rate: float
    on_time_rate: float
    weekly_breakdown: list[WeeklyStats]


class MedicationStats(BaseModel):
    medication_id: UUID
    medication_name: str
    total_doses: int
    taken: int
    missed: int
    skipped: int
    completion_rate: float
    on_time_rate: float
    average_delay_minutes: Optional[float]


class StatisticsResponse(BaseModel):
    user_id: UUID
    period: str
    start_date: date
    end_date: date
    overall_completion_rate: float
    overall_on_time_rate: float
    total_medications_tracked: int
    daily_stats: list[DailyStats]
    medication_breakdown: list[MedicationStats]
