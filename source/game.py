"""
Game logic for the game 'Abandoned Space Station'.

Contains the main game class and related functionality.
"""

import random
import sys
import os

from typing import Set, Tuple, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from exam.source.helpers import clear_terminal, process_coordinates


class AbandonedSpaceStation:
    """
    Main class for the game 'Abandoned Space Station'.

    Manages game state, grid, hazards, and player interactions.
    """

    def __init__(
        self, grid_width: int = 5, grid_height: int = 5, hazard_count: int = 5
    ) -> None:
        """
        Initialize a new game instance.

        Args:
            grid_width: Width of the game grid (default: 5)
            grid_height: Height of the game grid (default: 5)
            hazard_count: Number of hazards on the game grid (default: 5)
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.hazard_count = hazard_count
        self.grid: List[List[str]] = [
            ["?"] * self.grid_width for _ in range(self.grid_height)
        ]
        self.hazard_locations: Set[Tuple[int, int]] = set()
        self._place_hazards()
        self.scanned_areas: Set[Tuple[int, int]] = set()
        self.is_defeated = False
        self.is_victorious = False
        self.action_count = 0

    def _place_hazards(self) -> None:
        """
        Place hazards randomly on the game grid.
        """
        placed = 0
        while placed < self.hazard_count:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            position = (x, y)
            if position not in self.hazard_locations:
                self.hazard_locations.add(position)
                placed += 1

    def _count_adjacent_hazards(self, x: int, y: int) -> int:
        """
        Count the number of adjacent hazards for a given area.

        Args:
            x: X-coordinate of the area
            y: Y-coordinate of the area

        Returns:
            Number of adjacent hazards
        """
        if (x, y) in self.hazard_locations:
            return 0

        hazard_count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if (dx == 0 and dy == 0) or not (
                    0 <= nx < self.grid_width and 0 <= ny < self.grid_height
                ):
                    continue
                if (nx, ny) in self.hazard_locations:
                    hazard_count += 1
        return hazard_count

    def count_adjacent_hazards(self, x: int, y: int) -> int:
        """
        Public method to count the number of adjacent hazards for testing.

        Args:
            x: X-coordinate of the area
            y: Y-coordinate of the area

        Returns:
            Number of adjacent hazards
        """
        return self._count_adjacent_hazards(x, y)

    def scan_area(self, x: int, y: int) -> bool:
        """
        Scan an area on the game grid.

        Args:
            x: X-coordinate
            y: Y-coordinate

        Returns:
            True if the scan was successful, False if a hazard was detected
        """
        if not (0 <= x < self.grid_width and 0 <= y < self.grid_height):
            print("Invalid coordinates. Please try again.")
            return True

        if (x, y) in self.scanned_areas:
            print("This area has already been scanned. Please choose another.")
            return True

        self.action_count += 1

        if (x, y) in self.hazard_locations:
            self.grid[y][x] = "H"
            self.is_defeated = True
            return False

        adjacent = self._count_adjacent_hazards(x, y)
        self.grid[y][x] = str(adjacent)
        self.scanned_areas.add((x, y))

        self.check_victory_condition()
        return True

    def check_victory_condition(self) -> bool:
        """
        Check if all safe areas have been scanned and update victory status.

        Returns:
            True if the game is won, False otherwise
        """
        safe_area_count = (self.grid_width * self.grid_height) - len(
            self.hazard_locations
        )
        if len(self.scanned_areas) >= safe_area_count:
            self.is_victorious = True
            return True
        return False

    def display_grid(self, debug: bool = False) -> None:
        """
        Display the current game grid.

        Args:
            debug: Shows hazards in debug mode when True
        """
        print("   ", end="")
        for x in range(self.grid_width):
            print(f" {x} ", end="")
        print("\n   ", end="")
        print("---" * self.grid_width)

        for y in range(self.grid_height):
            print(f"{y} |", end="")
            for x in range(self.grid_width):
                if debug and (x, y) in self.hazard_locations:
                    print(" H ", end="")
                else:
                    print(f" {self.grid[y][x]} ", end="")
            print()
        print()

    def play(self) -> None:
        """
        Start the game and manage the game flow.
        """
        clear_terminal()
        print("\n" + "=" * 40)
        print("  Abandoned Space Station")
        print("=" * 40)
        print("\nWelcome to the derelict space station!")
        print("Your mission is to scan all safe areas,")
        print("without triggering any hazards.")
        print("\nInstructions:")
        print("- ? = Unexplored area")
        print("- 0-8 = Number of adjacent hazards")
        print("- H = Hazard (Game Over)")
        print("\nEnter coordinates in the format 'x y' (e.g. '2 3')")
        print("Enter 'q' to quit the game.")
        print("=" * 40 + "\n")

        while not (self.is_defeated or self.is_victorious):
            self.display_grid()
            while True:
                input_value = input("Enter coordinates (x y) or 'q' to quit: ").strip()
                success, coordinates, error_message = process_coordinates(
                    input_value, self.grid_width, self.grid_height
                )
                if not success:
                    print(error_message)
                    continue
                if input_value.lower() == "q":
                    print("\nGame terminated. Goodbye!")
                    return
                if coordinates is None:
                    print("Invalid coordinates. Please try again.")
                    continue
                break

            x, y = coordinates
            success = self.scan_area(x, y)
            if not success:
                break

            clear_terminal()
            self.check_victory_condition()
            if self.is_victorious:
                break

        self.display_grid()
        if self.is_defeated:
            print("\nALERT! You've triggered a hazard.")
            print("GAME OVER - The station has claimed another explorer.")
        elif self.is_victorious:
            print("\nCongratulations! You've mapped all safe areas.")
            print("The space station is now secured. Mission accomplished!")

        self._show_statistics()

    def _show_statistics(self) -> None:
        """
        Display game statistics after the game ends.
        """
        total_areas = self.grid_width * self.grid_height
        safe_areas = total_areas - len(self.hazard_locations)
        completion_percent = (
            (len(self.scanned_areas) / safe_areas) * 100 if safe_areas > 0 else 0
        )

        print("\n" + "-" * 40)
        print("MISSION STATISTICS")
        print("-" * 40)
        print(f"Grid size: {self.grid_width}x{self.grid_height}")
        print(f"Number of hazards: {len(self.hazard_locations)}")
        print(
            f"Areas scanned: {len(self.scanned_areas)} of {safe_areas} "
            f"({completion_percent:.1f}%)"
        )
        print(f"Total actions: {self.action_count}")
        print("-" * 40)
