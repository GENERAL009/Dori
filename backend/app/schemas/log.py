from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.log import LogStatus


class MedicationLogCreate(BaseModel):
    medication_id: UUID
    user_id: UUID
    scheduled_time: datetime
    taken_time: Optional[datetime] = None
    status: LogStatus
    notes: Optional[str] = None


class MedicationLogUpdate(BaseModel):
    taken_time: Optional[datetime] = None
    status: Optional[LogStatus] = None
    notes: Optional[str] = None


class MedicationLogResponse(BaseModel):
    id: UUID
    medication_id: UUID
    user_id: UUID
    scheduled_time: datetime
    taken_time: Optional[datetime]
    status: LogStatus
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class InfusionLogCreate(BaseModel):
    infusion_id: UUID
    user_id: UUID
    scheduled_time: datetime
    completed_time: Optional[datetime] = None
    status: LogStatus
    notes: Optional[str] = None


class InfusionLogUpdate(BaseModel):
    completed_time: Optional[datetime] = None
    status: Optional[LogStatus] = None
    notes: Optional[str] = None


class InfusionLogResponse(BaseModel):
    id: UUID
    infusion_id: UUID
    user_id: UUID
    scheduled_time: datetime
    completed_time: Optional[datetime]
    status: LogStatus
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class LogListResponse(BaseModel):
    items: list[MedicationLogResponse]
    total: int
    page: int
    page_size: int
