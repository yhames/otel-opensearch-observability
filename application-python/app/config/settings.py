from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Application settings
    app_name: str = "FastAPI Application"
    host: str = "127.0.0.1"
    port: int = 8000
    database_url: str = "sqlite:///./test.db"

    # OpenTelemetry settings
    service_name: str = "fastapi-service"
    log_otlp_endpoint: str = "http://localhost:4318/v1/logs"
    metric_otlp_endpoint: str = "http://localhost:4318/v1/metrics"
    tracer_otlp_endpoint: str = "http://localhost:4318/v1/traces"


settings = Settings()


def get_settings():
    return settings
