from tidepool import TidepoolRepository


def test_init_repository():
    tr = TidepoolRepository()
    assert isinstance(tr, TidepoolRepository)
    assert tr.name == "Tidepool Repository - Testing"


def test_create_image_item(repository, jpeg_image_item):
    item = repository.save_item(jpeg_image_item)
    assert item.item_uuid


def test_create_text_file_item(repository, text_file_item):
    item = repository.save_item(text_file_item)
    assert item.item_uuid


def test_create_data_file_item(repository, text_data_item):
    item = repository.save_item(text_data_item)
    assert item.item_uuid


def test_update_item_title():
    pass


def test_update_item_metadata():
    pass


def test_read_file_data():
    pass


def test_bulk_save_items():
    pass


def test_bulk_update_items():
    pass


def test_get_item():
    pass
