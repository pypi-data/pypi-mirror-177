import pytest

from advent_utils.parsers import string_

# ==================================================
#   string_()
# ==================================================


def test_string_returns_first_line_of_input_data() -> None:
    expected: str = "Single, I am"

    assert string_([expected]) == expected


def test_string_raises_error_when_more_than_one_line() -> None:
    with pytest.raises(
        ValueError,
        match=r"Parser expected input with a single line, got multiple lines.",
    ):
        string_(["Single, I should be", "oops"])
