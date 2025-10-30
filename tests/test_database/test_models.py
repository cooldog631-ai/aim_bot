"""Tests for database models."""

import pytest
from datetime import date

from src.database.models.employee import Employee
from src.database.models.report import Report


class TestEmployeeModel:
    """Test Employee model."""

    @pytest.mark.asyncio
    async def test_create_employee(self, db_session):
        """Test creating employee."""
        employee = Employee(
            full_name="Test User",
            messenger_id="123456789",
            messenger_username="test_user",
        )
        db_session.add(employee)
        await db_session.commit()

        assert employee.id is not None
        assert employee.full_name == "Test User"
        assert employee.messenger_id == "123456789"


class TestReportModel:
    """Test Report model."""

    @pytest.mark.asyncio
    async def test_create_report(self, db_session):
        """Test creating report."""
        # First create employee
        employee = Employee(
            full_name="Test User",
            messenger_id="123456789",
        )
        db_session.add(employee)
        await db_session.flush()

        # Create report
        report = Report(
            employee_id=employee.id,
            report_date=date.today(),
            equipment_number="K-101",
            brigade_number="B-3",
            work_description="Test work description",
        )
        db_session.add(report)
        await db_session.commit()

        assert report.id is not None
        assert report.equipment_number == "K-101"
