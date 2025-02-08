"""tidepool/services/storage.py"""

from importlib import import_module
import io
import logging
import os
import shutil
from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from botocore.response import StreamingBody

from tidepool import File, settings

if TYPE_CHECKING:
    from botocore.client import BaseClient

logger = logging.getLogger(__name__)


class StorageService:
    def __init__(self, *, replication: bool = False):
        if not replication:
            self.replication_services: list["StorageService"] = (
                self.load_replication_storage_services()
            )

    def load_replication_storage_services(self):
        return [
            getattr(import_module(storage_module), storage_classname)(replication=True)
            for storage_module, storage_classname in settings.REPLICATION_STORAGE_SERVICES
        ]

    @abstractmethod
    def store_file(
        self,
        file: File,
    ) -> str: ...


class POSIXStorageService(StorageService):
    def __init__(self, *, replication: bool = False) -> None:
        super().__init__(replication=replication)
        self.data_dir = os.path.expandvars(settings.POSIX_STORAGE["DATA_DIR"])
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

    def store_file(
        self,
        file: File,
    ) -> str:
        dest_dir = Path(self.data_dir) / str(file.item_uuid)
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_path = dest_dir / f"{file.file_uuid}_{file.filename}"
        if file.data:
            with open(dest_path, "wb") as f:
                f.write(file.data)
        elif file.filepath:
            shutil.copy(file.filepath, dest_path)
        else:
            raise ValueError("file data or filepath must be passed")
        return str(dest_path)


class MinioStorageService(StorageService):
    def __init__(self, *, replication: bool = False):
        super().__init__(replication=replication)

    def store_file(
        self,
        file: File,
    ) -> str:
        s3client = S3Client()
        s3_key = f"{file.item_uuid}/{file.file_uuid}_{file.filename}"

        if file.data:
            data = file.data
        elif file.filepath:
            # TODO: improve with streaming
            with open(file.filepath, "rb") as f:
                data = f.read()
        else:
            raise ValueError("file data or filepath must be passed")

        return s3client.upload(s3_key, data)


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
            logger.debug(f"Error reading object '{key}': {error}")
            raise

    def read_stream(self, key: str) -> StreamingBody:
        """Read an object from the S3 bucket and return a streaming object."""
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=key)
            stream: StreamingBody = response["Body"]
            return stream
        except (BotoCoreError, ClientError) as error:
            logger.debug(f"Error reading object '{key}' as stream: {error}")
            raise
