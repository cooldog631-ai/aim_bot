"""Permission model."""

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class Permission(Base):
    """Permission model for role-based access control."""

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    # Permissions
    can_submit_reports: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    can_request_reports: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    can_edit_reports: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    can_export_data: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="permission")

    def __repr__(self) -> str:
        return f"<Permission for employee_id={self.employee_id}>"
