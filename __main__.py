"""
Main entry point for running test coverage on the Abandoned Space Station game.

This module discovers and runs all tests while collecting code coverage data.
"""

import os
import sys
import unittest
import coverage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def run_tests_with_coverage() -> None:
    """
    Run all test cases with coverage analysis.

    Discovers all tests in the 'tests' directory and runs them while
    tracking code coverage. Generates a coverage report when complete.
    """
    cov = coverage.Coverage(
        source=["exam.source"],
        omit=["*/__init__.py", "*/__main__.py", "*/test_*.py"],
    )

    cov.start()

    print("=" * 70)
    print("Running tests with coverage for Abandoned Space Station")
    print("=" * 70)

    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), "tests")
    suite = loader.discover(start_dir, pattern="test_*.py")

    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(suite)

    cov.stop()

    print("\n" + "=" * 70)
    print("Test Results:")
    print(f"Tests Run: {test_result.testsRun}")
    print(f"Failures: {len(test_result.failures)}")
    print(f"Errors: {len(test_result.errors)}")
    print(f"Skipped: {len(test_result.skipped)}")

    print("\n" + "=" * 70)
    print("Coverage Report:")
    cov.report()

    html_dir = os.path.join(os.path.dirname(__file__), "coverage_html")
    cov.html_report(directory=html_dir)
    print(f"\nDetailed HTML coverage report generated in: {html_dir}")

    print("\n" + "=" * 70)

    if test_result.failures or test_result.errors:
        sys.exit(1)


if __name__ == "__main__":
    run_tests_with_coverage()
