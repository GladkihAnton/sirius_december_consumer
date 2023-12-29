from datetime import timedelta
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str

    KAFKA_CONSUMER_GROUP: str
    KAFKA_BOOTSTRAP_SERVERS: List[str]
    KAFKA_TOPIC: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_SIRIUS_CACHE_PREFIX: str = 'sirius'

    S3_BUCKET: str = 'file-resize'
    FILE_EXPIRE_TIME: timedelta = timedelta(minutes=15)


settings = Settings()
