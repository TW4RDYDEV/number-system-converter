from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_copy_signal_handlers_use_formal_parameters():
    source = (ROOT / "app/ui/pages/ConverterPage.qml").read_text(encoding="utf-8")
    assert "onCopyRequested: backend.copyText(value)" not in source
    assert source.count("onCopyRequested: function(value)") == 4
