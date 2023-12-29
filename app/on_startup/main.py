from app.on_startup.redis import start_redis


async def on_startup():
    await start_redis()