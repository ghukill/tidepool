import pytest

from tidepool import settings


@pytest.fixture(autouse=True)
def _testing_env(monkeypatch):
    monkeypatch.setenv(
        "TIDEPOOL_SETTINGS_MODULE",
        "tests.fixtures.settings_test",
    )
    settings.update_from_module("tests.fixtures.settings_test")


@pytest.fixture
def test_settings():
    from tidepool import settings

    return settings
