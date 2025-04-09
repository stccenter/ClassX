"""Validates the existence of a given directory,
    creating it if it does not exist."""

# Python Standard Library Imports
import os
import traceback
import logging

__all__ = ["verify_directory"]


def verify_directory(dir_: str, create_dir: bool = True) -> bool:
    """Validates the existence of a given directory,
    creating it if it does not exist.

    Args:
        dir_ (str): The file path of the directory to be validated.
        create_dir(bool): If True will create the directory
        if it does not exist. Defaults to True.
    Raises:
        ValueError: If directory argument is not a string.

    Returns:
        bool: Returns True if the directory exists or
        was successfully created, and False if an error occurs.
    """
    # Verifying function arguments
    if not isinstance(dir_, str):
        raise TypeError("directory argument must be of type string")

    #try:
    # Checking if the directory exists already
    dir_exists = os.path.isdir(dir_)

    # Create directory if it doesn't exist
    # and create_dir is true
    if dir_exists is False and create_dir is True:
        logging.info("Directory: %s does not exist, creating now.", dir_)
        os.makedirs(dir_, exist_ok=True)
        dir_exists = os.path.isdir(dir_)

    # Catching a more relevant exception
    # and a generic exception for unexpected errors
    # except (OSError, ValueError, TypeError) as error:
    #     logging.error("Error: %s", error)
    #     traceback.print_exc()
    #     return False
    return dir_exists
