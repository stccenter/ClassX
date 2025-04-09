"""Module for reading segment images into memory"""

# Python Standard Library Imports
import traceback
from ctypes import c_uint32

# Python Third Party Imports
import numpy as np
import h5py

# Local Library Imports
from ..file import merge_directory

__all__ = ["read_segment_image"]


def read_segment_image(
    segment_image_path: str, base_directory: str = ""
) -> tuple[np.ndarray, np.ndarray]:
    """Loads a segment image mask from a segment image object

    Args:
        segment_image_path (str): File directory for the segment image
        base_directory (str, optional): Base Directory to
        append for the file path. Defaults to "".

    Raises:
        TypeError: If the segment_image_path is not of type string
        TypeError: If the base_directory is not of type string

    Returns:
        tuple: 2D Array of segment image mask and segment info
    """
    try:
        # Verifying arguments
        if not isinstance(segment_image_path, str):
            raise TypeError("TypeError: segment_image_path must be of type string.")
        if not isinstance(base_directory, str):
            raise TypeError("TypeError: base_directory must be of type string.")

        if base_directory != "":
            # Formatting the path to the image
            segment_image_path = merge_directory(base_directory, segment_image_path)

        segment_info = None
        # Legacy Loading
        if segment_image_path.endswith(".txt"):
            # Loading the mask
            segment_image = np.loadtxt(segment_image_path)
        elif segment_image_path.endswith(".h5"):
            h5_file = h5py.File(segment_image_path, "r")
            segment_image = h5_file["segment_data"][:]
            # Converting the datatype to ensure consistent processing
            segment_image = np.ndarray.astype(segment_image, c_uint32)
            segment_info = h5_file["segment_info"][:]

        return segment_image, segment_info
    except (OSError, RuntimeError, ValueError, TypeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
