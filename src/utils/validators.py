"""Data validators."""

import re
from datetime import datetime
from typing import Optional


def validate_date(date_str: str) -> bool:
    """
    Validate date string.

    Args:
        date_str: Date string to validate

    Returns:
        True if valid, False otherwise
    """
    # Try DD.MM.YYYY format
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        pass

    # Try YYYY-MM-DD format
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        pass

    return False


def validate_equipment_number(equipment_number: str) -> bool:
    """
    Validate equipment number.

    Args:
        equipment_number: Equipment number to validate

    Returns:
        True if valid, False otherwise
    """
    if not equipment_number or len(equipment_number) < 1:
        return False

    # Basic validation - can be extended with specific rules
    return len(equipment_number) <= 100


def validate_brigade_number(brigade_number: str) -> bool:
    """
    Validate brigade number.

    Args:
        brigade_number: Brigade number to validate

    Returns:
        True if valid, False otherwise
    """
    if not brigade_number or len(brigade_number) < 1:
        return False

    # Basic validation - can be extended with specific rules
    return len(brigade_number) <= 100


def validate_messenger_id(messenger_id: str) -> bool:
    """
    Validate messenger ID.

    Args:
        messenger_id: Messenger ID to validate

    Returns:
        True if valid, False otherwise
    """
    # Telegram user IDs are numeric
    return messenger_id.isdigit()


def sanitize_text(text: str) -> str:
    """
    Sanitize text input.

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text
    """
    # Remove dangerous characters
    text = re.sub(r"[<>\"']", "", text)

    # Trim whitespace
    text = text.strip()

    return text
