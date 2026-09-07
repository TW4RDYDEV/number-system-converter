# Copyright (c) 2026 TW4RDYDEV. All rights reserved.

from __future__ import annotations

BASES = {
    "Binary": 2,
    "Octal": 8,
    "Decimal": 10,
    "Hexadecimal": 16,
}


def strip_separators(value: str) -> str:
    return value.strip().replace(" ", "").replace("_", "")


def detect_base(value: str) -> str:
    """
    Detect a number system conservatively.

    Prefixes are authoritative. Unprefixed values containing A-F are treated
    as hexadecimal. Digits-only values default to decimal to avoid guessing
    that values such as 10 or 100 are binary.
    """
    cleaned = strip_separators(value)

    if not cleaned:
        raise ValueError("Enter a number first.")

    unsigned = cleaned[1:] if cleaned[:1] in {"+", "-"} else cleaned
    lowered = unsigned.lower()

    if lowered.startswith("0b"):
        return "Binary"
    if lowered.startswith("0o"):
        return "Octal"
    if lowered.startswith("0x"):
        return "Hexadecimal"

    if any(char in "abcdefABCDEF" for char in unsigned):
        return "Hexadecimal"

    if unsigned.isdigit():
        return "Decimal"

    raise ValueError("Could not automatically detect the number system.")


def base_value(base_name: str) -> int:
    if base_name not in BASES:
        raise ValueError(f"Unsupported number system: {base_name}")
    return BASES[base_name]
