"""Submodule for stretching the contrast of images"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np

# Local Library Imports
from ..transform import rescale_intensity

__all__ = ['stretch_image_contrast']

def stretch_image_contrast(input_image:np.ndarray,
                           percentile_range:tuple=(2.0,98.0))->np.ndarray:
    """Stretches the image contrast across a range.

    Args:
        input_image (np.ndarray): The image array to stretch the contrast
        percentile_range (tuple(lower, upper)): The percentile range
        to stretch the image by.
        Defaults to (2.0,98.0) aka. (2%, 98%)

    Raises:
        TypeError: If the image array is not an np.ndarray

    Returns:
        np.ndarray: The image after stretching the contrast
    """
    try:
        # Verifying arguments
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("input image needs to be an ndarray")

        # Getting the lower and upper percentile intensity values
        lower, upper = np.percentile(input_image, percentile_range)

        # Checking which datatype the image is before stretching it's contrast
        if np.issubdtype(input_image, np.floating):
            # Float images standardly use range of 0-1 so we need to define that as
            # the old range
            input_image = rescale_intensity(input_image,
                                            old_range=(0,1),
                                            new_range=(lower,upper),
                                            target_dtype=input_image.dtype)
        else:
            # If it's a integer datatype we don't need to define the old range
            # Since they normally use the full data range
            input_image = rescale_intensity(input_image,
                                            new_range=(lower,upper),
                                            target_dtype=input_image.dtype)
        return input_image
    except (ValueError, TypeError,
            RuntimeError, RuntimeWarning) as error:
        print("Image Contrast Stretching Failed")
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return np.zeros(input_image.shape)
