from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class RabbitMQSettings(BaseModel):
    host: str
    port: int
    login: str
    password: str
    pika_publish_queue_name: str
    pika_consumer_queue_name: str


# class RedisSettings(BaseModel):
#     db_session: int
#     host: str
#     port: int
#     password: SecretStr
#     device_command_public_keys_var: str


class Settings(BaseSettings):
    debug: bool = False

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )

    environment: str = "local"
    log_level: str = "INFO"

    jwt_algorithm: str
    secret_key: str
    thread_pool_workers: int
    cors_origins: str = ""
    base_url: str = "http://localhost:8000"

    # rabbit: RabbitMQSettings
    # redis: RedisSettings


settings = Settings()
