"""tidepool/item.py"""

import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tidepool import File


class Item:
    def __init__(
        self,
        title: str,
        description: str,
        item_uuid: str | None = None,
        files: list["File"] | None = None,
        date_created: datetime.datetime | None = None,
        date_updated: datetime.datetime | None = None,
    ):
        self.item_uuid = item_uuid
        self.title = title
        self.description = description
        self.files = files or []
        self.date_created = date_created
        self.date_updated = date_updated
