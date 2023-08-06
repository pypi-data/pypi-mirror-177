from __future__ import annotations


def string_(data: list[str]) -> str:
    """
    Parses the input data when only one line is present.

    Args:
        data (list[str]): The list of lines read from the input.

    Returns:
        str: The string of input data.
    """
    if len(data) == 1:
        return data[0]
    else:
        raise ValueError(
            "Parser expected input with a single line, got multiple lines."
        )
