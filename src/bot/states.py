"""FSM (Finite State Machine) states for bot conversations."""

from aiogram.fsm.state import State, StatesGroup


class ReportStates(StatesGroup):
    """States for report submission flow."""

    waiting_for_voice = State()  # Waiting for initial voice message
    waiting_for_clarification = State()  # Waiting for additional info
    waiting_for_confirmation = State()  # Waiting for user confirmation
    waiting_for_correction = State()  # Waiting for corrections


class EditReportStates(StatesGroup):
    """States for report editing flow."""

    selecting_report = State()  # Selecting which report to edit
    editing_field = State()  # Editing a specific field
    confirming_changes = State()  # Confirming edits


class AdminStates(StatesGroup):
    """States for admin operations."""

    adding_user = State()  # Adding new user
    managing_permissions = State()  # Managing user permissions
    viewing_logs = State()  # Viewing system logs
