"""Module for segmenting images using the watershed algorithm"""
# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np
from skimage.segmentation import watershed
from skimage.morphology import disk
from skimage.filters import rank
from scipy import ndimage as ndi

# Local Library Imports
from classxlib.image import rgb2gray

__all__ = ['watershed_transformation']

def watershed_transformation(input_image:np.ndarray,
                             gausian_kernal_size:float,
                             gradient_cut:float) -> np.ndarray:
    """Performs a segmentation on an image array using the watershed algorithm
    before segmentation there is a gaussian smoothing applied and thresholding
    through an image gradient

    Args:
        input_image (np.ndarray): The image array from which the segmentation
        will be performed
        gausian_kernal_size (float): The size of the gausian disk used for smoothing
        gradient_cut (float): The threshold for the gradient cut

    Raises:
        TypeError: If the input image is not an np.ndarray

    Returns:
        np.ndarray: A single channel array mask with each unique value representing
        a segment.
    """
    try:
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("input image needs to be an ndarray")

        # Converting the image to grayscale
        gray_image = rgb2gray(input_image)

        # Disk for smoothing an image
        gausian_disk = disk(gausian_kernal_size)

        # Smoothing the image using a gausian smoothing algorithm
        denoised_image = rank.median(gray_image, gausian_disk)

        # Getting the gradient of the image
        gradient = rank.gradient(denoised_image, gausian_disk)

        # If the threshold for gradient markers is too high
        # the image will be blank so we increase the minimum
        if np.min(gradient) >= gradient_cut:
            print("NOTICE: GRADIENT IMAGE MINIMUM VALUE IS ABOVE GRADIENT CUT",
                  "ADJUSTING VALUES TO AVOID BLANK IMAGE")
            print("IMAGE GRADIENT MINIMUM:",
                  np.min(gradient),
                  "IMAGE GRADIENT CUT/FEATURE SEPARATION:",
                  gradient_cut)
            gradient = gradient - np.min(gradient)

        # Generating marker points
        markers = gradient < gradient_cut
        markers = ndi.label(markers)[0]  # Label each marker 1,2,3...

        # process the watershed on gradient layer
        return watershed(gradient, markers)
    except (ValueError, IndexError,
            TypeError, RuntimeError,
            RuntimeWarning) as error:
        print("Watershed transformation failed")
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
