"""Audio transcription using Whisper."""

import io
from typing import Union

from src.ai.providers.openai_provider import OpenAIProvider
from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


async def transcribe_audio(audio_data: Union[bytes, io.BytesIO]) -> str:
    """
    Transcribe audio to text using Whisper.

    Args:
        audio_data: Audio file data (bytes or BytesIO)

    Returns:
        Transcribed text

    Raises:
        Exception: If transcription fails
    """
    settings = get_settings()

    try:
        if settings.use_local_whisper:
            # TODO: Implement local Whisper transcription
            logger.warning("Local Whisper not implemented yet, falling back to API")
            return await _transcribe_with_api(audio_data)
        else:
            return await _transcribe_with_api(audio_data)

    except Exception as e:
        logger.error(f"Transcription error: {e}", exc_info=True)
        raise


async def _transcribe_with_api(audio_data: Union[bytes, io.BytesIO]) -> str:
    """Transcribe using OpenAI Whisper API."""
    settings = get_settings()

    # Convert bytes to BytesIO if needed
    if isinstance(audio_data, bytes):
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "audio.ogg"  # Telegram voice messages are in OGG format
    else:
        audio_file = audio_data

    provider = OpenAIProvider(api_key=settings.openai_api_key)
    transcription = await provider.transcribe(audio_file, language="ru")

    logger.info(f"Transcription completed: {transcription[:100]}...")
    return transcription


async def _transcribe_local(audio_data: Union[bytes, io.BytesIO]) -> str:
    """Transcribe using local Whisper model."""
    # TODO: Implement local Whisper using faster-whisper or openai-whisper
    raise NotImplementedError("Local Whisper transcription not implemented yet")
