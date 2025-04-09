"""Takes an image array and converts the dimensions based on the vertical and horizontal scales."""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
import cv2
import numpy as np

__all__ = ['resize_image']

def resize_image(input_image:np.ndarray,
                 vertical_scale:int=0,
                 horizontal_scale:int=0) -> np.ndarray:
    """Takes an image array and converts the dimensions based on the vertical and horizontal scales.

    Args:
        input_image (np.ndarray): RGB image in an array format
        vertical_scale (int, optional): Vertical pixel dimension to
        scale to if 0 will scale alongside horizontal. Defaults to 0.
        horizontal_scale (int, optional): Horizontal pixel dimension
        to scale to if 0 will scale alongside vertical. Defaults to 0.

    Raises:
        TypeError: If the input_image is not an ndarray
        TypeError: If the vertical scale is not of type int
        TypeError: If the horizontal scale is not of type int

    Returns:
        np.ndarray: returns the image resized based on the scaling factors
    """
    try:
        # Verifying arguments
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("input image needs to be an ndarray")
        if len(input_image.shape) != 3:
            raise ValueError("image dimension invalid")
        if not isinstance(vertical_scale, int):
            raise TypeError("vertical scale needs to be of type int")
        if not isinstance(horizontal_scale, int):
            raise TypeError("horizontal scale needs to be of type int")

        # If the image scales are 0 then no argument was given so just return the image
        if(vertical_scale == 0 and horizontal_scale == 0):
            return input_image

        # If vertical scale exists but no horizontal scale
        # exists scale the image vertically and the horizontal will be scaled proportionally
        if(horizontal_scale == 0 and vertical_scale != 0):
            resize_dim = (int(input_image.shape[1] * (vertical_scale/input_image.shape[0])),
                          int(input_image.shape[0] * (vertical_scale/input_image.shape[0])))
            resized_image = cv2.resize(input_image, resize_dim, interpolation=cv2.INTER_AREA)

        # If horizontal scale exists but no vertical scale
        # exists scale the image horizontally and the vertical will be scaled proportionally
        elif(horizontal_scale != 0 and vertical_scale == 0):
            resize_dim = (int(input_image.shape[1] * (horizontal_scale/input_image.shape[1])),
                          int(input_image.shape[0] * (horizontal_scale/input_image.shape[1])))
            resized_image = cv2.resize(input_image, resize_dim, interpolation=cv2.INTER_AREA)

        # Both horizontal and vertical scale exist so scale them accordingly.
        # This may result in unusual image visuals due to shrinking/stretching.
        else:
            resize_dim = (int(input_image.shape[1] * (horizontal_scale/input_image.shape[1])),
                          int(input_image.shape[0] * (vertical_scale/input_image.shape[0])))
            resized_image = cv2.resize(input_image, resize_dim, interpolation=cv2.INTER_AREA)

        return resized_image
    # This is added because cv2 is not recognized properly
    # pylint: disable=catching-non-exception
    except (RuntimeError, ValueError,
            TypeError, cv2.error) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
