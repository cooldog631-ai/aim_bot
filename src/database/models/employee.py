"""Employee model."""

from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base, TimestampMixin


class Employee(Base, TimestampMixin):
    """Employee model."""

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    messenger_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    messenger_username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)

    # Relationships
    department: Mapped[Optional["Department"]] = relationship(back_populates="employees")
    permission: Mapped[Optional["Permission"]] = relationship(back_populates="employee", uselist=False)
    reports: Mapped[list["Report"]] = relationship(back_populates="employee")
    report_sessions: Mapped[list["ReportSession"]] = relationship(back_populates="employee")

    def __repr__(self) -> str:
        return f"<Employee {self.id}: {self.full_name} (@{self.messenger_username})>"
