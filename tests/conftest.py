import pytest

from tidepool import settings, Item, TidepoolRepository


@pytest.fixture(autouse=True)
def _testing_settings(monkeypatch, tmp_path, storage_primary_posix_path):
    # wipe settings
    settings.clear()

    # set env vars
    monkeypatch.setenv("TIDEPOOL_POSIX_DATA_DIR", storage_primary_posix_path)

    # reload settings from testing module
    settings.update_from_module("tests.fixtures.settings.settings_test")


@pytest.fixture
def storage_primary_posix_path(tmp_path):
    return str(tmp_path / "storage" / "posix" / "data")


@pytest.fixture
def testing_settings():
    from tidepool import settings

    return settings


@pytest.fixture
def repository():
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
