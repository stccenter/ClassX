"""Module for checking the range of image datatypes"""
# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np

__all__ = ['get_dtype_range']

def get_dtype_range(dtype: np.dtype) -> tuple:
    """Gets the data range of an image

    Args:
        dtype (np.dtype): The dtype of the image

    Returns:
        tuple: Returns tuple of the range (min, max)
    """
    try:

        if np.issubdtype(dtype, np.integer):
            dtype_range = (np.iinfo(dtype).min,np.iinfo(dtype).max)
        else:
            dtype_range = (np.finfo(dtype).min,np.finfo(dtype).max)
        return dtype_range
    except TypeError as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
