"""Module for segmenting images using the
felzenszwalb algorithm"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np
from skimage.segmentation import felzenszwalb

__all__ = ['felzenszwalb_transformation']

def felzenszwalb_transformation(input_image:np.ndarray,
                                scale:float,
                                minimum_size:int,
                                gausian_kernal_size:float=0.7)-> np.ndarray:
    """Performs a segmentation on an image array using the felzenszwalb algorithm

    Args:
        input_image (np.ndarray): The image array from which the segmentation
        will be performed
        scale (float): Scaling factor for size of segment clusters
        minimum_size (int): Minmium size of segments, enforced using post processing
        gausian_kernal_size (float): The kernal size for the gaussian smoothing.
        Defaults to 0.7.

    Raises:
        TypeError: If the input image is not an np.ndarray

    Returns:
        np.ndarray: A single channel array mask with each unique value representing
        a segment.
    """
    try:
        # Verifying arguments
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("input image needs to be an ndarray")
        scale = scale * 100
        minimum_size = int(minimum_size * 20)
        return felzenszwalb(input_image,
                            scale=float(scale),
                            min_size=int(minimum_size),
                            sigma=float(gausian_kernal_size))
    except (ValueError, IndexError,
            TypeError, RuntimeError,
            RuntimeWarning) as error:
        print("felzenszwalb transformation failed")
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
