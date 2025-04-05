"""
Unit tests for the main functions in main.py
"""
# pylint: disable=C

import unittest
from unittest.mock import patch, MagicMock
import io
from contextlib import redirect_stdout
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from exam.source.main import _get_custom_settings, main, handle_game_interrupt


class TestGetCustomSettings(unittest.TestCase):
    @patch("builtins.input")
    def test_valid_inputs(self, mock_input):
        # Simulate valid user inputs
        mock_input.side_effect = ["8", "10", "15"]
        width, height, hazards = _get_custom_settings()
        self.assertEqual(width, 8)
        self.assertEqual(height, 10)
        self.assertEqual(hazards, 15)

    @patch("builtins.input")
    def test_invalid_width_then_valid(self, mock_input):
        # Simulate invalid width, then valid inputs
        mock_input.side_effect = ["3", "7", "8", "10"]
        with redirect_stdout(io.StringIO()) as f:
            width, height, hazards = _get_custom_settings()
        output = f.getvalue()
        self.assertIn("Width must be at least 5", output)
        self.assertEqual(width, 7)
        self.assertEqual(height, 8)
        self.assertEqual(hazards, 10)

    @patch("builtins.input")
    def test_invalid_height_then_valid(self, mock_input):
        # Simulate valid width, invalid height, then valid height
        mock_input.side_effect = ["6", "2", "8", "10"]
        with redirect_stdout(io.StringIO()) as f:
            width, height, hazards = _get_custom_settings()
        output = f.getvalue()
        self.assertIn("Height must be at least 5", output)
        self.assertEqual(width, 6)
        self.assertEqual(height, 8)
        self.assertEqual(hazards, 10)

    @patch("builtins.input")
    def test_non_numeric_input(self, mock_input):
        # Simulate non-numeric input
        mock_input.side_effect = ["abc", "6", "xyz", "7", "def", "5"]
        with redirect_stdout(io.StringIO()) as f:
            width, height, hazards = _get_custom_settings()
        output = f.getvalue()
        self.assertIn("Please enter a whole number", output)
        self.assertEqual(width, 6)
        self.assertEqual(height, 7)
        self.assertEqual(hazards, 5)

    @patch("builtins.input")
    def test_too_many_hazards(self, mock_input):
        # Simulate too many hazards, then valid number
        mock_input.side_effect = ["5", "5", "30", "10"]
        with redirect_stdout(io.StringIO()) as f:
            width, height, hazards = _get_custom_settings()
        output = f.getvalue()
        self.assertIn("maximum of", output)
        self.assertEqual(width, 5)
        self.assertEqual(height, 5)
        self.assertEqual(hazards, 10)

    @patch("builtins.input")
    def test_negative_hazards(self, mock_input):
        # Simulate negative number of hazards
        mock_input.side_effect = ["5", "5", "-3", "5"]
        with redirect_stdout(io.StringIO()) as f:
            _, _, hazards = _get_custom_settings()
        output = f.getvalue()
        self.assertIn("There must be at least 1 hazard", output)
        self.assertEqual(hazards, 5)


class TestMain(unittest.TestCase):
    @patch("exam.source.main.clear_terminal")
    @patch("builtins.input")
    @patch("exam.source.main.AbandonedSpaceStation")
    def test_default_settings(self, mock_game_class, mock_input, mock_clear):
        # Test game with default settings
        mock_input.return_value = "n"
        mock_game_instance = MagicMock()
        mock_game_class.return_value = mock_game_instance

        main()

        mock_clear.assert_called_once()
        mock_game_class.assert_called_once_with()
        mock_game_instance.play.assert_called_once()

    @patch("exam.source.main.clear_terminal")
    @patch("exam.source.main._get_custom_settings")
    @patch("builtins.input")
    @patch("exam.source.main.AbandonedSpaceStation")
    def test_custom_settings(
        self, mock_game_class, mock_input, mock_get_settings, mock_clear
    ):
        # Test game with custom settings
        mock_input.return_value = "y"
        mock_get_settings.return_value = (10, 12, 20)
        mock_game_instance = MagicMock()
        mock_game_class.return_value = mock_game_instance

        main()

        mock_clear.assert_called_once()
        mock_get_settings.assert_called_once()
        mock_game_class.assert_called_once_with(10, 12, 20)
        mock_game_instance.play.assert_called_once()

    @patch("exam.source.main.clear_terminal")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_invalid_customization_input(self, mock_print, mock_input, _):
        # Test invalid input for customization question
        mock_input.side_effect = ["invalid", "n"]

        with patch("exam.source.main.AbandonedSpaceStation") as mock_game_class:
            mock_game_instance = MagicMock()
            mock_game_class.return_value = mock_game_instance
            main()

        # Check if error message was displayed
        mock_print.assert_any_call("Please enter 'y' or 'n'.")


class TestHandleGameInterrupt(unittest.TestCase):
    @patch("builtins.print")
    @patch("sys.exit")
    def test_handle_game_interrupt(self, mock_exit, mock_print):
        # Test handling of game interruptions
        handle_game_interrupt()
        mock_print.assert_called_once_with(
            "\nGame was interrupted by the user. Goodbye!"
        )
        mock_exit.assert_called_once_with(0)


class TestMainWithInterrupt(unittest.TestCase):
    def test_keyboard_interrupt_handling(self):
        # Directly test that KeyboardInterrupt is properly handled
        with patch("sys.exit") as mock_exit:
            try:
                raise KeyboardInterrupt()
            except KeyboardInterrupt:
                handle_game_interrupt()

            # Verify sys.exit was called with the correct argument
            mock_exit.assert_called_once_with(0)


if __name__ == "__main__":
    unittest.main()
