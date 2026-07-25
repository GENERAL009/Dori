from pydantic import BaseModel
from uuid import UUID
from datetime import date, time
from typing import Optional


class MedicationSummaryItem(BaseModel):
    id: UUID
    name: str
    type: str
    dosage: str
    time: str
    status: str
    instruction: Optional[str] = None


class InfusionSummaryItem(BaseModel):
    id: UUID
    name: str
    volume: Optional[str]
    session_number: int
    total_sessions: Optional[int]
    status: str


class DashboardResponse(BaseModel):
    date: date
    user_name: str
    user_role: str

    total_medications_today: int
    completed_medications: int
    remaining_medications: int
    missed_medications: int

    total_infusions_today: int
    completed_infusions: int
    remaining_infusions: int

    vitamins_count: int
    injections_count: int

    days_until_treatment_ends: Optional[int]
    treatment_progress_percentage: float

    upcoming_medications: list[MedicationSummaryItem]
    upcoming_infusions: list[InfusionSummaryItem]

    class Config:
        from_attributes = True
