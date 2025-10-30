"""FastAPI dependencies."""

from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories.employee_repo import EmployeeRepository
from src.database.repositories.report_repo import ReportRepository
from src.database.session import get_db


async def get_employee_repo(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[EmployeeRepository, None]:
    """Get employee repository."""
    yield EmployeeRepository(db)


async def get_report_repo(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[ReportRepository, None]:
    """Get report repository."""
    yield ReportRepository(db)
