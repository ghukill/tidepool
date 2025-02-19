from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command
import pytest

from tidepool import settings, Item, TidepoolRepository


@pytest.fixture(autouse=True)
def _testing_settings(
    monkeypatch,
    tmp_path,
    db_primary_posix_path,
    storage_primary_posix_path,
):
    # wipe settings
    settings.clear()

    # set env vars
    monkeypatch.setenv("TIDEPOOL_SQLITE_DB_DATA_DIR", db_primary_posix_path)
    monkeypatch.setenv("TIDEPOOL_POSIX_DATA_DIR", storage_primary_posix_path)

    # reload settings from testing module
    settings.update_from_module("tests.fixtures.settings.settings_test")


@pytest.fixture
def db_primary_posix_path(tmp_path):
    return str(tmp_path / "storage" / "sqlite" / "data")


@pytest.fixture
def storage_primary_posix_path(tmp_path):
    return str(tmp_path / "storage" / "posix" / "data")


@pytest.fixture
def testing_settings():
    from tidepool import settings

    return settings


@pytest.fixture
def run_db_migrations():
    alembic_cfg = AlembicConfig("tidepool/services/db/sqlite/alembic.ini")
    alembic_command.upgrade(alembic_cfg, "head")


@pytest.fixture
def sqlite_db_service(run_db_migrations):
    return True


@pytest.fixture
def repository(sqlite_db_service):
    return TidepoolRepository()


@pytest.fixture
def small_jpeg_image_filepath():
    return "tests/fixtures/data/images/washington_coast_rock.jpg"


@pytest.fixture
def jpeg_image_item(small_jpeg_image_filepath):
    return Item.from_file(small_jpeg_image_filepath)


@pytest.fixture
def text_file_item():
    item = Item.from_file("tests/fixtures/data/text/tidepool_wikipedia.txt")
    title = "Tidepool Snippet from Wikipedia"
    item.title = title
    item.jsonld_metadata.set_statement("dc:title", title)
    return item


@pytest.fixture
def text_data_item():
    return Item.from_data(
        b"Hello world!",
        "hello-world.txt",
        title="Hello World Notes",
    )
