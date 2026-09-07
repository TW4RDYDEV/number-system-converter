from app.core.detector import detect_base


def test_prefix_detection():
    assert detect_base("0b1010") == "Binary"
    assert detect_base("0o755") == "Octal"
    assert detect_base("0xF3C") == "Hexadecimal"


def test_hex_letters_detection():
    assert detect_base("DEADBEEF") == "Hexadecimal"


def test_digits_default_to_decimal():
    assert detect_base("1010") == "Decimal"
    assert detect_base("415") == "Decimal"
