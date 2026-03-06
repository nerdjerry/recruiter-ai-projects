"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    gmail_credentials_path: str = "./credentials/token.json"
    chat_model: str = "gpt-4o"
    max_emails_per_run: int = 20
    human_in_the_loop: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
