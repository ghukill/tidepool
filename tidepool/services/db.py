"""tidepool/services/db.py"""

import logging
import uuid
from typing import Iterator, Optional

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

from tidepool import File, Item, ItemMetadata, settings

logger = logging.getLogger(__name__)

Base = declarative_base()


def create_db_session() -> Session:
    engine = create_engine(settings.DATABASE_CONNECTION_URI)
    local_session = sessionmaker(bind=engine)
    return local_session()


class DBService:
    pass


class ItemDB(Base):
    __tablename__ = "item"

    item_uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    title = Column(String, index=True)
    jsonld_metadata = Column(JSONB, nullable=False, default={})
    date_created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())

    files = relationship("FileDB", back_populates="item")

    def to_item(self) -> "Item":
        return Item(
            item_uuid=self.item_uuid,
            title=self.title,
            jsonld_metadata=ItemMetadata.from_jsonld(self.jsonld_metadata),
            date_created=self.date_created,
            date_updated=self.date_updated,
        )

    @classmethod
    def from_item(cls, item: "Item") -> "ItemDB":
        return cls(
            item_uuid=item.item_uuid,
            title=item.title,
            jsonld_metadata=item.jsonld_metadata.to_compact(),
        )


class FileDB(Base):
    __tablename__ = "file"

    file_uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    item_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("item.item_uuid", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    filename = Column(String, index=True)
    mimetype = Column(String, index=True)
    date_created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())

    item = relationship("ItemDB", back_populates="files")

    def to_file(self) -> "File":
        return File(
            file_uuid=self.file_uuid,
            item_uuid=self.item_uuid,
            filename=self.filename,
            mimetype=self.mimetype,
            date_created=self.date_created,
            date_updated=self.date_updated,
        )

    @classmethod
    def from_file(cls, file: "File") -> "FileDB":
        return cls(
            file_uuid=file.file_uuid,
            item_uuid=file.item_uuid,
            filename=file.filename,
            mimetype=file.mimetype,
        )


class RelationshipDB(Base):
    __tablename__ = "relationship"

    relationship_uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )

    subject = Column(String, index=True)
    predicate = Column(String, index=True)
    object = Column(String, index=True)

    date_created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())


class PostgresDBService(DBService):
    def __init__(self, session: Session | None = None):
        self.session = session or create_db_session()

    def _get_item_db(self, item_uuid: str) -> ItemDB | None:
        return self.session.get(ItemDB, item_uuid)

    def _get_file_db(self, file_uuid: str) -> FileDB | None:
        return self.session.get(FileDB, file_uuid)

    def save_item(self, item: "Item", *, commit: bool = True) -> "Item":
        """Save an Item to the Database.

        Create if not exists, else update.
        """
        files = item.files

        if not item.item_uuid:
            item_uuid = str(uuid.uuid4())
            item.item_uuid = item_uuid
            item.jsonld_metadata.set_id(item_uuid)

        item_db = ItemDB.from_item(item)

        try:
            item_db = self.session.merge(item_db)
            if commit:
                self.session.commit()
            else:
                self.session.flush()
        except SQLAlchemyError:
            logger.exception("Error saving Item")
            self.session.rollback()
            raise

        self.session.refresh(item_db)
        new_item = item_db.to_item()
        new_item.files = files

        return new_item

    def save_file(self, file: "File", *, commit: bool = True) -> File:
        """Save a File to the Database.

        Create if not exists, else update.
        """
        data, filepath = file.data, file.filepath

        file_db = FileDB.from_file(file)

        try:
            file_db = self.session.merge(file_db)
            if commit:
                self.session.commit()
            else:
                self.session.flush()
        except SQLAlchemyError:
            logger.exception("Error saving File")
            self.session.rollback()
            raise

        self.session.refresh(file_db)
        new_file = file_db.to_file()
        new_file.data = data
        new_file.filepath = filepath

        return new_file

    def get_item(self, item_uuid: str) -> Optional["Item"]:
        """Retrieve an Item by its UUID and convert it to the domain model."""
        item_db = self._get_item_db(item_uuid)
        if not item_db:
            return None

        files = [file.to_file() for file in item_db.files]
        item = item_db.to_item()
        item.files = files
        return item

    def get_file(self, file_uuid: str) -> Optional["File"]:
        """Retrieve a File by its UUID and convert it to the domain model."""
        file_db = self._get_file_db(file_uuid)
        if not file_db:
            return None
        item = file_db.item.to_item()
        file = file_db.to_file()
        file.item = item
        return file

    def get_items(self, batch_size=100) -> Iterator["Item"]:
        """Yield all Items from the item table."""
        query = self.session.query(ItemDB).yield_per(batch_size)
        for item_db in query:
            files = [file.to_file() for file in item_db.files]
            item = item_db.to_item()
            item.files = files
            yield item

    def delete_item(self, item: "Item", *, commit: bool = True):
        item_db = self._get_item_db(item.item_uuid)
        self.session.delete(item_db)
        if commit:
            self.session.commit()
        else:
            self.session.flush()
        return True

    def delete_file(self, file: "File", *, commit: bool = True):
        file_db = self._get_file_db(file.file_uuid)
        if not file_db:
            return False
        self.session.delete(file_db)
        if commit:
            self.session.commit()
        else:
            self.session.flush()
        return True
