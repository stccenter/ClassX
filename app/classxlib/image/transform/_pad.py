"""Pads an input image with the target dimensions"""
# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np

__all__ = ['pad_image']

def pad_image(input_image:np.ndarray,
             target_x_dim:int,
             target_y_dim:int,
             channel_axis:int=-1) -> np.ndarray:
    """Pads an input image with the target dimensions

    Args:
        input_image (np.ndarray): Image ndarray
        target_x_dim (int): target x dimension for padding
        target_y_dim (int): target y dimension for padding
        num_channel (int, optional): number of channels
        in an input image. Defaults to 3.

    Raises:
        TypeError: If the input image is not an ndarray
        TypeError: If the target dimensions are not int
        TypeError: If the channel number is not an int

    Returns:
        np.ndarray: returns the input_image padded as an np.ndarray
    """
    #Verifying the correct arguments
    if not isinstance(input_image, (np.ndarray,np.generic)):
        raise TypeError("input image needs to be an ndarray")
    if not isinstance(target_x_dim, int):
        raise TypeError("target_x_dim needs to be of type int")
    if not isinstance(target_y_dim, int):
        raise TypeError("target_x_dim needs to be of type int")
    if not isinstance(channel_axis, int):
        raise TypeError("num_channel must be of type int")
    try:
        if input_image.ndim == 2:
            num_channel = 1
        else:
            num_channel = input_image.shape[channel_axis]

        # Amount of pixels to add to the x and y dimensions for the input_image
        image_pad_x = target_x_dim - input_image.shape[1]
        image_pad_y = target_y_dim - input_image.shape[0]

        # An array of zeros to pad in both dimensions
        if num_channel > 1:
            y_pad_array = np.zeros((image_pad_y,input_image.shape[1], num_channel),dtype=input_image.dtype)
            x_pad_array = np.zeros((target_y_dim,image_pad_x,num_channel),dtype=input_image.dtype)
        else:
            y_pad_array = np.zeros((image_pad_y,input_image.shape[1]),dtype=input_image.dtype)
            x_pad_array = np.zeros((target_y_dim,image_pad_x),dtype=input_image.dtype)

        # Adding the padding arrays to the image
        padded_image = np.vstack((input_image,y_pad_array))
        padded_image = np.hstack((padded_image, x_pad_array))

        return padded_image
    except (RuntimeError,TypeError,
            ValueError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return np.zeros(input_image.shape)