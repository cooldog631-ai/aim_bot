"""Seed database with test data."""

import asyncio
import sys
from datetime import date, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.repositories.employee_repo import EmployeeRepository
from src.database.repositories.report_repo import ReportRepository
from src.database.session import get_db, init_db
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


async def seed_database():
    """Seed database with test data."""
    await init_db()

    async with get_db() as db:
        employee_repo = EmployeeRepository(db)
        report_repo = ReportRepository(db)

        # Create test employees
        logger.info("Creating test employees...")

        employees = [
            await employee_repo.get_or_create("123456789", "Иван Иванов", "ivan_ivanov"),
            await employee_repo.get_or_create("987654321", "Петр Петров", "petr_petrov"),
            await employee_repo.get_or_create("555555555", "Сидор Сидоров", "sidor_sidorov"),
        ]

        logger.info(f"Created {len(employees)} employees")

        # Create test reports
        logger.info("Creating test reports...")

        report_count = 0
        for i, employee in enumerate(employees):
            # Create 5 reports for each employee
            for j in range(5):
                report_date = date.today() - timedelta(days=j)
                await report_repo.create(
                    employee_id=employee.id,
                    report_date=report_date,
                    equipment_number=f"K-{100 + i}",
                    brigade_number=f"B-{i + 1}",
                    work_description=f"Тестовый отчет #{j + 1}: "
                    f"Проверка системы, техническое обслуживание, инструктаж бригады.",
                    transcription=f"Это тестовая транскрипция отчета номер {j + 1}",
                    structured_data={
                        "date": report_date.strftime("%d.%m.%Y"),
                        "equipment_number": f"K-{100 + i}",
                        "brigade_number": f"B-{i + 1}",
                        "work_description": f"Тестовый отчет #{j + 1}",
                    },
                )
                report_count += 1

        logger.info(f"Created {report_count} test reports")
        logger.info("✅ Database seeded successfully!")


if __name__ == "__main__":
    try:
        asyncio.run(seed_database())
    except Exception as e:
        logger.error(f"❌ Error seeding database: {e}", exc_info=True)
        sys.exit(1)
