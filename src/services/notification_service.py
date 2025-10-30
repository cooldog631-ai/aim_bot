"""Notification service for reminders and alerts."""

from datetime import date

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class NotificationService:
    """Service for sending notifications and reminders."""

    async def send_report_reminder(self, employee_id: int, messenger_id: str):
        """
        Send reminder to submit daily report.

        Args:
            employee_id: Employee database ID
            messenger_id: Messenger user ID
        """
        # TODO: Implement reminder sending via bot
        logger.info(f"Sending report reminder to employee {employee_id} ({messenger_id})")

    async def check_missing_reports(self, check_date: date = None):
        """
        Check for employees who haven't submitted reports.

        Args:
            check_date: Date to check (default: today)
        """
        if check_date is None:
            check_date = date.today()

        # TODO: Implement missing reports check
        logger.info(f"Checking for missing reports on {check_date}")

    async def send_admin_alert(self, message: str):
        """
        Send alert to administrators.

        Args:
            message: Alert message
        """
        # TODO: Implement admin alerts
        logger.warning(f"Admin alert: {message}")
