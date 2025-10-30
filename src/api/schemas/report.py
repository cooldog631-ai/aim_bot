"""Report schemas."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReportCreate(BaseModel):
    """Report creation schema."""

    employee_id: int
    report_date: date
    equipment_number: str = Field(..., min_length=1, max_length=100)
    brigade_number: str = Field(..., min_length=1, max_length=100)
    work_description: str = Field(..., min_length=1)
    transcription: Optional[str] = None
    structured_data: Optional[dict] = None


class ReportResponse(BaseModel):
    """Report response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    report_date: date
    equipment_number: str
    brigade_number: str
    work_description: str
    transcription: Optional[str] = None
    structured_data: Optional[dict] = None
    status: str
    confirmed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
