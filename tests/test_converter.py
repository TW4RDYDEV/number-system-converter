import pytest

from app.core.converter import ConversionOptions, convert_number


def test_decimal_converts_to_all_bases():
    result = convert_number("415", "Decimal", ConversionOptions())
    assert result["decimal"] == "415"
    assert result["binary"].replace(" ", "") == "110011111"
    assert result["octal"] == "637"
    assert result["hexadecimal"] == "19F"


def test_auto_hex_prefix():
    result = convert_number("0xF3C", "Auto", ConversionOptions())
    assert result["detectedBase"] == "Hexadecimal"
    assert result["decimal"] == "3900"


def test_unsigned_8_bit():
    result = convert_number(
        "255",
        "Decimal",
        ConversionOptions(bit_width=8, signed=False),
    )
    assert result["binary"] == "1111 1111"
    assert result["hexadecimal"] == "FF"
    assert result["unsignedValue"] == "255"
    assert result["signedValue"] == "-1"


def test_signed_hex_bit_pattern():
    result = convert_number(
        "FF",
        "Hexadecimal",
        ConversionOptions(bit_width=8, signed=True),
    )
    assert result["decimal"] == "-1"
    assert result["binary"] == "1111 1111"
    assert result["signedValue"] == "-1"


def test_negative_decimal_requires_signed_mode():
    with pytest.raises(ValueError, match="Signed mode"):
        convert_number("-5", "Decimal", ConversionOptions(signed=False))


def test_negative_decimal_signed_mode():
    result = convert_number("-5", "Decimal", ConversionOptions(signed=True))
    assert result["decimal"] == "-5"
    assert result["binary"] == "-101"


def test_signed_8_bit_range_is_enforced():
    with pytest.raises(ValueError, match="signed 8-bit"):
        convert_number(
            "255",
            "Decimal",
            ConversionOptions(bit_width=8, signed=True),
        )


def test_invalid_binary_rejected():
    with pytest.raises(ValueError, match="Invalid binary"):
        convert_number("10201", "Binary", ConversionOptions())


def test_signed_auto_binary_infers_8_bit_twos_complement():
    result = convert_number(
        "1111 1111",
        "Binary",
        ConversionOptions(bit_width=None, signed=True),
    )
    assert result["decimal"] == "-1"
    assert result["bitWidth"] == 8
    assert result["unsignedValue"] == "255"
    assert result["signedValue"] == "-1"


def test_signed_auto_hex_infers_8_bit_twos_complement():
    result = convert_number(
        "FF",
        "Hexadecimal",
        ConversionOptions(bit_width=None, signed=True),
    )
    assert result["decimal"] == "-1"
    assert result["bitWidth"] == 8


def test_lowercase_hex_option():
    result = convert_number(
        "48879",
        "Decimal",
        ConversionOptions(uppercase_hex=False),
    )
    assert result["hexadecimal"] == "beef"


def test_binary_grouping_can_be_disabled():
    result = convert_number(
        "255",
        "Decimal",
        ConversionOptions(group_binary=False),
    )
    assert result["binary"] == "11111111"
