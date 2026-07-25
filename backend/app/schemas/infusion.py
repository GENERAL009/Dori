from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime, time
from typing import Optional
from app.models.infusion import InfusionStatus


class InfusionCreate(BaseModel):
    name: str = Field(..., max_length=200)
    solution: Optional[str] = Field(None, max_length=200)
    volume: Optional[str] = Field(None, max_length=50)
    frequency: str = Field(..., max_length=100)
    time: Optional[time] = None
    clinic: Optional[str] = Field(None, max_length=200)
    doctor: Optional[str] = Field(None, max_length=200)
    start_date: date
    end_date: Optional[date] = None
    duration_days: Optional[int] = None
    total_sessions: Optional[int] = None
    notes: Optional[str] = None
    user_id: UUID


class InfusionUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    solution: Optional[str] = Field(None, max_length=200)
    volume: Optional[str] = Field(None, max_length=50)
    frequency: Optional[str] = Field(None, max_length=100)
    time: Optional[time] = None
    clinic: Optional[str] = Field(None, max_length=200)
    doctor: Optional[str] = Field(None, max_length=200)
    status: Optional[InfusionStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration_days: Optional[int] = None
    total_sessions: Optional[int] = None
    completed_sessions: Optional[int] = None
    notes: Optional[str] = None


class InfusionResponse(BaseModel):
    id: UUID
    name: str
    solution: Optional[str]
    volume: Optional[str]
    frequency: str
    time: Optional[time]
    clinic: Optional[str]
    doctor: Optional[str]
    status: InfusionStatus
    start_date: date
    end_date: Optional[date]
    duration_days: Optional[int]
    total_sessions: Optional[int]
    completed_sessions: int
    notes: Optional[str]
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InfusionListResponse(BaseModel):
    items: list[InfusionResponse]
    total: int
    page: int
    page_size: int
