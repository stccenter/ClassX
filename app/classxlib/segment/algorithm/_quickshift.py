"""Module for segmenting images using the
quickshift algorithm"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np
from skimage.segmentation import quickshift

__all__ = ['quickshift_transformation']

def quickshift_transformation(input_image:np.ndarray,
                              kernel_size:float=3,
                              max_distance:float=10,
                              gausian_kernal_size:float=0.7,
                              ratio:float=0.75)->np.ndarray:
    """Performs a segmentation on an image array using the quickshift algorithm

    Args:
        input_image (np.ndarray): The image array from which the segmentation
        will be performed
        kernel_size (float, optional): The kernal size for the algorithm to consider, references
        how many surrounding pixels are checked for determining boundaries. Defaults to 3.
        max_distance (float, optional): The max distance of of cluster centers. Defaults to 10.
        gausian_kernal_size (float, optional): The kernal size for the gaussian smoothing.
        Defaults to 0.7.
        ratio (float, optional, between 0 and 1): Balances color-space proximity
        and image-space proximity. Higher values give more weight to
        color-space. Defaults to 0.75.

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
        return quickshift(input_image,
                          kernel_size=kernel_size,
                          max_dist=max_distance,
                          ratio=ratio,
                          sigma=gausian_kernal_size)
    except (ValueError, IndexError,
            TypeError, RuntimeError,
            RuntimeWarning) as error:
        print("Quickshift transformation failed")
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
