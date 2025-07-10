from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
    )
    API_V1_STR: str = "/api/v1"
    OPENAI_API_KEY: str = ""

    LANGSMITH_TRACING: bool
    LANGSMITH_API_KEY: str


settings = Settings()