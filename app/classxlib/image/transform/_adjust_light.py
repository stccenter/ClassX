"""Image Submodule related to adjusting the lighting of images"""

# Python Third Party Imports
import numpy as np
from skimage.exposure import equalize_adapthist, equalize_hist
from skimage.util import img_as_uint, img_as_float
import cv2

# Local Library Imports
from ..utils import get_channel, set_channel

__all__ = ['equalize_image']

def equalize_image(input_image:np.ndarray,
                   method:int,
                   channel_axis:int=-1) -> np.ndarray:
    """Function for adjusting image lighting by equalizing it's
    histogram

    Args:
        input_image (np.ndarray): The image array to be equalized
        method (int): The method id for which algorithm to use

    Returns:
        np.ndarray: The image after it has been equalized
    """
    ndim = len(input_image.shape)

    # If method is 0 then just return the image
    if method == 0:
        return input_image
    # Method 1 Histogram Equalization
    if method == 1:
        input_image = _equalize_histogram(input_image,
                                          ndim=ndim,
                                          channel_axis=channel_axis)
    # Method 2 Adaptive Histogram Equalization
    if method == 2:
        input_image = _equalize_adaptive_histogram(input_image,
                                                   ndim=ndim,
                                                   channel_axis=channel_axis)
    # Method 3 Contrast Limited Adaptive Histogram Equalization
    if method == 3:
        input_image = _equalize_clahe_histogram(input_image,
                                                ndim=ndim,
                                                channel_axis=channel_axis)
    return input_image

def _equalize_histogram(input_image:np.ndarray,
                        ndim:int,
                        channel_axis:int=-1) -> np.ndarray:
    """Performs a standard histogram equalization

    Args:
        input_image (np.ndarray): The image array to equalize
        ndim (int): Number of dimensions in the image
        channel_axis (int, optional): Channel axis where
        the color channels are located. Defaults to -1.

    Returns:
        np.ndarray: The image after equalization
    """
    # Checking if it's a single channel image
    if ndim == 2:
        input_image = equalize_hist(input_image)
    else:
        # Looping through each color channel/band
        for band_index in range(input_image.shape[channel_axis]):
            # Retriving the band data
            band_data = get_channel(input_image=input_image,
                                    channel=band_index,
                                    channel_axis=channel_axis)

            # Equalizaing the band
            band_data = equalize_hist(band_data)

            # Setting the band data
            set_channel(image=input_image,
                        new_channel_data=band_data,
                        chan=band_index,
                        channel_axis=channel_axis)
    return input_image

def _equalize_adaptive_histogram(input_image:np.ndarray,
                                 ndim:int,
                                 channel_axis:int=-1) -> np.ndarray:
    """Performs an adaptive histogram equalization,
    by doing the equalization over regions instead of
    the entire image at once

    Args:
        input_image (np.ndarray): The image array to equalize
        ndim (int): Number of dimensions in the image
        channel_axis (int, optional): Channel axis where
        the color channels are located. Defaults to -1.

    Returns:
        np.ndarray: The image after equalization
    """
    # Checking if it's a single channel image
    if ndim == 2:
        input_image = equalize_adapthist(input_image,
                                         clip_limit=0.004)
    else:
        # Looping through each color channel/band
        for band_index in range(input_image.shape[channel_axis]):
            # Retriving the band data
            band_data = get_channel(input_image=input_image,
                                    channel=band_index,
                                    channel_axis=channel_axis)

            # Equalizaing the band
            band_data = equalize_adapthist(band_data,
                                           clip_limit=0.004)

            # Setting the band data
            set_channel(image=input_image,
                        new_channel_data=band_data,
                        chan=band_index,
                        channel_axis=channel_axis)
    return input_image

def _equalize_clahe_histogram(input_image:np.ndarray,
                              ndim:int,
                              channel_axis:int=-1) -> np.ndarray:
    """Performs an contrast limited
    adaptive histogram equalization,
    by doing the equalization over regions instead of
    the entire image at once

    Args:
        input_image (np.ndarray): The image array to equalize
        ndim (int): Number of dimensions in the image
        channel_axis (int, optional): Channel axis where
        the color channels are located. Defaults to -1.

    Returns:
        np.ndarray: The image after equalization
    """
    # This method requires a integer type image
    input_image = img_as_uint(input_image)

    # Creating the model to apply to the images
    clahe = cv2.createCLAHE(clipLimit = 700)

    # Checking if it's a single channel image
    if ndim == 2:
        input_image = clahe.apply(input_image)
    else:
        # Looping through each color channel/band
        for band_index in range(input_image.shape[channel_axis]):
            # Retriving the band data
            band_data = get_channel(input_image=input_image,
                                    channel=band_index,
                                    channel_axis=channel_axis)

            # Equalizaing the band
            band_data = clahe.apply(band_data)

            # Setting the band data
            set_channel(image=input_image,
                        new_channel_data=band_data,
                        chan=band_index,
                        channel_axis=channel_axis)
    # We return the image as a float because
    # that is the standard for the processing pipeline
    return img_as_float(input_image)
