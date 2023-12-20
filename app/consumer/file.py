import asyncio
import logging
import msgpack

from aiokafka.consumer import AIOKafkaConsumer

from app.record.parser import parse_consumer_record
from conf.config import settings


async def main():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_CONSUMER_GROUP,
        enable_auto_commit=False,
        auto_offset_reset='earliest',
    )
    await consumer.start()

    async for record in consumer:
        try:
            parsed_record = parse_consumer_record(record)

            logging.debug("Task_id: %s, ", parsed_record['value']['task_id'])


        finally:
            pass
            # await consumer.commit()


if __name__ == '__main__':
    asyncio.run(main())