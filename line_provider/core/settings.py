from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class RabbitMQSettings(BaseModel):
    host: str
    port: int
    login: str
    password: str
    pika_publish_queue_name: str


class Settings(BaseSettings):
    debug: bool = False

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )

    environment: str = "local"
    log_level: str = "INFO"

    cors_origins: str = ""
    base_url: str = "http://localhost:8000"

    rabbit: RabbitMQSettings


settings = Settings()
