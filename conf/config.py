from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str

    KAFKA_CONSUMER_GROUP: str
    KAFKA_BOOTSTRAP_SERVERS: List[str]
    KAFKA_TOPIC: str


settings = Settings()
