# Copyright (c) 2026 TW4RDYDEV. All rights reserved.

from __future__ import annotations

import math


def group_from_right(value: str, size: int) -> str:
    if not value:
        return value

    sign = ""
    if value[0] in "+-":
        sign, value = value[0], value[1:]

    groups = []
    while value:
        groups.append(value[-size:])
        value = value[:-size]

    grouped = " ".join(reversed(groups))
    return f"{sign}{grouped}"


def format_binary(value: int, *, width: int | None, grouped: bool) -> str:
    if width is not None:
        raw = value & ((1 << width) - 1)
        result = format(raw, f"0{width}b")
    elif value < 0:
        result = "-" + format(abs(value), "b")
    else:
        result = format(value, "b")

    return group_from_right(result, 4) if grouped else result


def format_octal(value: int, *, width: int | None) -> str:
    if width is not None:
        raw = value & ((1 << width) - 1)
        digits = math.ceil(width / 3)
        return format(raw, f"0{digits}o")
    if value < 0:
        return "-" + format(abs(value), "o")
    return format(value, "o")


def format_hex(value: int, *, width: int | None, uppercase: bool) -> str:
    if width is not None:
        raw = value & ((1 << width) - 1)
        digits = math.ceil(width / 4)
        result = format(raw, f"0{digits}X" if uppercase else f"0{digits}x")
    elif value < 0:
        body = format(abs(value), "X" if uppercase else "x")
        result = "-" + body
    else:
        result = format(value, "X" if uppercase else "x")
    return result


def required_bits(value: int, signed: bool) -> int:
    if value == 0:
        return 1

    if not signed:
        return value.bit_length()

    if value > 0:
        return value.bit_length() + 1

    # Minimum two's-complement width that can represent the negative number.
    return (~value).bit_length() + 1


def required_bytes(bit_count: int) -> int:
    return max(1, math.ceil(bit_count / 8))
