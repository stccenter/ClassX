"""Joins two file paths together in a cross-platform manner."""

# Python Standard Library Imports
import os

__all__ = ["merge_directory"]


def merge_directory(base_dir: str, sub_dir: str = "") -> str:
    """Joins two file paths together in a cross-platform manner.

    Args:
        base_dir (str): Base directory to join together.
        sub_dir (str): Sub directory or file name to join with base.

    Raises:
        ValueError: If either base_dir or sub_dir is not a string.

    Returns:
        str: A combined file path.
    """
    # Verifying the function arguments
    if not isinstance(base_dir, str) or not isinstance(sub_dir, str):
        raise ValueError("Both base_dir and sub_dir must be strings.")

    # Returns the directory in the correct OS format
    return os.path.join(base_dir, sub_dir).replace("\\", "/").rstrip("/")
