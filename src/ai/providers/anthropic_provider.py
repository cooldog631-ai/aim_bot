"""Anthropic Claude API provider."""

from typing import Optional

from anthropic import AsyncAnthropic

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class AnthropicProvider:
    """Anthropic Claude API provider."""

    def __init__(self, api_key: str):
        """Initialize Anthropic client."""
        self.client = AsyncAnthropic(api_key=api_key)

    async def chat(
        self,
        prompt: str,
        model: str = "claude-3-sonnet-20240229",
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> str:
        """
        Send chat message to Claude.

        Args:
            prompt: User prompt
            model: Model name (claude-3-opus, claude-3-sonnet, etc.)
            temperature: Sampling temperature
            max_tokens: Maximum response tokens

        Returns:
            Model response text
        """
        try:
            response = await self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Anthropic chat error: {e}", exc_info=True)
            raise
