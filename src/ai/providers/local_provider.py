"""Local LLM provider (LM Studio, Ollama, etc.)."""

import aiohttp
from typing import Optional

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class LocalLLMProvider:
    """Provider for local LLM APIs (LM Studio, Ollama)."""

    def __init__(self, base_url: str = "http://localhost:1234/v1"):
        """
        Initialize local LLM provider.

        Args:
            base_url: Base URL for local LLM API
        """
        self.base_url = base_url.rstrip("/")

    async def chat(
        self, prompt: str, model: str = "local-model", temperature: float = 0.3
    ) -> str:
        """
        Send chat completion request to local LLM.

        Args:
            prompt: User prompt
            model: Model name
            temperature: Sampling temperature

        Returns:
            Model response text
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature,
                    },
                ) as response:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"Local LLM error: {e}", exc_info=True)
            raise

    async def is_available(self) -> bool:
        """Check if local LLM is available."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/models", timeout=5) as response:
                    return response.status == 200
        except Exception:
            return False
