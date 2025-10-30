"""Report model."""

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base, TimestampMixin


class Report(Base, TimestampMixin):
    """Report model."""

    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False, index=True)

    # Report data
    report_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    equipment_number: Mapped[str] = mapped_column(String(100), nullable=False)
    brigade_number: Mapped[str] = mapped_column(String(100), nullable=False)
    work_description: Mapped[str] = mapped_column(Text, nullable=False)

    # Metadata
    transcription: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    structured_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="confirmed", nullable=False
    )  # 'pending', 'validated', 'confirmed'
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="reports")

    def __repr__(self) -> str:
        return f"<Report {self.id}: {self.report_date} - Employee {self.employee_id}>"
