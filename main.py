# Copyright (c) 2026 TW4RDYDEV. All rights reserved.
# Licensed under the TW4RDYDEV Source-Available License v1.0.

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtWidgets import QApplication

from app.backend import AppBackend


APP_NAME = "Number System Converter"
APP_VERSION = "1.0.0"
ORG_NAME = "TW4RDYDEV"


def resource_path(relative_path: str) -> Path:
    """Resolve files both from source and from PyInstaller's temporary bundle."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / relative_path


def main() -> int:
    QCoreApplication.setOrganizationName(ORG_NAME)
    QCoreApplication.setApplicationName(APP_NAME)
    QCoreApplication.setApplicationVersion(APP_VERSION)

    # Use a non-native Qt Quick Controls style because this application
    # intentionally customizes control backgrounds, indicators, and content.
    # This must be selected before QApplication/QML controls are created.
    QQuickStyle.setStyle("Basic")

    app = QApplication(sys.argv)
    app.setApplicationDisplayName(APP_NAME)
    app.setWindowIcon(QIcon(str(resource_path("assets/icon.png"))))

    engine = QQmlApplicationEngine()
    backend = AppBackend(version=APP_VERSION, parent=engine)
    engine.rootContext().setContextProperty("backend", backend)

    qml_file = resource_path("app/ui/Main.qml")
    engine.load(QUrl.fromLocalFile(str(qml_file)))

    if not engine.rootObjects():
        return 1

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
