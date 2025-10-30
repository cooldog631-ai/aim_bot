"""Employee repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models.employee import Employee
from src.database.models.permission import Permission


class EmployeeRepository:
    """Repository for employee operations."""

    def __init__(self, db: AsyncSession):
        """Initialize repository with database session."""
        self.db = db

    async def get_by_messenger_id(self, messenger_id: str) -> Optional[Employee]:
        """Get employee by messenger ID."""
        result = await self.db.execute(
            select(Employee)
            .where(Employee.messenger_id == messenger_id)
            .options(selectinload(Employee.permission), selectinload(Employee.department))
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """Get employee by ID."""
        result = await self.db.execute(
            select(Employee)
            .where(Employee.id == employee_id)
            .options(selectinload(Employee.permission), selectinload(Employee.department))
        )
        return result.scalar_one_or_none()

    async def create(
        self, messenger_id: str, full_name: str, messenger_username: Optional[str] = None
    ) -> Employee:
        """Create new employee."""
        employee = Employee(
            messenger_id=messenger_id,
            full_name=full_name,
            messenger_username=messenger_username,
        )
        self.db.add(employee)
        await self.db.flush()

        # Create default permissions
        permission = Permission(employee_id=employee.id, can_submit_reports=True)
        self.db.add(permission)
        await self.db.flush()

        return employee

    async def get_or_create(
        self, messenger_id: str, full_name: str, messenger_username: Optional[str] = None
    ) -> Employee:
        """Get existing employee or create new one."""
        employee = await self.get_by_messenger_id(messenger_id)
        if employee:
            return employee

        return await self.create(messenger_id, full_name, messenger_username)

    async def update(self, employee: Employee) -> Employee:
        """Update employee."""
        self.db.add(employee)
        await self.db.flush()
        return employee

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Employee]:
        """Get all employees with pagination."""
        result = await self.db.execute(
            select(Employee)
            .options(selectinload(Employee.permission), selectinload(Employee.department))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
