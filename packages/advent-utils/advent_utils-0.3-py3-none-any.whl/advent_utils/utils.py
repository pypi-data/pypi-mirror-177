from __future__ import annotations

from typing import Callable

move: dict[str, Callable] = {
    "up": lambda c: (c[0], c[1] + 1),
    "down": lambda c: (c[0], c[1] - 1),
    "left": lambda c: (c[0] - 1, c[1]),
    "right": lambda c: (c[0] + 1, c[1]),
}
