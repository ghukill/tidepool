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
    def __init__(
        self,
        config: dict,
        *,
        replication: bool = False,
    ):
        self.config = config
        if not replication:
            self.replication_services: list["StorageService"] = (
                self.load_replication_storage_services()
            )

    def load_replication_storage_services(self):
        replication_services = []
        for storage_service_config in settings.REPLICATION_STORAGE_SERVICES:
            storage_service = getattr(
                import_module(storage_service_config["module"]),
                storage_service_config["class"],
            )
            replication_services.append(
                storage_service(
                    config=storage_service_config["config"],
                    replication=True,
                )
            )
        return replication_services

    @property
    def name(self):
        return self.config["NAME"]

    @abstractmethod
    def store_file(
        self,
        file: File,
    ) -> str | None: ...

    @abstractmethod
    def delete_file(
        self,
        file: File,
    ) -> bool: ...


class POSIXStorageService(StorageService):
    def __init__(self, config: dict, *, replication: bool = False) -> None:
        super().__init__(config, replication=replication)
        self.data_dir = os.path.expandvars(self.config["DATA_DIR"])
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

    def store_file(
        self,
        file: File,
    ) -> str | None:
        file_dir = Path(self.data_dir) / str(file.item_uuid)
        file_dir.mkdir(parents=True, exist_ok=True)

        file_path = file_dir / f"{file.file_uuid}_{file.filename}"
        if file.data:
            with open(file_path, "wb") as f:
                f.write(file.data)
        elif file.filepath:
            shutil.copy(file.filepath, file_path)
        else:
            return None
        return str(file_path)

    def delete_file(
        self,
        file: File,
    ) -> bool:
        file_dir = Path(self.data_dir) / str(file.item_uuid)
        file_path = file_dir / f"{file.file_uuid}_{file.filename}"
        try:
            os.remove(file_path)
            logger.debug(f"removed item file: {file_path}")
        except Exception as e:
            logger.debug(f"error deleting object '{file_path}': {e}")
            return False

        if not os.listdir(file_dir):
            os.rmdir(file_dir)
            logger.debug(f"removed item files directory: {file_dir}")

        return True


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

    def store_file(
        self,
        file: File,
    ) -> str | None:
        s3client = self.get_s3_client()
        s3_key = f"{file.item_uuid}/{file.file_uuid}_{file.filename}"

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
        s3_key = f"{file.item_uuid}/{file.file_uuid}_{file.filename}"
        s3client.delete(s3_key)
        return True


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
