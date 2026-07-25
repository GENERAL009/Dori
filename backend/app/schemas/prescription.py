from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime
from typing import Optional


class PrescriptionCreate(BaseModel):
    doctor: str = Field(..., max_length=200)
    hospital: Optional[str] = Field(None, max_length=200)
    diagnosis: Optional[str] = None
    date: date
    notes: Optional[str] = None
    image_path: Optional[str] = None
    user_id: UUID


class PrescriptionUpdate(BaseModel):
    doctor: Optional[str] = Field(None, max_length=200)
    hospital: Optional[str] = Field(None, max_length=200)
    diagnosis: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None
    image_path: Optional[str] = None


class PrescriptionResponse(BaseModel):
    id: UUID
    doctor: str
    hospital: Optional[str]
    diagnosis: Optional[str]
    date: date
    notes: Optional[str]
    image_path: Optional[str]
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PrescriptionListResponse(BaseModel):
    items: list[PrescriptionResponse]
    total: int
    page: int
    page_size: int
