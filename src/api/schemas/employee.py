"""Employee schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EmployeeResponse(BaseModel):
    """Employee response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    messenger_id: str
    messenger_username: Optional[str] = None
    department_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
