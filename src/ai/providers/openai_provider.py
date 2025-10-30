"""OpenAI API provider for LLM and Whisper."""

import io
from typing import Optional, Union

from openai import AsyncOpenAI

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class OpenAIProvider:
    """OpenAI API provider."""

    def __init__(self, api_key: str):
        """Initialize OpenAI client."""
        self.client = AsyncOpenAI(api_key=api_key)

    async def chat(
        self, prompt: str, model: str = "gpt-4", temperature: float = 0.3
    ) -> str:
        """
        Send chat completion request.

        Args:
            prompt: User prompt
            model: Model name (gpt-4, gpt-3.5-turbo, etc.)
            temperature: Sampling temperature

        Returns:
            Model response text
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI chat error: {e}", exc_info=True)
            raise

    async def transcribe(
        self,
        audio_file: Union[io.BytesIO, bytes],
        language: str = "ru",
        model: str = "whisper-1",
    ) -> str:
        """
        Transcribe audio using Whisper API.

        Args:
            audio_file: Audio file (BytesIO or bytes)
            language: Language code (e.g., 'ru', 'en')
            model: Whisper model name

        Returns:
            Transcribed text
        """
        try:
            # Ensure we have BytesIO with a name
            if isinstance(audio_file, bytes):
                buffer = io.BytesIO(audio_file)
                buffer.name = "audio.ogg"
            else:
                buffer = audio_file
                if not hasattr(buffer, "name"):
                    buffer.name = "audio.ogg"

            response = await self.client.audio.transcriptions.create(
                model=model, file=buffer, language=language
            )

            return response.text

        except Exception as e:
            logger.error(f"OpenAI transcription error: {e}", exc_info=True)
            raise
