from __future__ import annotations

import pytest

from advent_utils import move

# ==================================================
#   move
# ==================================================


@pytest.mark.parametrize(
    "key,expected",
    [("up", (0, 1)), ("down", (0, -1)), ("left", (-1, 0)), ("right", (1, 0))],
)
def test_move(key: str, expected: tuple[int, int]) -> None:
    assert move[key]((0, 0)) == expected
