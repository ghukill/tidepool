"""tidepool/item.py"""

import datetime
import json
from typing import TYPE_CHECKING, Optional

from pyld import jsonld

from tidepool.exceptions import FileNotFound
from tidepool.settings.manager import settings

if TYPE_CHECKING:
    from tidepool import File


class Item:
    def __init__(
        self,
        title: str,
        jsonld_metadata: Optional["ItemMetadata"] = None,
        item_uuid: str | None = None,
        files: list["File"] | None = None,
        date_created: datetime.datetime | None = None,
        date_updated: datetime.datetime | None = None,
    ):
        self.item_uuid = item_uuid
        self.title = title
        self.jsonld_metadata = jsonld_metadata or ItemMetadata()
        self.files = files or []
        self.date_created = date_created
        self.date_updated = date_updated

    @property
    def api_uri(self):
        return f"{settings.API_BASE_URI}/items/{self.item_uuid}"

    def get_file(self, file_uuid: str):
        for file in self.files:
            if str(file.file_uuid) == str(file_uuid):
                return file
        raise FileNotFound

    def to_dict(self):
        return {
            "item_uuid": str(self.item_uuid),
            "api_uri": self.api_uri,
            "title": self.title,
            "jsonld_metadata": self.jsonld_metadata.to_compact(),
            "files": [file.to_dict() for file in self.files],
            "date_created": self.date_created.isoformat() if self.date_created else None,
            "date_updated": self.date_updated.isoformat() if self.date_updated else None,
        }

    def to_json(self, indent=None):
        return json.dumps(self.to_dict(), indent=indent)


class ItemMetadata:
    default_context = {
        "schema": "http://schema.org/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "tidepool": "http://henondesigns.org/tidepool/ontology/",
    }

    def __init__(self, context: dict | None = None):
        self.context = {**self.default_context, **(context or {})}
        self.data = {
            "@context": self.context,
            "@type": "tidepool:DigitalObject",
        }

    def register_namespace(self, prefix: str, iri: str):
        self.context[prefix] = iri

    def set_statement(self, term: str, value: str | dict | list) -> None:
        self.data[term] = value

    def set_id(self, _id: str) -> None:
        self.data["@id"] = _id

    def set_type(self, type_uri: str) -> None:
        self.data["@type"] = type_uri

    def to_compact(self) -> dict:
        return jsonld.compact(self.data, self.context)

    def to_expanded(self) -> list[dict]:
        return jsonld.expand(self.data)

    @classmethod
    def from_jsonld(
        cls, jsonld_data: dict | list, context: dict | None = None
    ) -> "ItemMetadata":
        if isinstance(jsonld_data, list):
            compacted = jsonld.compact(jsonld_data, context or {})
        else:
            compacted = jsonld_data
        metadata = cls(context=compacted.get("@context", {}))
        metadata.data = compacted
        return metadata

    def __str__(self) -> str:
        return json.dumps(self.to_compact(), indent=2)
