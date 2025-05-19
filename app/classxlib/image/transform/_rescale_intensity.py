"""Rescales the intensity range of an image to a new range by stretching or shrinking it."""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np
from .. import analysis

__all__ = ['rescale_intensity']

def rescale_intensity(input_image:np.ndarray,
                      old_range:tuple=None,
                      new_range:tuple=None,
                      target_dtype:np.dtype=np.float32,
                      copy:bool=True,
                      mask:np.ndarray=None)->np.ndarray:
    """Rescales the intensity range of an image to a new range by stretching or shrinking it.

    Args:
        input_image (np.ndarray): The input image to rescale.
        old_range (tuple),(old_min,old_max): Tuple value of the
        old image data range. If None
        will use datatype range. Defaults to None.
        new_range (tuple),(new_min,new_max): Tuple value of the new
        image data range that will be scaled to. If None
        will use datatype range. Defaults to None.
        target_dtype (np.dtype): The target datatype of the image after rescaling.

    Raises:
        TypeError: If the input_image is not an ndarray
        ValueError: If the input_image is not a integer or float dtype

    Returns:
        np.ndarray: Rescaled image
    """
    try:
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("input image needs to be an ndarray")

        # Checking if the ranges were defined if not assigns
        # the range values as the datatype max/min
        if old_range is None:
            old_range = analysis.get_dtype_range(input_image.dtype)
        if new_range is None:
            new_range = analysis.get_dtype_range(target_dtype)

        # Converting the datatypes of images to their max
        # This is done to avoid potential data overflow when rescaling the image
        if np.issubdtype(input_image.dtype, np.integer):
            input_image = input_image.astype(np.int64)
        elif np.issubdtype(input_image.dtype, np.floating):
            input_image = input_image.astype(np.float64)
        else:
            raise ValueError("Error: input_image must be an integer or float dtype")

        # Assigning range variables
        old_min = old_range[0]
        old_max = old_range[1]
        new_min = new_range[0]
        new_max = new_range[1]

        # Copy the image before starting since
        # numpy arrays sync changes across variables
        input_image = input_image.copy() if copy is True else input_image

        # Logic flow to rescale the image
        # Converts the appropriate datatype as well
        if mask is not None:
            input_image = np.where(mask == True,
                                   (((input_image - old_min)
                                     / (old_max - old_min))
                                    * (new_max - new_min)
                                    + new_min),
                                   input_image).astype(target_dtype)
        else:
            input_image = (((input_image - old_min)
                        / (old_max - old_min))
                       * (new_max - new_min)
                       + new_min).astype(target_dtype)

    except (RuntimeError, ValueError,
            TypeError) as error:
        print("Image Rescaling failed")
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
    return input_image
