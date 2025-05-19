"""ClassX image module for converting image data into new formats"""
# Python Standard Library Imports
import traceback
import base64

# Python Third Party Imports
import cv2
import numpy as np

__all__ = ['image_as_b64', 'rgb2gray']

def image_as_b64(input_image:np.ndarray,
                 reverse_channel:bool=True)->str:
    """Converts an input image array to Base64 Image

    Args:
        input_image (np.ndarray): An image array to be converted
        reverse_channel (bool): Condition whether to reverse the
        color channels or not before encoding since OpenCV will
        reverse them. Defaults to True
    Raises:
        TypeError: If input is not an array
        ValueError: If input image is incorrect shape

    Returns:
        str: Base64 encoded string of image
    """
    try:
        # Checking if the input image is the correct type
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("Error: Input image needs to be an ndarray")
        if len(input_image.shape) != 3:
            raise ValueError("Error: Incorrect shape for input image")

        # Reversing the color channels
        if reverse_channel is True:
            input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

        # Encoding the image
        buffer = cv2.imencode('.png', input_image)[1]

        # Encoding the buffer into base64 text
        return base64.b64encode(buffer).decode('utf-8')
    # pylint: disable=catching-non-exception
    except (RuntimeError, TypeError,
            cv2.error, ValueError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None

def rgb2gray(input_image:np.ndarray) -> np.ndarray:
    """Converts RGB image to grayscale

    Args:
        input_image (np.ndarray): RGB image to convert

    Raises:
        TypeError: If the image is not an np.ndarray
        ValueError: If the image is the incorrect shape

    Returns:
        np.ndarray: Returns grayscale array
    """
    try:
        # Verifying Arguments
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("Error: Input image needs to be an ndarray")
        if len(input_image.shape) != 3:
            raise ValueError("Error: Incorrect shape for input image")

        # Converting image to grayscale
        return np.dot(input_image[...,:3], [0.2989, 0.5870, 0.1140])
    except (RuntimeError, TypeError,
            ValueError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return np.zeros(input_image.shape)
