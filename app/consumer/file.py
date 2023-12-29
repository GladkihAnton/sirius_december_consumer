import asyncio
import io

import orjson
from PIL import Image

from aiokafka.consumer import AIOKafkaConsumer
from sqlalchemy import insert
#from sqlalchemy.dialects.postgresql import insert


from app.integrations.cache.key_builder import get_file_resize_cache
from app.integrations.cache.redis import get_redis
from app.integrations.postgres import async_session_maker
from app.integrations.s3.put_object import put_object, get_presigned_url
from app.logger import logger
from app.models.sirius.file import File
from app.models.sirius.user_file import UserFile
from app.on_startup.main import on_startup
from app.record.parser import parse_consumer_record
from conf.config import settings
#
#
async def main():
    await on_startup()
    logger.debug('After start up')
#
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_CONSUMER_GROUP,
        enable_auto_commit=False,
        auto_offset_reset='earliest',
    )
    await consumer.start()

    logger.error('Consumer started')
    async for record in consumer:
        try:
            parsed_record = parse_consumer_record(record)
            task_id = parsed_record['value']['task_id']
            user_id = parsed_record['value']['user_id']

            logger.error('New message with. Task_id: %s', task_id)

            with io.BytesIO() as buffer:
                buffer.write(parsed_record['value']['image'])
                buffer.seek(0)

                image = Image.open(buffer)
                logger.error('Start resizing image. Task_id: %s', task_id)
                resized_image = image.resize((parsed_record['value']['width'], parsed_record['value']['height']))

            await put_object(task_id, resized_image)
            logger.error('Put image. Task_id: %s', task_id)

            url = get_presigned_url(task_id)

            redis = get_redis()
            await redis.set(
                get_file_resize_cache(task_id),
                orjson.dumps({'url': url}),
                ex=settings.FILE_EXPIRE_TIME,
            )

            async with async_session_maker() as session:
                file_id = (
                    await session.scalars(
                        insert(File)
                        .values({
                            'url': url,
                            'task_id': task_id,
                        })
                        # .on_conflict_do_nothing()
                        .returning(File.id)
                    )
                ).one_or_none()


                await session.execute(
                    insert(UserFile)
                    .values({
                        'user_id': user_id,
                        'file_id': file_id,
                    })
                )
                await session.commit()

            logger.error('Set to redis. Task_id: %s', task_id)
        except Exception:
            logger.exception('ASDASD')
        finally:
            await consumer.commit()

    await consumer.stop()


if __name__ == '__main__':
    asyncio.run(main())