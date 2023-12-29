from miniopy_async import Minio

client = Minio(
    "minio:9000",
    access_key="MINIO_LOGIN",
    secret_key="MINIO_PASS",
    secure=False,
)
