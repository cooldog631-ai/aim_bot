"""Department model."""

from typing import Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class Department(Base):
    """Department model."""

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    employees: Mapped[list["Employee"]] = relationship(back_populates="department")

    def __repr__(self) -> str:
        return f"<Department {self.id}: {self.name}>"
