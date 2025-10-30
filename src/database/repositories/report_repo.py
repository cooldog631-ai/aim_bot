"""Report repository."""

from datetime import date, datetime
from typing import Optional

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.report import Report


class ReportRepository:
    """Repository for report operations."""

    def __init__(self, db: AsyncSession):
        """Initialize repository with database session."""
        self.db = db

    async def create(
        self,
        employee_id: int,
        report_date: date,
        equipment_number: str,
        brigade_number: str,
        work_description: str,
        transcription: Optional[str] = None,
        structured_data: Optional[dict] = None,
    ) -> Report:
        """Create new report."""
        report = Report(
            employee_id=employee_id,
            report_date=report_date,
            equipment_number=equipment_number,
            brigade_number=brigade_number,
            work_description=work_description,
            transcription=transcription,
            structured_data=structured_data,
            status="confirmed",
            confirmed_at=datetime.now(),
        )
        self.db.add(report)
        await self.db.flush()
        return report

    async def get_by_id(self, report_id: int) -> Optional[Report]:
        """Get report by ID."""
        result = await self.db.execute(select(Report).where(Report.id == report_id))
        return result.scalar_one_or_none()

    async def get_user_reports(
        self, employee_id: int, start_date: date, end_date: date
    ) -> list[Report]:
        """Get reports for employee within date range."""
        result = await self.db.execute(
            select(Report)
            .where(
                Report.employee_id == employee_id,
                Report.report_date >= start_date,
                Report.report_date <= end_date,
            )
            .order_by(desc(Report.report_date))
        )
        return list(result.scalars().all())

    async def get_last_user_report(self, employee_id: int) -> Optional[Report]:
        """Get last report for employee."""
        result = await self.db.execute(
            select(Report)
            .where(Report.employee_id == employee_id)
            .order_by(desc(Report.created_at))
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def update(self, report: Report) -> Report:
        """Update report."""
        self.db.add(report)
        await self.db.flush()
        return report

    async def delete(self, report_id: int) -> bool:
        """Delete report by ID."""
        report = await self.get_by_id(report_id)
        if report:
            await self.db.delete(report)
            await self.db.flush()
            return True
        return False

    async def get_all(
        self, limit: int = 100, offset: int = 0, start_date: Optional[date] = None
    ) -> list[Report]:
        """Get all reports with pagination and optional date filter."""
        query = select(Report)

        if start_date:
            query = query.where(Report.report_date >= start_date)

        query = query.order_by(desc(Report.report_date)).limit(limit).offset(offset)

        result = await self.db.execute(query)
        return list(result.scalars().all())
