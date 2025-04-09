"""Image Processing Submodule for reducing or quantizing the number of colors
in an image color pallete"""
# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from sklearn.metrics import pairwise_distances_argmin

# Local Library Imports
from ..transform import rescale_intensity
from ..analysis import get_dtype_range

__all__ = ['quantize_image']

def quantize_image(input_image:np.ndarray,
                   method:int=2,
                   n_colors:int=64) -> np.ndarray:
    """Function to reduce or quantize the number of distinct colors in an image

    Args:
        input_image (np.ndarray): Input image in 3 channel format
        method (int, optional): Method id for which method to use. Defaults to 2.
                1:PIL Adaptive Reduction
                2:Kmeans quantization
                3:Random sample reduction
        n_colors (int, optional): Number of colors to reduce to. Defaults to 64.

    Raises:
        TypeError: If input is not np.ndarray
        TypeError: If method is not a valid id or is not an integer
        TypeError: If n_colors is not an integer

    Returns:
        np.ndarray: Image after quantization is completed
    """
    try:
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("input image needs to be an ndarray")
        if not isinstance(method, int) or method not in (1,2,3):
            raise TypeError("invalid method id")
        if not isinstance(n_colors, int):
            raise TypeError("number of colors needs to be a valid integer")

        # Checking which method to use
        if method == 1:
            input_image = _quantize_image_pil(input_image.copy(), n_colors)
        if method == 2:
            input_image = _quantize_image_kmeans(input_image.copy(), n_colors)
        if method == 3:
            input_image = _quantize_image_random(input_image.copy(), n_colors)


        return input_image
    except (RuntimeError, RuntimeWarning,
            ValueError, TypeError) as error:
        print("WARNING: Image color quantization failed")
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return input_image

### METHOD 1 ###
def _quantize_image_pil(input_image:np.ndarray,
                        n_colors:int) -> np.ndarray:
    """Function for quantizing image using Python Imaging Library"""
    # This method requires an 8 bit image this can result in quality loss
    if input_image.dtype != np.uint8:
        # Checking if the subtype is integer
        if np.issubdtype(input_image.dtype, np.integer):
            # Get the integer data range
            image_range = get_dtype_range(input_image.dtype)
        else:
            # If it's not an integer then it's a float image which is (0-1)
            image_range = (0,1)

        # Rescaling image intensity
        input_image = rescale_intensity(input_image,
                                        old_range=image_range,
                                        new_range=(0,255),
                                        target_dtype=np.uint8)
    # Loading the image into format compatible
    # with the Python Imaging Library(PIL)
    input_image = Image.fromarray(input_image)

    # Lowering the image color palette
    input_image = input_image.convert('P',
                                      palette=Image.ADAPTIVE, # pylint: disable=no-member
                                      colors=n_colors)
    input_image = input_image.convert('RGB')

    # Converting it back to numpy array
    input_image = np.array(input_image)

    # Rescaling the intensity back to a float
    input_image = rescale_intensity(input_image,
                                    old_range=(0,255),
                                    new_range=(0,1),
                                    target_dtype=np.float32)
    return input_image

### METHOD 2 ###
def _quantize_image_kmeans(input_image:np.ndarray,
                           n_colors:int) -> np.ndarray:
    """Function for quantizing image using KMeans Clustering"""
    # Confirming the dtype is a float before processing
    if not np.issubdtype(input_image.dtype, np.floating):
        input_image = rescale_intensity(input_image,
                                        new_range=(0,1),
                                        target_dtype=np.float32)

    # Getting the dimensions of the image
    width, height, depth = input_image.shape

    # Reshaping the data
    input_image = np.reshape(input_image, (width * height, depth))

    # Creating Sample Data
    image_sample = shuffle(input_image, random_state=0, n_samples=1_000)

    # Fitting the model
    model = KMeans(n_clusters=n_colors, random_state=0, n_init=10).fit(image_sample)

    # Generate cluster points from our image
    labels = model.predict(input_image)

    # Recreating image from model and labels
    input_image = _recreate_image(model.cluster_centers_, labels, width, height)

    return input_image

### METHOD 3 ###
def _quantize_image_random(input_image:np.ndarray,
                           n_colors:int) -> np.ndarray:
    """Function for quantizing image using Random Color Sampling"""
    # Confirming the dtype is a float before processing
    if not np.issubdtype(input_image.dtype, np.floating):
        input_image = rescale_intensity(input_image, new_range=(0,1),target_dtype=np.float32)

    # Getting the dimensions of the image
    width, height, depth = input_image.shape

    # Reshaping the data
    input_image = np.reshape(input_image, (width * height, depth))

    # Shuffle the data
    codebook_random = shuffle(input_image, random_state=0, n_samples=n_colors)

    # Get the list of Dominant Colors randomly generated
    labels_random = pairwise_distances_argmin(codebook_random, input_image, axis=0)

    # Recreating the image from the random labels
    input_image = _recreate_image(input_image, labels_random, width, height)

    # Recreating the image from the random labels
    input_image = codebook_random[labels_random].reshape(width, height, -1)

    return input_image

def _recreate_image(codebook,
                    labels,
                    width:int,
                    height:int) -> np.ndarray:
    """Recreate the (compressed) image from the code book & labels"""
    return codebook[labels].reshape(width, height, -1)
