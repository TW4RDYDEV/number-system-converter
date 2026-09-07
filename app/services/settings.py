# Copyright (c) 2026 TW4RDYDEV. All rights reserved.

from __future__ import annotations

from PySide6.QtCore import QSettings


DEFAULTS = {
    "theme": "dark",
    "liveConversion": True,
    "uppercaseHex": True,
    "groupBinary": True,
    "rememberHistory": True,
    "defaultBitWidth": "Auto",
}

VALID_VALUES = {
    "theme": {"dark", "light", "system"},
    "defaultBitWidth": {"Auto", "8-bit", "16-bit", "32-bit", "64-bit"},
}


class SettingsService:
    def __init__(self) -> None:
        self._settings = QSettings()

    def get_all(self) -> dict:
        values = {}
        for key, default in DEFAULTS.items():
            value = self._settings.value(key, default)

            if isinstance(default, bool):
                if isinstance(value, str):
                    value = value.lower() in {"1", "true", "yes", "on"}
                else:
                    value = bool(value)

            if key in VALID_VALUES and value not in VALID_VALUES[key]:
                value = default

            values[key] = value

        return values

    def set_value(self, key: str, value) -> None:
        if key not in DEFAULTS:
            return

        if key in VALID_VALUES and value not in VALID_VALUES[key]:
            return

        self._settings.setValue(key, value)
        self._settings.sync()
