# Copyright (c) 2026 TW4RDYDEV. All rights reserved.

from __future__ import annotations

from dataclasses import dataclass
import math

from .detector import base_value, detect_base, strip_separators
from .formatter import (
    format_binary,
    format_hex,
    format_octal,
    required_bits,
    required_bytes,
)


@dataclass(frozen=True)
class ConversionOptions:
    bit_width: int | None = None
    signed: bool = False
    uppercase_hex: bool = True
    group_binary: bool = True


def _remove_prefix(value: str, base_name: str) -> str:
    sign = ""
    if value[:1] in {"+", "-"}:
        sign, value = value[0], value[1:]

    prefixes = {
        "Binary": "0b",
        "Octal": "0o",
        "Hexadecimal": "0x",
    }

    prefix = prefixes.get(base_name)
    if prefix and value.lower().startswith(prefix):
        value = value[2:]

    return sign + value


def _validate_digits(value: str, base_name: str) -> None:
    signless = value[1:] if value[:1] in {"+", "-"} else value

    if not signless:
        raise ValueError("Enter a valid number.")

    valid = {
        "Binary": set("01"),
        "Octal": set("01234567"),
        "Decimal": set("0123456789"),
        "Hexadecimal": set("0123456789abcdefABCDEF"),
    }[base_name]

    invalid = sorted(set(ch for ch in signless if ch not in valid))
    if invalid:
        joined = ", ".join(invalid)
        raise ValueError(f"Invalid {base_name.lower()} character(s): {joined}")


def _parse_value(text: str, base_name: str) -> tuple[int, bool]:
    cleaned = strip_separators(text)
    explicitly_negative = cleaned.startswith("-")
    cleaned = _remove_prefix(cleaned, base_name)
    _validate_digits(cleaned, base_name)
    return int(cleaned, base_value(base_name)), explicitly_negative


def _infer_signed_auto_width(value: int) -> int:
    """
    Infer a natural signed width for a raw non-decimal bit pattern.

    Auto Signed mode uses the smallest whole-byte width that can contain the
    entered raw value. This makes values such as 11111111 / 0xFF naturally
    interpret as 8-bit two's-complement values, while preserving arbitrary
    precision for larger inputs.
    """
    bits = max(1, value.bit_length())
    return max(8, math.ceil(bits / 8) * 8)


def _interpret_fixed_width(
    value: int,
    *,
    input_base: str,
    bit_width: int,
    signed: bool,
    explicitly_negative: bool,
) -> tuple[int, int]:
    mask = (1 << bit_width) - 1

    if signed:
        minimum = -(1 << (bit_width - 1))
        maximum = (1 << (bit_width - 1)) - 1

        # Binary/octal/hex inputs can represent a raw two's-complement bit pattern.
        if (
            input_base != "Decimal"
            and not explicitly_negative
            and value >= 0
            and value <= mask
        ):
            raw = value
            interpreted = raw - (1 << bit_width) if raw & (1 << (bit_width - 1)) else raw
            return interpreted, raw

        if not minimum <= value <= maximum:
            raise ValueError(
                f"{value} does not fit in a signed {bit_width}-bit integer "
                f"({minimum} to {maximum})."
            )
        return value, value & mask

    if value < 0:
        raise ValueError("Negative values require Signed mode.")

    if value > mask:
        raise ValueError(
            f"{value} does not fit in an unsigned {bit_width}-bit integer "
            f"(0 to {mask})."
        )

    return value, value


def convert_number(
    text: str,
    input_base: str,
    options: ConversionOptions,
) -> dict:
    if not text.strip():
        raise ValueError("Enter a number first.")

    detected = detect_base(text) if input_base == "Auto" else input_base
    if detected not in {"Binary", "Octal", "Decimal", "Hexadecimal"}:
        raise ValueError("Choose a supported input number system.")

    parsed_value, explicitly_negative = _parse_value(text, detected)
    value = parsed_value
    raw_value = parsed_value if parsed_value >= 0 else None
    effective_width = options.bit_width

    if effective_width is not None:
        if effective_width not in {8, 16, 32, 64}:
            raise ValueError("Bit width must be Auto, 8, 16, 32, or 64.")

        value, raw_value = _interpret_fixed_width(
            parsed_value,
            input_base=detected,
            bit_width=effective_width,
            signed=options.signed,
            explicitly_negative=explicitly_negative,
        )

    elif (
        options.signed
        and detected != "Decimal"
        and not explicitly_negative
        and parsed_value >= 0
    ):
        effective_width = _infer_signed_auto_width(parsed_value)
        value, raw_value = _interpret_fixed_width(
            parsed_value,
            input_base=detected,
            bit_width=effective_width,
            signed=True,
            explicitly_negative=False,
        )

    elif not options.signed and parsed_value < 0:
        raise ValueError("Negative values require Signed mode.")

    bit_count = (
        effective_width
        if effective_width is not None
        else required_bits(value, options.signed)
    )

    decimal_value = str(value)
    binary_value = format_binary(
        value,
        width=effective_width,
        grouped=options.group_binary,
    )
    octal_value = format_octal(value, width=effective_width)
    hex_value = format_hex(
        value,
        width=effective_width,
        uppercase=options.uppercase_hex,
    )

    unsigned_value = ""
    signed_value = ""
    twos_complement = ""

    if effective_width is not None:
        unsigned_value = str(raw_value)
        sign_bit = 1 << (effective_width - 1)
        signed_interpretation = (
            raw_value - (1 << effective_width)
            if raw_value & sign_bit
            else raw_value
        )
        signed_value = str(signed_interpretation)
        twos_complement = format_hex(
            raw_value,
            width=effective_width,
            uppercase=options.uppercase_hex,
        )

    sign_label = "Zero" if value == 0 else ("Negative" if value < 0 else "Positive")
    parity = "Even" if value % 2 == 0 else "Odd"

    return {
        "detectedBase": detected,
        "decimal": decimal_value,
        "binary": binary_value,
        "octal": octal_value,
        "hexadecimal": hex_value,
        "bitLength": bit_count,
        "byteRequirement": required_bytes(bit_count),
        "parity": parity,
        "sign": sign_label,
        "decimalDigits": len(str(abs(value))),
        "hexDigits": len(hex_value.replace("-", "").replace(" ", "")),
        "unsignedValue": unsigned_value,
        "signedValue": signed_value,
        "twosComplement": twos_complement,
        "bitWidth": effective_width or 0,
        "signedMode": options.signed,
    }
