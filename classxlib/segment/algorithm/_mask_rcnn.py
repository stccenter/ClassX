"""Module for segmenting images using the
mask-rcnn algorithm"""

# Python Standard Library Imports
import traceback
import requests
import ast

# Python Third Party Imports
import numpy as np

__all__ = ['maskrcnn_transformation']

def maskrcnn_transformation(input_image:np.ndarray, model_id:int=1, num_classes:int=1)->np.ndarray:
    """Performs a segmentation on an image array using the quickshift algorithm

    Args:
        input_image (np.ndarray): The image array from which the segmentation
        will be performed

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
        image_shape = input_image.shape
        # Image is converted to a string to be json serialible
        json_data = {"image_shape":image_shape,
                     "image":str(input_image.tobytes()),
                     "model_id":model_id,
                     "num_classes":num_classes}

        # Sending the request to the container to process the image
        response_data = requests.get("http://mask-rcnn-cpu:5002/process_image/",
                                        json=json_data).json()
        # Casting the image string back into bytes
        response_image_string = ast.literal_eval(response_data["segment_image"])

        # Converting the byte string into a numpy array
        # Image is flattened so it has to be reshaped
        response_image = np.frombuffer(response_image_string,
                                       dtype=np.float32).reshape((image_shape[0],image_shape[1]))
        # Label Map
        return response_image
    except (ValueError, IndexError,
            TypeError, RuntimeError,
            RuntimeWarning) as error:
        print("Quickshift transformation failed")
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None