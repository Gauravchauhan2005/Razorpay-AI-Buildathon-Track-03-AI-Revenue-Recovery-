"""Configuration settings for the application."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings class using pydantic for validation."""
    razorpay_key_id: str = ''
    razorpay_key_secret: str = ''
    razorpay_webhook_secret: str = ''
    database_url: str = 'sqlite:///./payment_recovery.db'
    openai_api_key: str = ''
    max_recovery_attempts: int = 3
    app_name: str = 'Payment Recovery Agent'
    debug: bool = True

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()
