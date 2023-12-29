from redis.asyncio import ConnectionPool, Redis

from app.integrations.cache import redis
from conf.config import settings


async def start_redis() -> None:
    pool = ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
    )
    redis.redis = Redis(
        connection_pool=pool,
    )

