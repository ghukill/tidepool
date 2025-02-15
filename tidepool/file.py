"""tidepool/file.py"""

import datetime
import json
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from tidepool.settings.manager import settings

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

    @property
    def api_uri(self):
        return (
            f"{settings.API_BASE_URI}/api/items/{self.item_uuid}/files/{self.file_uuid}"
        )

    def to_dict(self):
        return {
            "file_uuid": str(self.file_uuid),
            "api_uri": self.api_uri,
            "data_uri": f"{self.api_uri}/data",
            "filename": str(self.filename),
            "mimetype": str(self.mimetype),
            "date_created": self.date_created.isoformat() if self.date_created else None,
            "date_updated": self.date_updated.isoformat() if self.date_updated else None,
        }

    def to_json(self, indent=None):
        return json.dumps(self.to_dict(), indent=indent)
