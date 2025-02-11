import uuid

from tidepool import settings
from tidepool import TidepoolRepository


def test_init_repository_default():
    tr = TidepoolRepository()
    assert isinstance(tr, TidepoolRepository)


def test_init_repository_read_from_settings():
    repo_name = f"Tidepool Repository {str(uuid.uuid4())}"
    settings.REPOSITORY_NAME = repo_name
    tr = TidepoolRepository()
    assert tr.name == repo_name
