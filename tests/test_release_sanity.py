from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_qt_quick_uses_customizable_style():
    source = (ROOT / "main.py").read_text(encoding="utf-8")
    assert 'QQuickStyle.setStyle("Basic")' in source


def test_backend_is_parented_to_qml_engine():
    source = (ROOT / "main.py").read_text(encoding="utf-8")
    assert "AppBackend(version=APP_VERSION, parent=engine)" in source


def test_shutdown_sensitive_qml_bindings_are_null_safe():
    main_qml = (ROOT / "app/ui/Main.qml").read_text(encoding="utf-8")
    converter_qml = (ROOT / "app/ui/pages/ConverterPage.qml").read_text(encoding="utf-8")
    settings_qml = (ROOT / "app/ui/pages/SettingsPage.qml").read_text(encoding="utf-8")

    assert 'backend ? "v" + backend.version : ""' in main_qml
    assert "backend ? backend.history : []" in converter_qml
    assert "backend ? backend.history.length" in converter_qml
    assert "backend ?" in settings_qml
