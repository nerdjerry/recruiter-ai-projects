from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    plaid_client_id: str = ""
    plaid_secret: str = ""
    plaid_env: str = "sandbox"
    mem0_api_key: str = ""
    chat_model: str = "gpt-4o"
    db_path: str = "./data/transactions.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
