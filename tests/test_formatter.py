from app.core.formatter import group_from_right, required_bits, required_bytes


def test_binary_grouping():
    assert group_from_right("111100001111", 4) == "1111 0000 1111"
    assert group_from_right("-10101010", 4) == "-1010 1010"


def test_required_size_helpers():
    assert required_bits(255, False) == 8
    assert required_bytes(9) == 2
