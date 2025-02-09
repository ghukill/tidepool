from tidepool import settings
from tidepool import TidepoolRepository


def test_init_repository_default():
    tr = TidepoolRepository()
    assert isinstance(tr, TidepoolRepository)


def test_init_repository_name_from_settings():
    repo_name = "GooberTronic Repository"
    settings.REPOSITORY_NAME = repo_name
    tr = TidepoolRepository()
    assert tr.name == repo_name
