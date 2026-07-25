from pydantic import BaseModel
from uuid import UUID
from datetime import time, datetime
from typing import Optional


class ScheduleCreate(BaseModel):
    medication_id: UUID
    scheduled_time: time
    day_of_week: Optional[int] = None


class ScheduleUpdate(BaseModel):
    scheduled_time: Optional[time] = None
    day_of_week: Optional[int] = None


class ScheduleResponse(BaseModel):
    id: UUID
    medication_id: UUID
    scheduled_time: time
    day_of_week: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class ScheduleListResponse(BaseModel):
    items: list[ScheduleResponse]
    total: int
