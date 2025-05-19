"""Utility Module for manipulating image color channels"""

# Python Third Party Imports
import numpy as np

__all__ = ['get_channel','set_channel']

def get_channel(input_image:np.ndarray,
                channel:int,
                channel_axis:int=-1):
    """
    Extracts a specific channel from an image array.

    Parameters:
    image : numpy.ndarray
        The image array from which to extract the channel.
    chan : int
        The index of the channel to extract.
    channel_axis : int
        The index of the axis corresponding to the channels.

    Returns:
    numpy.ndarray
        A 2D array representing the specified channel.
    """
    return np.take(input_image, indices=channel, axis=channel_axis)

def set_channel(image, new_channel_data, chan, channel_axis):
    """
    Sets a specific channel of an image array to new data.

    Parameters:
    image : numpy.ndarray
        The image array where the channel data will be updated.
    new_channel_data : numpy.ndarray
        The new data to be set in the specified channel. This array should match the size
        of the other dimensions of the image array, excluding the channel dimension.
    chan : int
        The index of the channel to set.
    channel_axis : int
        The index of the axis corresponding to the channels.

    Raises:
        ValueError: If the new_channel_data dimensions do not match the required dimensions.
    """
    # Ensure the new channel data has the correct shape by checking against the image dimensions
    # with the channel dimension omitted.
    target_shape = list(image.shape)
    del target_shape[channel_axis]
    if list(new_channel_data.shape) != target_shape:
        raise ValueError("The new channel data does not match the required dimensions.")

    # Use np.take to isolate the channel and then use np.put along the same axis to update it.
    indices = [slice(None)] * image.ndim
    indices[channel_axis] = chan
    image[tuple(indices)] = new_channel_data
