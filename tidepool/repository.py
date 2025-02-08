"""tidepool/repository.py"""
# ruff: noqa: D105

from typing import Generator, Iterator
from importlib import import_module

from tidepool import Item, settings
from tidepool.services import DBService, StorageService


class TidepoolRepository:
    def __init__(self) -> None:
        self.name = settings.REPOSITORY_NAME
        self.settings = settings
        self.db = DBService()
        self.storage = self.load_storage_service()

    def __repr__(self) -> str:
        return f"<TidepoolRepository: {self.name}>"

    def load_storage_service(self) -> StorageService:
        storage_module, storage_classname = settings.PRIMARY_STORAGE_SERVICE
        storage_class = getattr(import_module(storage_module), storage_classname)
        return storage_class()

    def save_item(self, item: Item, *, commit: bool = True) -> Item:
        # save item to DB
        item = self.db.save_item(item, commit=False)

        # save files to DB
        for file in item.files:
            file.item_uuid = item.item_uuid
            saved_file = self.db.save_file(file, commit=False)

            # save files to storage
            self.storage.store_file(saved_file)
            for replication_service in self.storage.replication_services:
                replication_service.store_file(saved_file)

        if commit:
            self.db.session.commit()
        else:
            self.db.session.flush()

        return self.db.get_item(item.item_uuid)

    def bulk_save_items(
        self, items: Iterator[Item], yield_items=True, batch_size=1_000
    ) -> Generator[Item]:
        for i, item in enumerate(items):
            saved_item = self.save_item(item, commit=False)
            if i > 0 and i % batch_size == 0:
                self.db.session.commit()
            yield saved_item
        self.db.session.commit()
