from tidepool.settings.manager import TidepoolSettings


def test_globally_imported_settings_are_tidepoolsettings_instance(test_settings):
    assert isinstance(test_settings, TidepoolSettings)


def test_update_settings_from_module_string(test_settings):
    test_settings.update_from_module("tests.fixtures.settings_test_addition_1")
    assert test_settings.FRUIT == "honeydew"


def test_update_settings_from_imported_module(test_settings):
    from tests.fixtures import settings_test_addition_1

    test_settings.update_from_module(settings_test_addition_1)
    assert test_settings.FRUIT == "honeydew"


def test_update_settings_from_dict(test_settings):
    test_settings.update_from_dict({"FRUIT": "honeydew"})
    assert test_settings.FRUIT == "honeydew"


def test_update_settings_from_for_single_key_value(test_settings):
    test_settings.update(FRUIT="honeydew", VEGETABLE="onion")
    assert test_settings.FRUIT == "honeydew"
    assert test_settings.VEGETABLE == "onion"
