"""tidepool/repository.py"""
# ruff: noqa: D105

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

        # save files to DB and storage
        for file in item.files:
            file.item_uuid = item.item_uuid
            saved_file = self.db.save_file(file, commit=False)
            self.storage.store_file(saved_file)

        if commit:
            self.db.session.commit()
        else:
            self.db.session.flush()

        return self.db.get_item(item.item_uuid)
