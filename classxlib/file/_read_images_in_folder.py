"""Reads the files in a folder and returns
their names and directories in a tuple"""

# Python Standard Library Imports
import os

# Local Library Imports
from ._manage_directory import merge_directory


def read_images_in_folder(directory: str) -> list:
    """Reads the files in a folder and returns their names and directories in a tuple

    Args:
        directory (str): Path to the directory to read

    Returns:
        list: Tuple list of the images in the folder,
        ((file name 1, directory 1),(file name 2, directory 2),.....)
    """
    # Verifying the arguments
    if not isinstance(directory, str):
        raise TypeError("TypeError: directory argument must be of type string")

    # Show directory contents
    user_files = []
    for file in os.listdir(directory):
        file_path = merge_directory(directory, file)
        user_files.append([file, file_path])
    return user_files
