from tidepool import TidepoolRepository


def test_init_repository():
    tr = TidepoolRepository()
    assert isinstance(tr, TidepoolRepository)
    assert tr.name == "Tidepool Repository - Testing"
