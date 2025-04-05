"""
Helper functions for the game 'Abandoned Space Station'.

Provides utility functions used across the game.
"""

import os
from typing import Tuple, Union


def clear_terminal() -> None:
    """
    Clear the terminal content for better readability.
    """
    if os.name == "nt":  # Windows
        _ = os.system("cls")
    else:  # Unix/Linux/Mac
        _ = os.system("clear")


def process_coordinates(
    input_str: str, grid_width: int, grid_height: int
) -> tuple[bool, Union[Tuple[int, int], None], str]:
    """
    Process and validate user input for coordinates.

    Args:
        input_str: The user input as string
        grid_width: The width of the game grid
        grid_height: The height of the game grid

    Returns:
        Tuple with:
        - Success (bool): True if the input is valid
        - Coordinates (Tuple[int, int] or None): The x,y coordinates or None on error
        - Error message (str): Empty string on success, otherwise error description
    """
    input_str = input_str.strip()

    if input_str.lower() == "q":
        return True, None, ""

    parts = input_str.split()
    if len(parts) != 2:
        return (
            False,
            None,
            "Invalid input. Please enter two numbers in the format 'x y'.",
        )

    try:
        x, y = map(int, parts)
    except ValueError:
        return False, None, "Invalid input. Please enter two whole numbers."

    error_msg = (
        f"Coordinates out of bounds. Valid ranges: "
        f"0-{grid_width - 1} for x, 0-{grid_height - 1} for y."
    )

    if not (0 <= x < grid_width and 0 <= y < grid_height):
        return False, None, error_msg

    return True, (x, y), ""
