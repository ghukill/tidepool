"""tidepool/services/db.py"""

import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, UUID, DateTime
from sqlalchemy.sql import func

from tidepool import settings

Base = declarative_base()


def create_db_session():
    engine = create_engine(settings.DATABASE_CONNECTION_URI)
    local_session = sessionmaker(bind=engine)
    return local_session()


class ItemDB(Base):
    __tablename__ = "item"

    item_uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    title = Column(String, index=True)
    description = Column(String)
    date_created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())


class FileDB(Base):
    __tablename__ = "file"

    file_uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    filename = Column(String, index=True)
    mimetype = Column(String, index=True)
    storage_uri = Column(String, index=True)
    date_created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())


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


class DBService:
    def __init__(self, session=None):
        self.session = session or create_db_session()
