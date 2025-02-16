from tidepool import Item


def test_init_item_from_file(small_jpeg_image_filepath):
    filename = small_jpeg_image_filepath.split("/")[-1]
    item = Item.from_file(small_jpeg_image_filepath)

    assert item.title == filename
    assert item.jsonld_metadata.to_compact()["dc:title"] == filename

    assert len(item.files) == 1
    file = item.files[0]
    assert file.mimetype == "image/jpeg"
    assert file.filename == filename
