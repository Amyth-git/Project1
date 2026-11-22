from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "project1"
    app_env: str = "development"
    app_port: int = 8000
    log_level: str = "INFO"
    api_key: str = "change-me-in-production"


settings = Settings()
