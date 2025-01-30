"""
Init file for the tests package.

This allows pytest to recognize the `tests` directory as a Python package.
"""

import sys
import os

# Get the absolute path of the project directory
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the project directory to sys.path so test modules can find the main package
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)
