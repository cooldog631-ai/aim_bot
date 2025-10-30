"""Configuration management for the bot."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Bot Configuration
    messenger_type: Literal["telegram", "vkmax", "both"] = Field(
        default="telegram", description="Which messenger to use (telegram, vkmax, or both)"
    )
    telegram_bot_token: str = Field(default="", description="Telegram Bot API token")
    vk_bot_token: str = Field(default="", description="VK Bot API token (classic VK)")
    vk_max_token: str = Field(default="", description="VK Max Bot API token")

    # AI Services
    openai_api_key: str = Field(default="", description="OpenAI API key")
    anthropic_api_key: str = Field(default="", description="Anthropic API key")

    # Whisper Configuration
    whisper_model: Literal["tiny", "base", "small", "medium", "large"] = Field(
        default="base", description="Whisper model size"
    )
    use_local_whisper: bool = Field(
        default=False, description="Use local Whisper model instead of API"
    )

    # LLM Configuration
    llm_provider: Literal["openai", "anthropic", "local"] = Field(
        default="openai", description="LLM provider to use"
    )
    llm_model: str = Field(
        default="gpt-4", description="LLM model name (gpt-4, gpt-3.5-turbo, claude-3-sonnet, etc.)"
    )
    local_llm_url: str = Field(
        default="http://localhost:1234/v1", description="Local LLM API URL (LM Studio)"
    )

    # Database
    database_url: str = Field(
        default="sqlite:///./aim_bot.db", description="Database connection URL"
    )

    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=True, description="Debug mode")

    # Session
    session_timeout: int = Field(default=3600, description="Session timeout in seconds (1 hour)")

    # Reports
    report_reminder_time: str = Field(
        default="18:00", description="Time to send report reminders (HH:MM)"
    )
    required_fields: str = Field(
        default="date,equipment_number,brigade_number,work_description",
        description="Comma-separated list of required report fields",
    )

    # Security
    allowed_users: str = Field(
        default="", description="Comma-separated list of allowed messenger IDs (empty = all)"
    )
    admin_users: str = Field(
        default="", description="Comma-separated list of admin messenger IDs"
    )

    @property
    def required_fields_list(self) -> list[str]:
        """Get required fields as a list."""
        return [field.strip() for field in self.required_fields.split(",") if field.strip()]

    @property
    def allowed_users_list(self) -> list[str]:
        """Get allowed users as a list."""
        if not self.allowed_users:
            return []
        return [user.strip() for user in self.allowed_users.split(",") if user.strip()]

    @property
    def admin_users_list(self) -> list[str]:
        """Get admin users as a list."""
        if not self.admin_users:
            return []
        return [user.strip() for user in self.admin_users.split(",") if user.strip()]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
