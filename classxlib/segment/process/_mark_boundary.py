"""Submodule for marking boundaries of segments on images"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np
from skimage.segmentation import mark_boundaries

# Python Local Library Imports
from ...image.transform import rescale_intensity

__all__ = ['mark_segment_boundaries']

def mark_segment_boundaries(input_image:np.ndarray,
                            segment_image:np.ndarray,
                            light:str=None) -> np.ndarray:
    """Marks the boundaries of a segment image mask onto a
    an image of same shape

    Args:
        input_image (np.ndarray): The image to mark, must be a numpy array
        segment_image (np.ndarray): Segment image mask to used to mark bounaries
        light (str, optional): lighting condition to determine
        boundary color. Defaults to None.

    Raises:
        TypeError: If the input image is not an numpy array

    Returns:
        np.ndarray: Returns an 8 bit image with the boundaries marked
    """
    try:
        # Verifying arguments
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("input image needs to be an ndarray")

        # Colors the segment boundaries onto the original image
        # Colors it differently based off lighting
        # NOTE not all images have a light condition
        if light == 'bright':
            marked_image = mark_boundaries(input_image, segment_image,
                                            color=(0, 0, 1))
        elif light == 'medium':
            marked_image = mark_boundaries(input_image, segment_image,
                                            color=(0, 0, 1))
        else:
            marked_image = mark_boundaries(input_image, segment_image,
                                            color=(0.65, 0.85, 1))

        # Rescaling the image back to a 8 bit image
        # This is done because mark boundaries returns
        # A float image
        marked_image = rescale_intensity(input_image=marked_image,
                                        old_range=(0,1),
                                        new_range=(0,255),
                                        target_dtype=np.uint8)

        return marked_image
    except (ValueError, IndexError,
            TypeError, RuntimeError,
            RuntimeWarning) as error:
        print("Marking Segment Boundaries failed")
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
