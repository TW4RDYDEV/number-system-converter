# Copyright (c) 2026 TW4RDYDEV. All rights reserved.

from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication

from app.core.converter import ConversionOptions, convert_number
from app.services.history import HistoryService, build_history_item
from app.services.settings import SettingsService


class AppBackend(QObject):
    historyChanged = Signal()
    settingsChanged = Signal()
    toastRequested = Signal(str)

    def __init__(self, version: str, parent=None) -> None:
        super().__init__(parent)
        self._version = version
        self._settings = SettingsService()
        initial_settings = self._settings.get_all()
        self._history_service = HistoryService(
            load_persisted=bool(initial_settings["rememberHistory"])
        )

    @Property(str, constant=True)
    def version(self) -> str:
        return self._version

    @Property("QVariantList", notify=historyChanged)
    def history(self):
        return self._history_service.items

    @Slot(result="QVariantMap")
    def getSettings(self):
        return self._settings.get_all()

    @Slot(str, "QVariant")
    def setSetting(self, key: str, value) -> None:
        self._settings.set_value(key, value)

        if key == "rememberHistory":
            if bool(value):
                self._history_service.save()
            else:
                self._history_service.remove_persisted()

        self.settingsChanged.emit()

    @Slot(str, str, int, bool, bool, result="QVariantMap")
    def convertNumber(
        self,
        text: str,
        input_base: str,
        bit_width: int,
        signed_mode: bool,
        add_history: bool,
    ):
        settings = self._settings.get_all()
        options = ConversionOptions(
            bit_width=bit_width if bit_width in {8, 16, 32, 64} else None,
            signed=signed_mode,
            uppercase_hex=bool(settings["uppercaseHex"]),
            group_binary=bool(settings["groupBinary"]),
        )

        try:
            result = convert_number(text, input_base, options)
            result["ok"] = True
            result["error"] = ""

            if add_history:
                item = build_history_item(text.strip(), result)
                self._history_service.add(
                    item,
                    remember=bool(settings["rememberHistory"]),
                )
                self.historyChanged.emit()

            return result

        except ValueError as exc:
            return {
                "ok": False,
                "error": str(exc),
                "detectedBase": "",
                "decimal": "",
                "binary": "",
                "octal": "",
                "hexadecimal": "",
                "bitLength": 0,
                "byteRequirement": 0,
                "parity": "",
                "sign": "",
                "decimalDigits": 0,
                "hexDigits": 0,
                "unsignedValue": "",
                "signedValue": "",
                "twosComplement": "",
                "bitWidth": 0,
                "signedMode": signed_mode,
            }

    @Slot(str)
    def copyText(self, text: str) -> None:
        if not text:
            return
        QGuiApplication.clipboard().setText(text)
        self.toastRequested.emit("Copied to clipboard")

    @Slot()
    def clearHistory(self) -> None:
        remember = bool(self._settings.get_all()["rememberHistory"])
        self._history_service.clear(remember=remember)
        self.historyChanged.emit()
        self.toastRequested.emit("History cleared")

    @Slot(int)
    def deleteHistory(self, index: int) -> None:
        remember = bool(self._settings.get_all()["rememberHistory"])
        self._history_service.delete(index, remember=remember)
        self.historyChanged.emit()

    @Slot(str, str)
    def exportHistory(self, destination: str, file_type: str) -> None:
        try:
            path = self._history_service.export(destination, file_type)
            self.toastRequested.emit(f"History exported to {path.name}")
        except OSError:
            self.toastRequested.emit("Could not export history")
