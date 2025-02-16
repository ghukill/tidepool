"""tidepool/services/storage/posix.py"""

import logging
import os
import shutil
from pathlib import Path

from tidepool import File
from tidepool.services.storage.base import StorageService


logger = logging.getLogger(__name__)


class POSIXStorageService(StorageService):
    def __init__(self, config: dict, *, replication: bool = False) -> None:
        super().__init__(config, replication=replication)
        self.data_dir = os.path.expandvars(self.config["DATA_DIR"])
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

    def get_file_dir_and_path(self, file: File):
        file_dir = Path(self.data_dir) / str(file.item_uuid)
        file_path = file_dir / f"{file.file_uuid}__{file.filename}"
        return file_dir, file_path

    def store_file(
        self,
        file: File,
    ) -> str | None:
        file_dir, file_path = self.get_file_dir_and_path(file)
        file_dir.mkdir(parents=True, exist_ok=True)

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
        file_dir, file_path = self.get_file_dir_and_path(file)
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

    # TODO: add a streaming version
    def read_file(self, file: File):
        file_dir, file_path = self.get_file_dir_and_path(file)
        with open(file_path, "rb") as f:
            return f.read()
