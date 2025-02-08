"""tidepool/services/storage.py"""

import io
from typing import BinaryIO

import boto3
from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError, ClientError
from botocore.response import StreamingBody

from tidepool import settings


class StorageService:
    pass


class S3Client:
    def __init__(
        self,
        bucket: str = settings.S3_STORAGE["BUCKET"],
        region_name: str = settings.S3_STORAGE["REGION"],
        endpoint_url: str = settings.S3_STORAGE["ENDPOINT"],
        aws_access_key_id: str = settings.S3_STORAGE["ACCESS_KEY_ID"],
        aws_secret_access_key: str = settings.S3_STORAGE["SECRET_ACCESS_KEY"],
    ) -> None:
        """Initialize the S3 client."""
        self.bucket: str = bucket
        self.s3: BaseClient = boto3.client(
            "s3",
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def upload(
        self,
        key: str,
        data: bytes | BinaryIO,
        mimetype: str = "application/octet-stream",
    ) -> str:
        """Upload data to the S3 bucket."""
        if isinstance(data, bytes):
            file_obj: BinaryIO = io.BytesIO(data)
        elif hasattr(data, "read"):
            file_obj = data  # type: ignore
        else:
            raise ValueError("Data must be a bytes object or a file-like object.")

        try:
            self.s3.upload_fileobj(
                Fileobj=file_obj,
                Bucket=self.bucket,
                Key=key,
                ExtraArgs={"ContentType": mimetype},
            )
            print(f"Successfully uploaded object '{key}' to bucket '{self.bucket}'.")
            return f"s3://{self.bucket}/{key}"

        except (BotoCoreError, ClientError) as error:
            print(f"Error uploading object: {error}")
            raise

    def read(self, key: str) -> bytes:
        """Read an object from the S3 bucket and return its contents as bytes."""
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=key)
            data: bytes = response["Body"].read()
            return data
        except (BotoCoreError, ClientError) as error:
            print(f"Error reading object '{key}': {error}")
            raise

    def read_stream(self, key: str) -> StreamingBody:
        """Read an object from the S3 bucket and return a streaming object."""
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=key)
            stream: StreamingBody = response["Body"]
            return stream
        except (BotoCoreError, ClientError) as error:
            print(f"Error reading object '{key}' as stream: {error}")
            raise
