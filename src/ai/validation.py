"""Report validation using LLM."""

import json
from typing import Dict, List, Optional

from src.ai.prompts import (
    CLARIFICATION_PROMPT,
    CONFIRMATION_PROMPT,
    MERGE_DATA_PROMPT,
    VALIDATION_PROMPT,
)
from src.ai.providers.anthropic_provider import AnthropicProvider
from src.ai.providers.openai_provider import OpenAIProvider
from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


async def validate_report(transcription: str) -> Dict:
    """
    Validate report transcription and extract structured data.

    Args:
        transcription: Text transcription of voice message

    Returns:
        Dictionary with validation results:
        {
            "complete": bool,
            "missing_fields": List[str],
            "extracted_data": Dict
        }
    """
    settings = get_settings()

    prompt = VALIDATION_PROMPT.format(transcription=transcription)

    try:
        # Get LLM response
        response = await _get_llm_response(prompt)

        # Parse JSON response
        result = json.loads(response)

        logger.info(f"Validation result: complete={result.get('complete')}")
        return result

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response as JSON: {e}")
        logger.error(f"Response was: {response}")
        return {
            "complete": False,
            "missing_fields": ["all"],
            "extracted_data": {},
            "error": "Failed to parse validation response",
        }
    except Exception as e:
        logger.error(f"Validation error: {e}", exc_info=True)
        return {
            "complete": False,
            "missing_fields": ["all"],
            "extracted_data": {},
            "error": str(e),
        }


async def generate_clarification_questions(missing_fields: List[str]) -> str:
    """
    Generate friendly clarification questions for missing fields.

    Args:
        missing_fields: List of missing field names

    Returns:
        Friendly message asking for missing information
    """
    prompt = CLARIFICATION_PROMPT.format(missing_fields=", ".join(missing_fields))

    try:
        response = await _get_llm_response(prompt)
        return response.strip()
    except Exception as e:
        logger.error(f"Error generating questions: {e}", exc_info=True)
        # Fallback message
        return f"Пожалуйста, уточни: {', '.join(missing_fields)}"


async def format_report_for_confirmation(report_data: Dict) -> str:
    """
    Format report data for user confirmation.

    Args:
        report_data: Structured report data

    Returns:
        Formatted report text
    """
    prompt = CONFIRMATION_PROMPT.format(report_data=json.dumps(report_data, ensure_ascii=False))

    try:
        response = await _get_llm_response(prompt)
        return response.strip()
    except Exception as e:
        logger.error(f"Error formatting report: {e}", exc_info=True)
        # Fallback formatting
        return f"""
📅 Дата: {report_data.get('date', 'N/A')}
🚜 Техника: {report_data.get('equipment_number', 'N/A')}
👷 Бригада: {report_data.get('brigade_number', 'N/A')}
📝 Работы: {report_data.get('work_description', 'N/A')}
""".strip()


async def merge_partial_data(partial_data: Dict, new_transcription: str) -> Dict:
    """
    Merge partial report data with new information.

    Args:
        partial_data: Existing partial report data
        new_transcription: New transcription to extract data from

    Returns:
        Merged validation result
    """
    prompt = MERGE_DATA_PROMPT.format(
        partial_data=json.dumps(partial_data, ensure_ascii=False),
        new_info=new_transcription,
    )

    try:
        response = await _get_llm_response(prompt)
        result = json.loads(response)
        return result
    except Exception as e:
        logger.error(f"Error merging data: {e}", exc_info=True)
        return {
            "complete": False,
            "missing_fields": ["all"],
            "merged_data": partial_data,
            "error": str(e),
        }


async def _get_llm_response(prompt: str) -> str:
    """Get response from configured LLM provider."""
    settings = get_settings()

    if settings.llm_provider == "openai":
        provider = OpenAIProvider(api_key=settings.openai_api_key)
        return await provider.chat(prompt, model=settings.llm_model)

    elif settings.llm_provider == "anthropic":
        provider = AnthropicProvider(api_key=settings.anthropic_api_key)
        return await provider.chat(prompt, model=settings.llm_model)

    else:
        # TODO: Implement local LLM provider
        raise NotImplementedError(f"Provider {settings.llm_provider} not implemented yet")
