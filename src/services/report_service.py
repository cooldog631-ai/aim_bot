"""Report service for business logic."""

from datetime import date, datetime
from typing import Dict, List, Optional

from src.ai.transcription import transcribe_audio
from src.ai.validation import (
    generate_clarification_questions,
    merge_partial_data,
    validate_report,
)
from src.database.repositories.employee_repo import EmployeeRepository
from src.database.repositories.report_repo import ReportRepository
from src.database.session import get_db
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ReportService:
    """Service for report processing and management."""

    async def process_voice_message(self, user_id: str, voice_data: bytes) -> Dict:
        """
        Process voice message and extract report data.

        Args:
            user_id: Messenger user ID
            voice_data: Voice message audio data

        Returns:
            Dictionary with processing result
        """
        try:
            # Transcribe audio
            logger.info(f"Transcribing voice message from user {user_id}")
            transcription = await transcribe_audio(voice_data)

            # Validate and extract data
            logger.info(f"Validating transcription for user {user_id}")
            validation_result = await validate_report(transcription)

            if validation_result.get("complete"):
                return {
                    "status": "complete",
                    "data": validation_result["extracted_data"],
                    "transcription": transcription,
                }
            else:
                # Generate clarification questions
                missing_fields = validation_result.get("missing_fields", [])
                questions = await generate_clarification_questions(missing_fields)

                return {
                    "status": "incomplete",
                    "data": validation_result.get("extracted_data", {}),
                    "missing_fields": missing_fields,
                    "questions": questions,
                    "transcription": transcription,
                }

        except Exception as e:
            logger.error(f"Error processing voice message: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}

    async def process_clarification(
        self, user_id: str, clarification_data: str, partial_data: Dict, is_voice: bool = False
    ) -> Dict:
        """
        Process clarification message (voice or text).

        Args:
            user_id: Messenger user ID
            clarification_data: Clarification text or voice data
            partial_data: Existing partial report data
            is_voice: Whether clarification is voice message

        Returns:
            Dictionary with processing result
        """
        try:
            # Transcribe if voice
            if is_voice:
                transcription = await transcribe_audio(clarification_data)
            else:
                transcription = clarification_data

            # Merge with partial data
            merge_result = await merge_partial_data(partial_data, transcription)

            if merge_result.get("complete"):
                return {
                    "status": "complete",
                    "data": merge_result["merged_data"],
                }
            else:
                missing_fields = merge_result.get("missing_fields", [])
                questions = await generate_clarification_questions(missing_fields)

                return {
                    "status": "incomplete",
                    "data": merge_result.get("merged_data", {}),
                    "missing_fields": missing_fields,
                    "questions": questions,
                }

        except Exception as e:
            logger.error(f"Error processing clarification: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}

    async def save_report(self, user_id: str, report_data: Dict) -> bool:
        """
        Save confirmed report to database.

        Args:
            user_id: Messenger user ID
            report_data: Validated report data

        Returns:
            True if successful, False otherwise
        """
        try:
            async with get_db() as db:
                # Get or create employee
                employee_repo = EmployeeRepository(db)
                employee = await employee_repo.get_by_messenger_id(user_id)

                if not employee:
                    logger.warning(f"Employee not found for user {user_id}, creating...")
                    employee = await employee_repo.create(
                        messenger_id=user_id, full_name="Unknown User"
                    )

                # Parse report data
                report_date_str = report_data.get("date", "")
                report_date = self._parse_date(report_date_str)

                # Save report
                report_repo = ReportRepository(db)
                await report_repo.create(
                    employee_id=employee.id,
                    report_date=report_date,
                    equipment_number=report_data.get("equipment_number", ""),
                    brigade_number=report_data.get("brigade_number", ""),
                    work_description=report_data.get("work_description", ""),
                    structured_data=report_data,
                )

                logger.info(f"Report saved for user {user_id}")
                return True

        except Exception as e:
            logger.error(f"Error saving report: {e}", exc_info=True)
            return False

    async def get_user_reports(
        self, user_id: str, start_date: date, end_date: date
    ) -> List:
        """
        Get reports for user within date range.

        Args:
            user_id: Messenger user ID
            start_date: Start date
            end_date: End date

        Returns:
            List of reports
        """
        try:
            async with get_db() as db:
                employee_repo = EmployeeRepository(db)
                employee = await employee_repo.get_by_messenger_id(user_id)

                if not employee:
                    return []

                report_repo = ReportRepository(db)
                reports = await report_repo.get_user_reports(employee.id, start_date, end_date)
                return reports

        except Exception as e:
            logger.error(f"Error getting user reports: {e}", exc_info=True)
            return []

    async def get_last_user_report(self, user_id: str) -> Optional:
        """
        Get last report for user.

        Args:
            user_id: Messenger user ID

        Returns:
            Last report or None
        """
        try:
            async with get_db() as db:
                employee_repo = EmployeeRepository(db)
                employee = await employee_repo.get_by_messenger_id(user_id)

                if not employee:
                    return None

                report_repo = ReportRepository(db)
                return await report_repo.get_last_user_report(employee.id)

        except Exception as e:
            logger.error(f"Error getting last user report: {e}", exc_info=True)
            return None

    def _parse_date(self, date_str: str) -> date:
        """Parse date string to date object."""
        try:
            # Try DD.MM.YYYY format
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            try:
                # Try YYYY-MM-DD format
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                # Default to today
                logger.warning(f"Could not parse date '{date_str}', using today")
                return date.today()
