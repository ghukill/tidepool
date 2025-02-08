"""tidepool/repository.py"""

from tidepool import settings
from tidepool.services import DBService, StorageService


class TidepoolRepository:
    def __init__(self):
        self.name = settings.REPOSITORY_NAME
        self.settings = settings
        self.db = DBService()
        self.storage = StorageService()

    def __repr__(self):
        return f"<TidepoolRepository: {self.name}>"

    def save(self, item):
        """
        TODO: create or update item in SQL database via self.db
        TODO: save files via self.storage
        """
