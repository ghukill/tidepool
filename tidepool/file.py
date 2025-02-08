"""tidepool/file.py"""

import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from tidepool import Item


class File:
    def __init__(
        self,
        filename: str,
        mimetype: str,
        file_uuid: str | None = None,
        item_uuid: str | None = None,
        data: bytes | str | None = None,
        filepath: str | Path | None = None,
        date_created: datetime.datetime | None = None,
        date_updated: datetime.datetime | None = None,
        item: Optional["Item"] = None,
    ):
        self.file_uuid = file_uuid
        self.item_uuid = item_uuid
        self.filename = filename
        self.mimetype = mimetype
        self.data = data
        self.filepath = filepath
        self.date_created = date_created
        self.date_updated = date_updated
        self.item = item
