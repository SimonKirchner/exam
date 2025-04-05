"""
Unit tests for the helper functions in helpers.py
"""
# pylint: disable=C

import unittest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from exam.source.helpers import clear_terminal, process_coordinates


class TestHelpers(unittest.TestCase):
    def test_clear_terminal(self) -> None:
        with patch("os.name", "nt"), patch("os.system") as mock_system:
            clear_terminal()
            mock_system.assert_called_once_with("cls")
        with patch("os.name", "posix"), patch("os.system") as mock_system:
            clear_terminal()
            mock_system.assert_called_once_with("clear")

    def test_process_coordinates_valid(self) -> None:
        success, coordinates, error = process_coordinates("2 3", 5, 5)
        self.assertTrue(success)
        self.assertEqual(coordinates, (2, 3))
        self.assertEqual(error, "")

        success, coordinates, error = process_coordinates("q", 5, 5)
        self.assertTrue(success)
        self.assertIsNone(coordinates)
        self.assertEqual(error, "")

        success, coordinates, error = process_coordinates("Q", 5, 5)
        self.assertTrue(success)
        self.assertIsNone(coordinates)
        self.assertEqual(error, "")

        success, coordinates, error = process_coordinates("  1 2  ", 5, 5)
        self.assertTrue(success)
        self.assertEqual(coordinates, (1, 2))
        self.assertEqual(error, "")

    def test_process_coordinates_invalid(self) -> None:
        success, coordinates, error = process_coordinates("1", 5, 5)
        self.assertFalse(success)
        self.assertIsNone(coordinates)
        self.assertTrue(len(error) > 0)

        success, coordinates, error = process_coordinates("1 2 3", 5, 5)
        self.assertFalse(success)
        self.assertIsNone(coordinates)
        self.assertTrue(len(error) > 0)

        success, coordinates, error = process_coordinates("a b", 5, 5)
        self.assertFalse(success)
        self.assertIsNone(coordinates)
        self.assertTrue(len(error) > 0)

        success, coordinates, error = process_coordinates("5 5", 5, 5)
        self.assertFalse(success)
        self.assertIsNone(coordinates)
        self.assertTrue(len(error) > 0)

        success, coordinates, error = process_coordinates("-1 3", 5, 5)
        self.assertFalse(success)
        self.assertIsNone(coordinates)
        self.assertTrue(len(error) > 0)


if __name__ == "__main__":
    unittest.main()
