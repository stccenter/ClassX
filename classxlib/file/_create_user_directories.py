"""Generates user directories in a given directory
    for purposes of storing images and user data"""

# Python Standard Library Imports
import traceback

# Local Library Imports
from ._manage_directory import merge_directory
from ._verify_directory import verify_directory


__all__ = ["create_user_directories"]


def create_user_directories(base_dir: str, user_name: str) -> bool:
    """Generates user directories in a given directory
    for purposes of storing images and user data

    Args:
        base_dir (str): Base directory/folder to generate the sub directories in
        user_name (str): Name of user to generate directories under

    Raises:
        TypeError: If base directory is not a string
        TypeError: If username given is not a string

    Returns:
        bool: Returns True if succcessful and False if an error occurs in generating directories
    """
    # Validating arguments
    if not isinstance(base_dir, str):
        raise TypeError("TypeError: directory argument must be of type string")
    if not isinstance(user_name, str):
        raise TypeError("TypeError: user_name needs to be of type string")
    #try:

    # Where original image data is stored
    input_directory = merge_directory(base_dir, user_name + "/ReadGUI")

    # Where the processed original image data is stored
    processed_directory = merge_directory(base_dir, user_name + "/ProcessedImages")

    # Where all active writing directories are stored
    output_directory = merge_directory(base_dir, user_name + "/WriteGUI")

    # Where training datasets are exported to before zipping them
    export_directory = merge_directory(base_dir, user_name + "/export")

    # Directories to verify
    required_directories = [
        base_dir,
        input_directory,
        processed_directory,
        output_directory,
        export_directory,
    ]

    # The sub directories of the output directory
    output_sub_directories = [
        "HDF5",
        "ColorImages",
        "CropImages",
        "AutoCropImages",
        "SegmentImages",
        "MarkedImages",
        "TrainingFiles",
        "Models",
    ]

    # Adding all the sub directories to the verification list
    for directory in output_sub_directories:
        required_directories.append(merge_directory(output_directory, directory))

    # Making sure directories don't already exist before creation
    for directory in required_directories:
        verify_directory(directory)
    # except (TypeError, RuntimeError) as error:
    #     print("Error:", error)
    #     traceback.print_tb(error.__traceback__)
    #     return False

    return True
