"""Report session model for tracking multi-step conversations."""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base, TimestampMixin


class ReportSession(Base, TimestampMixin):
    """Report session model for tracking conversation state."""

    __tablename__ = "report_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False, index=True)

    # Session state
    status: Mapped[str] = mapped_column(
        String(50), default="active", nullable=False
    )  # 'active', 'waiting_confirmation', 'closed'

    # Session data
    messages: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )  # History of messages in session
    partial_data: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )  # Partially collected report data

    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="report_sessions")

    def __repr__(self) -> str:
        return f"<ReportSession {self.id}: Employee {self.employee_id}, status={self.status}>"
