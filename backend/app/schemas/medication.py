from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime, time
from typing import Optional
from app.models.medication import MedicationType, MedicationStatus


class MedicationCreate(BaseModel):
    name: str = Field(..., max_length=200)
    type: MedicationType
    dosage: str = Field(..., max_length=100)
    instruction: Optional[str] = None
    frequency: str = Field(..., max_length=100)
    times: list[str] = Field(default_factory=list)
    start_date: date
    end_date: Optional[date] = None
    duration_days: Optional[int] = None
    notes: Optional[str] = None
    user_id: UUID


class MedicationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    type: Optional[MedicationType] = None
    dosage: Optional[str] = Field(None, max_length=100)
    instruction: Optional[str] = None
    frequency: Optional[str] = Field(None, max_length=100)
    times: Optional[list[str]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration_days: Optional[int] = None
    status: Optional[MedicationStatus] = None
    notes: Optional[str] = None


class MedicationResponse(BaseModel):
    id: UUID
    name: str
    type: MedicationType
    dosage: str
    instruction: Optional[str]
    frequency: str
    times: list[str]
    start_date: date
    end_date: Optional[date]
    duration_days: Optional[int]
    status: MedicationStatus
    notes: Optional[str]
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MedicationListResponse(BaseModel):
    items: list[MedicationResponse]
    total: int
    page: int
    page_size: int
