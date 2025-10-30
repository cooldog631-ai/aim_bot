"""Add admin user to the system."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.repositories.employee_repo import EmployeeRepository
from src.database.session import get_db, init_db
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


async def add_admin(messenger_id: str, full_name: str, username: str = None):
    """
    Add admin user.

    Args:
        messenger_id: Messenger ID (Telegram user ID)
        full_name: Full name
        username: Optional username
    """
    await init_db()

    async with get_db() as db:
        repo = EmployeeRepository(db)

        # Create or get employee
        employee = await repo.get_or_create(
            messenger_id=messenger_id, full_name=full_name, messenger_username=username
        )

        # Update permissions
        if employee.permission:
            employee.permission.is_admin = True
            employee.permission.can_submit_reports = True
            employee.permission.can_request_reports = True
            employee.permission.can_edit_reports = True
            employee.permission.can_export_data = True
        else:
            from src.database.models.permission import Permission

            permission = Permission(
                employee_id=employee.id,
                is_admin=True,
                can_submit_reports=True,
                can_request_reports=True,
                can_edit_reports=True,
                can_export_data=True,
            )
            db.add(permission)

        logger.info(f"✅ Admin user created/updated: {full_name} ({messenger_id})")


async def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Add admin user")
    parser.add_argument("messenger_id", help="Messenger ID (Telegram user ID)")
    parser.add_argument("full_name", help="Full name")
    parser.add_argument("--username", help="Optional username", default=None)

    args = parser.parse_args()

    await add_admin(args.messenger_id, args.full_name, args.username)


if __name__ == "__main__":
    asyncio.run(main())
