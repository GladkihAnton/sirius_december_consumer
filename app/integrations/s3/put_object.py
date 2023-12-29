import io
from datetime import timedelta

from PIL.Image import Image

from app.integrations.s3.client import client
from conf.config import settings


async def put_object(task_id: str, img: Image):
    with io.BytesIO() as buffer:
        img.save(buffer, format='png')
        buffer.seek(0)

        await client.put_object(settings.S3_BUCKET, task_id, buffer, buffer.getbuffer().nbytes)


def get_presigned_url(task_id: str) -> str:
    return f'http://localhost:9000/{settings.S3_BUCKET}/{task_id}'
