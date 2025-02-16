"""
tidepool/settings_manager.py
"""

import importlib
import os
from types import ModuleType
from typing import Any


class TidepoolSettings:
    def __init__(self, _settings: dict | None = None):
        if _settings:
            self._settings = _settings
        else:
            self._settings = self.load_from_module()

    def __getattr__(self, name: str) -> Any:
        try:
            return self._settings[name]
        except KeyError:
            raise AttributeError(f"Setting '{name}' not found")

    def clear(self):
        self._settings = {}

    def load_from_module(self) -> dict:
        settings_module = os.environ.get(
            "TIDEPOOL_SETTINGS_MODULE",
            "tidepool.settings.base",
        )
        try:
            mod = importlib.import_module(settings_module)
        except ImportError as e:
            raise ImportError(f"Could not import settings '{settings_module}': {e}")
        return self._get_dict_from_module(mod)

    @staticmethod
    def _get_dict_from_module(mod: ModuleType):
        return {key: getattr(mod, key) for key in dir(mod) if key.isupper()}

    def update_from_module(self, mod: str | ModuleType):
        if isinstance(mod, str):
            mod = importlib.import_module(mod)
        self._settings.update(self._get_dict_from_module(mod))

    def update_from_dict(self, data: dict):
        self._settings.update({key: val for key, val in data.items() if key.isupper()})

    def update(self, **kwargs):
        self.update_from_dict(kwargs)


settings = TidepoolSettings()
