"""tidepool/services/storage/s3.py"""

import io
import logging
from typing import TYPE_CHECKING, BinaryIO

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from botocore.response import StreamingBody

from tidepool import File
from tidepool.services.storage.base import StorageService

if TYPE_CHECKING:
    from botocore.client import BaseClient

logger = logging.getLogger(__name__)


class S3StorageService(StorageService):
    def __init__(self, config: dict, *, replication: bool = False) -> None:
        super().__init__(config, replication=replication)

    def get_s3_client(self):
        return S3Client(
            self.config["BUCKET"],
            self.config["REGION"],
            self.config["ACCESS_KEY_ID"],
            self.config["SECRET_ACCESS_KEY"],
            endpoint_url=self.config.get("ENDPOINT"),
        )

    def get_s3_key(self, file: File):
        return f"{file.item_uuid}/{file.file_uuid}__{file.filename}"

    def store_file(
        self,
        file: File,
    ) -> str | None:
        s3client = self.get_s3_client()
        s3_key = self.get_s3_key(file)

        if file.data:
            data = file.data
        elif file.filepath:
            # TODO: improve with streaming
            with open(file.filepath, "rb") as f:
                data = f.read()
        else:
            return None

        return s3client.upload(s3_key, data)

    def delete_file(
        self,
        file: File,
    ) -> bool:
        s3client = self.get_s3_client()
        s3_key = self.get_s3_key(file)
        s3client.delete(s3_key)
        return True

    def read_file(
        self,
        file: File,
    ) -> bytes:
        s3client = self.get_s3_client()
        s3_key = self.get_s3_key(file)
        return s3client.read(s3_key)


class S3Client:
    def __init__(
        self,
        bucket: str,
        region_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        endpoint_url: str | None = None,
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
            file_obj = data
        else:
            raise ValueError("Data must be a bytes object or a file-like object.")

        try:
            self.s3.upload_fileobj(
                Fileobj=file_obj,
                Bucket=self.bucket,
                Key=key,
                ExtraArgs={"ContentType": mimetype},
            )
            logger.debug(
                f"Successfully uploaded object '{key}' to bucket '{self.bucket}'."
            )
            return f"s3://{self.bucket}/{key}"

        except (BotoCoreError, ClientError) as error:
            logger.debug(f"Error uploading object: {error}")
            raise

    def read(self, key: str) -> bytes:
        """Read an object from the S3 bucket and return its contents as bytes."""
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=key)
            data: bytes = response["Body"].read()
            return data
        except (BotoCoreError, ClientError) as error:
            logger.debug(f"error reading object '{key}': {error}")
            raise

    def read_stream(self, key: str) -> StreamingBody:
        """Read an object from the S3 bucket and return a streaming object."""
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=key)
            stream: StreamingBody = response["Body"]
            return stream
        except (BotoCoreError, ClientError) as error:
            logger.debug(f"error reading object '{key}' as stream: {error}")
            raise

    def delete(self, key: str) -> None:
        """Delete an object from the S3 bucket."""
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=key)
            logger.debug(f"deleted S3 object '{key}' from bucket '{self.bucket}'.")
        except (BotoCoreError, ClientError) as error:
            logger.debug(f"error deleting object '{key}': {error}")
            raise
