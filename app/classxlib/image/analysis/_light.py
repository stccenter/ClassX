"""ClassX Module for light analysis related functions"""
# Python Standard Library Imports
import traceback
import math

# Python Third Party Imports
import numpy as np

# Local Library Imports
from .. import transform
from .._convert import rgb2gray
from ._dtype import get_dtype_range

__all__ = ['get_image_light', 'is_image_black']

def get_image_light(input_image:np.ndarray,
                    remove_background:bool=True,
                    background_threshold:float=0.01,
                    data_range:tuple=None) -> float:
    """Gets the `perceived brightness` of an image, image can be single channel
    or RGB

    Args:
        input_image (np.ndarray): image array to analyze
        remove_background (bool, optional): Check to remove pixels of a certain intensity.
        Defaults to True.
        background_threshold (float, optional): Pixel threshold to remove from
        analysis. This is ignored if `remove_background` is `False` Defaults to 0.01.
        data_range (tuple, optional): Intensity range of image, used if image range does not
        match the datatype range. If None will use image datatype range. Defaults to None.

    Raises:
        TypeError: If input image is not an np.ndarray.

    Returns:
        float: Returns float value in range 0.0-1.0, 0 being completely dark,
        1 being completely bright
    """
    try:
        # Verifying arguments
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("Error: Input image needs to be an ndarray")

        # Checking if a specified data range was defined
        # If not set the range to the image datatype limits
        if data_range is None:
            data_range = get_dtype_range(input_image.dtype)

        # Normalizing the data before checking image light
        input_image = transform.rescale_intensity(input_image=input_image,
                                                    old_range=data_range,
                                                    new_range=(0,1),
                                                    target_dtype=np.float32)

        # Checking if it's a single channel image
        if len(input_image.shape) == 2:
            r,g,b = input_image,input_image,input_image
        else:
            # Splitting color channels into 3
            r,g,b = input_image[:,:,0], input_image[:,:,1], input_image[:,:,2]

        # Checking if function should remove pixels within a certain intensity
        if remove_background is False:
            background_threshold = -1

        # Computes the "perceived brightness" of the image
        brightness = math.sqrt(0.241*(np.mean(r,where=r>background_threshold)**2)
                                + 0.691*(np.mean(g,where=g>background_threshold)**2)
                                + 0.068*(np.mean(b,where=b>background_threshold)**2))
        # if average_light > 0.627:
        #     light = 'bright'
        # elif average_light > 0.392:
        #     light = 'medium'
        # else:
        #     light = 'poor'
        print(f'lighting condition is {brightness}')
        return brightness
    except (TypeError, ValueError,
            RuntimeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None

def is_image_black(input_image:np.ndarray,
                   percent_threshold:float=0.80) -> bool:
    """Checks if an image is black/void dependending on
    the specified percentage and returns a bool value accordingly

    Args:
        input_image (np.ndarray): The image to be checked
        percent_threshold (float, optional): What percent of the image must be black
        to be determined a black/void image. Defaults to 0.80 or 80%.

    Returns:
        bool: True if image falls within black threshold, False if it doesn't
    """
    try:
        # Verifying Arguments
        if not isinstance(input_image, np.ndarray):
            raise TypeError("input_image needs to be an ndarray")
        if not isinstance(percent_threshold, float):
            raise TypeError("percent_threshold needs to be a float")
        if percent_threshold < 0 or percent_threshold > 1.0:
            raise ValueError("Percent threshold needs to be in range 0-1")

        if input_image.ndim == 3:
            grayscale_image = rgb2gray(input_image)
        else:
            grayscale_image = input_image

        # Getting black pixels in image
        total_pixels = grayscale_image.shape[0] * grayscale_image.shape[1]
        black_pixels = total_pixels - np.count_nonzero(grayscale_image)
        if black_pixels/total_pixels > percent_threshold:
            return True

        return False
    except (RuntimeError, ValueError,
            TypeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return False
