from tidepool.settings.manager import TidepoolSettings


def test_globally_imported_settings_are_tidepoolsettings_instance():
    from tidepool import settings

    assert isinstance(settings, TidepoolSettings)


def test_update_settings_from_module_path(testing_settings):
    testing_settings.update_from_module("tests.fixtures.settings.settings_test_addition_1")
    assert testing_settings.FRUIT == "honeydew"


def test_update_settings_from_imported_module(testing_settings):
    from tests.fixtures.settings import settings_test_addition_1

    testing_settings.update_from_module(settings_test_addition_1)
    assert testing_settings.FRUIT == "honeydew"


def test_update_settings_from_dict(testing_settings):
    testing_settings.update_from_dict({"FRUIT": "honeydew"})
    assert testing_settings.FRUIT == "honeydew"


def test_update_settings_from_for_single_key_value(testing_settings):
    testing_settings.update(FRUIT="honeydew", VEGETABLE="onion")
    assert testing_settings.FRUIT == "honeydew"
    assert testing_settings.VEGETABLE == "onion"
