"""
Unit tests for the game functions in game.py
"""
# pylint: disable=C

import io
import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from exam.source.game import AbandonedSpaceStation


class TestAbandonedSpaceStation(unittest.TestCase):
    def setUp(self) -> None:
        self.grid_width = 5
        self.grid_height = 5
        self.hazard_count = 3
        self.game = AbandonedSpaceStation(
            grid_width=self.grid_width,
            grid_height=self.grid_height,
            hazard_count=self.hazard_count,
        )

    def test_init(self) -> None:
        self.assertEqual(self.game.grid_width, self.grid_width)
        self.assertEqual(self.game.grid_height, self.grid_height)
        self.assertEqual(len(self.game.hazard_locations), self.hazard_count)
        self.assertEqual(self.game.action_count, 0)
        self.assertFalse(self.game.is_defeated)
        self.assertFalse(self.game.is_victorious)

    def test_place_hazards(self) -> None:
        self.assertEqual(len(self.game.hazard_locations), self.hazard_count)
        for x, y in self.game.hazard_locations:
            self.assertTrue(
                0 <= x < self.grid_width, f"Hazard position X ({x}) outside valid range"
            )
            self.assertTrue(
                0 <= y < self.grid_height,
                f"Hazard position Y ({y}) outside valid range",
            )

    def test_count_adjacent_hazards(self) -> None:
        test_game = AbandonedSpaceStation(grid_width=5, grid_height=5, hazard_count=0)
        test_game.hazard_locations = {(1, 1), (2, 2), (3, 3)}
        self.assertEqual(test_game.count_adjacent_hazards(0, 0), 1)
        self.assertEqual(test_game.count_adjacent_hazards(2, 2), 0)
        self.assertEqual(test_game.count_adjacent_hazards(2, 1), 2)

    def test_scan_area_safe(self) -> None:
        test_game = AbandonedSpaceStation(grid_width=5, grid_height=5, hazard_count=0)
        test_game.hazard_locations = {(1, 1), (2, 2)}
        success = test_game.scan_area(0, 0)
        self.assertTrue(success)
        self.assertEqual(test_game.grid[0][0], "1")
        self.assertIn((0, 0), test_game.scanned_areas)
        self.assertFalse(test_game.is_defeated)
        self.assertEqual(test_game.action_count, 1)

    def test_scan_area_hazard(self) -> None:
        test_game = AbandonedSpaceStation(grid_width=5, grid_height=5, hazard_count=0)
        test_game.hazard_locations = {(1, 1)}
        success = test_game.scan_area(1, 1)
        self.assertFalse(success)
        self.assertEqual(test_game.grid[1][1], "H")
        self.assertTrue(test_game.is_defeated)
        self.assertEqual(test_game.action_count, 1)

    def test_scan_area_invalid(self) -> None:
        original_stdout = sys.stdout
        try:
            captured_output = io.StringIO()
            sys.stdout = captured_output
            success = self.game.scan_area(-1, 0)
            self.assertTrue(success)
            self.assertEqual(self.game.action_count, 0)
            output_text = captured_output.getvalue()
            self.assertIn("Invalid coordinates", output_text)

            captured_output = io.StringIO()
            sys.stdout = captured_output
            success = self.game.scan_area(self.grid_width, 0)
            self.assertTrue(success)
            self.assertEqual(self.game.action_count, 0)
            output_text = captured_output.getvalue()
            self.assertIn("Invalid coordinates", output_text)
        finally:
            sys.stdout = original_stdout

    def test_scan_area_already_scanned(self) -> None:
        original_stdout = sys.stdout
        try:
            x, y = 0, 0
            while (x, y) in self.game.hazard_locations:
                x, y = 1, 1

            dummy_output = io.StringIO()
            sys.stdout = dummy_output
            self.game.scan_area(x, y)

            captured_output = io.StringIO()
            sys.stdout = captured_output
            actions_before = self.game.action_count
            success = self.game.scan_area(x, y)

            self.assertTrue(success)
            self.assertEqual(self.game.action_count, actions_before)
            output_text = captured_output.getvalue()
            self.assertIn("already been scanned", output_text)
        finally:
            sys.stdout = original_stdout

    def test_game_won(self) -> None:
        test_game = AbandonedSpaceStation(grid_width=2, grid_height=2, hazard_count=0)
        test_game.hazard_locations = {(1, 1)}
        self.assertFalse(test_game.is_victorious)

        test_game.scan_area(0, 0)
        test_game.scan_area(0, 1)
        test_game.scan_area(1, 0)

        # Check if the game is won after scanning all safe areas
        self.assertTrue(
            test_game.is_victorious,
            "Game was not recognized as won despite all safe areas being scanned",
        )

    @patch("exam.source.helpers.clear_terminal")
    def test_play_validation(self, _mock_clear: MagicMock) -> None:
        test_game = AbandonedSpaceStation(grid_width=5, grid_height=5, hazard_count=0)
        test_game.hazard_locations = {(3, 3)}

        # Mock the input and process_coordinates functions together
        with patch("builtins.input", side_effect=["2 2", "q"]) as mock_input:
            # Set up process_coordinates to give valid responses for first input and quit for second
            with patch("exam.source.game.process_coordinates") as mock_process:
                mock_process.side_effect = [
                    (True, (2, 2), ""),  # First call: valid coordinates
                    (True, None, ""),  # Second call: quit
                ]

                # Mock the scan_area to avoid actually scanning
                with patch.object(
                    test_game, "scan_area", return_value=True
                ) as mock_scan:
                    # Mock print to avoid terminal output
                    with patch("builtins.print"):
                        test_game.play()

                        # Verify our mocks were called correctly
                        mock_input.assert_has_calls(
                            [
                                call("Enter coordinates (x y) or 'q' to quit: "),
                                call("Enter coordinates (x y) or 'q' to quit: "),
                            ]
                        )
                        mock_process.assert_has_calls(
                            [call("2 2", 5, 5), call("q", 5, 5)]
                        )
                        mock_scan.assert_called_once_with(2, 2)

    @patch("exam.source.helpers.clear_terminal")
    def test_play_invalid_input(self, _mock_clear: MagicMock) -> None:
        test_game = AbandonedSpaceStation(grid_width=5, grid_height=5, hazard_count=0)
        test_game.hazard_locations = {(3, 3)}

        # Create a more controlled test with specific inputs and process_coordinates responses
        with patch("builtins.input", side_effect=["invalid", "2 2", "q"]) as mock_input:
            with patch("exam.source.game.process_coordinates") as mock_process:
                mock_process.side_effect = [
                    (False, None, "Error message"),  # First call: invalid input
                    (True, (2, 2), ""),  # Second call: valid coordinates
                    (True, None, ""),  # Third call: quit
                ]
                with patch("builtins.print"):
                    with patch.object(
                        test_game, "scan_area", return_value=True
                    ) as mock_scan:
                        test_game.play()

                        # Verify all expected calls happened
                        mock_input.assert_has_calls(
                            [
                                call("Enter coordinates (x y) or 'q' to quit: "),
                                call("Enter coordinates (x y) or 'q' to quit: "),
                                call("Enter coordinates (x y) or 'q' to quit: "),
                            ]
                        )
                        mock_process.assert_has_calls(
                            [call("invalid", 5, 5), call("2 2", 5, 5), call("q", 5, 5)]
                        )
                        mock_scan.assert_called_once_with(2, 2)


if __name__ == "__main__":
    unittest.main()
