from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel


class ParsedMedication(BaseModel):
    name: str
    type: str
    dosage: str
    frequency: str
    times: List[str]
    duration_days: int | None = None
    instruction: str | None = None
    notes: str | None = None


class ParsedPrescription(BaseModel):
    doctor: str | None = None
    hospital: str | None = None
    diagnosis: str | None = None
    date: str | None = None
    medications: List[ParsedMedication] = []


class PrescriptionParser(ABC):
    @abstractmethod
    async def parse_image(self, image_path: str) -> ParsedPrescription:
        pass

    @abstractmethod
    async def parse_text(self, text: str) -> ParsedPrescription:
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        pass
