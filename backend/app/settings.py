from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Kenyan CBE Assessment Management System"
    app_env: str = "development"
    secret_key: str = "development-only-change-me"
    jwt_secret_key: str = "development-only-change-me-too"
    database_url: str = "postgresql+asyncpg://cbe:change-me-local-only@localhost:5432/cbe_assessment"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: str = "http://localhost:3000"
    paystack_secret_key: str = ""
    paystack_public_key: str = ""
    paystack_webhook_secret: str = ""


settings = Settings()
