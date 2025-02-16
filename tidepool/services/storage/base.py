"""tidepool/services/storage/base.py"""

import logging
from abc import abstractmethod
from importlib import import_module

from tidepool import File
from tidepool.settings.manager import settings


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

    @abstractmethod
    def read_file(
        self,
        file: File,
    ) -> bytes: ...
