"""
Abandoned Space Station - A console-based Python game

Main file to start the game
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from exam.source.game import AbandonedSpaceStation
from exam.source.helpers import clear_terminal


def _get_custom_settings() -> tuple[int, int, int]:
    """
    Gets the user-defined game settings.

    Returns:
        Tuple with grid_width, grid_height and number of hazards
    """
    grid_width, grid_height, hazards = 5, 5, 5

    while True:
        try:
            width_input = input("Width (min. 5): ").strip()
            grid_width = int(width_input)
            if grid_width < 5:
                print("Width must be at least 5.")
                continue
            break
        except ValueError:
            print("Please enter a whole number.")

    while True:
        try:
            height_input = input("Height (min. 5): ").strip()
            grid_height = int(height_input)
            if grid_height < 5:
                print("Height must be at least 5.")
                continue
            break
        except ValueError:
            print("Please enter a whole number.")

    while True:
        try:
            hazards_input = input("Number of hazards: ").strip()
            hazards = int(hazards_input)
            if hazards < 1:
                print("There must be at least 1 hazard.")
                continue
            max_hazards = (grid_width * grid_height) - 1
            if max_hazards < hazards:
                print(f"There can be a maximum of {max_hazards} hazards.")
                continue
            break
        except ValueError:
            print("Please enter a whole number.")

    return grid_width, grid_height, hazards


def main() -> None:
    """Main function to start the game."""
    clear_terminal()
    print("Abandoned Space Station\n")
    game = None

    while True:
        customize_input = (
            input("Would you like to customize the grid size? (y/n):").lower().strip()
        )
        if customize_input not in ["y", "n"]:
            print("Please enter 'y' or 'n'.")
        else:
            break

    if customize_input == "y":
        grid_width, grid_height, hazards = _get_custom_settings()
        game = AbandonedSpaceStation(grid_width, grid_height, hazards)
    else:
        game = AbandonedSpaceStation()

    if game:
        game.play()


def handle_game_interrupt() -> None:
    """Handles KeyboardInterrupt when the game is interrupted by the user."""
    print("\nGame was interrupted by the user. Goodbye!")
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        handle_game_interrupt()
