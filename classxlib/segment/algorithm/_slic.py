"""Module for segmenting images using the
SLIC(Simple Linear Iterative Clustering) algorithm"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np
from skimage.segmentation import slic

__all__ = ['slic_transformation']

def slic_transformation(input_image:np.ndarray,
                       n_segments:int,
                       compactness:float,
                       gausian_kernal_size:float)->np.ndarray:
    """Performs a segmentation on an image array using the SLIC algorithm

    Args:
        input_image (np.ndarray): The image array from which the segmentation
        will be performed
        n_segments (int): Approximate number of segments to generate
        compactness (float): How compact segments should be the higher the value
        the more square segments will look
        gausian_kernal_size (float): The kernal size for the gaussian smoothing

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
        # We times this by 25 to increase the number of segments
        # This makes it easier to manage on the front-end UI
        n_segments = int(n_segments * 25)

        # Running the
        # SLIC(Simple Linear Iterative Clustering) Algorithm
        return slic(input_image,
                    n_segments=n_segments,
                    compactness=compactness,
                    start_label=1,
                    sigma=gausian_kernal_size)
    except (ValueError, IndexError,
            TypeError, RuntimeError,
            RuntimeWarning) as error:
        print("SLIC transformation failed")
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
