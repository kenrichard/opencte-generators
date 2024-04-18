"""Module providing helpers for command line interface"""

from pathlib import Path


def validate_file(arg):
    """Function to validate a fine CLI parameter"""
    if (file := Path(arg)).is_file():
        return file
    raise FileNotFoundError(arg)
