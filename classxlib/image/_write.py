"""ClassX image module that stores all functions related to writing images"""
# Python Standard Library Imports
import traceback

# Python Third Party Imports
import cv2
import numpy as np
import h5py
import matplotlib.pyplot as plt

#Function that writes an Array as an image to disk
def write_cv_image(input_image:np.ndarray,
                   dir_:str,
                   reverse_channel:bool=True,
                   colormap=None) -> bool:
    """Writes a given array as an image to disk

    Args:
        input_image (np.ndarray): Input array to write.
        dir_ (str): File directory to write to.
        reverse_channel (bool, optional): Reverses the channels before writing to disk,
        this is ignored if colormapping is used. Defaults to True.
        colormap (Pyplot Colormap, optional): Colormaps an image before writing.
        Image will always be 8 bit if this is used. Defaults to None.

    Raises:
        ValueError: If filename is not of type String
        TypeError: If input_array is not an ndarray

    Returns:
        bool: Returns true if successful
    """
    #try:
    if not isinstance(dir_, str):
        raise ValueError("filename and/or directory needs to be of type String")
    if not isinstance(input_image, (np.ndarray,np.generic)):
        raise TypeError("input_image needs to be an ndarray")
    if not isinstance(reverse_channel, bool):
        raise ValueError("reverse_channel must be bool")

    if colormap is not None:
        plt.imsave(dir_, input_image, cmap=colormap)
    else:
        #Reverses the color channels if set to true.
        if reverse_channel is True:
            input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(dir_, input_image)
    return True
    # pylint: disable=catching-non-exception
    # except (cv2.error, RuntimeError,
    #         ValueError, TypeError) as error:
    #     print("Error:", error)
    #     traceback.print_tb(error.__traceback__)
    #     return False

def write_hdf5_image(input_image:np.ndarray,
                     dir_:str,
                     dataset_name:str="image_data",
                     datatype:np.dtype=np.float32) -> bool:
    """Writes an image array to disk in an HDF5 file.

    Args:
        input_image (np.ndarray): Input array to write.
        dir_ (str): File directory to write to.
        dataset_name (str, optional): _description_. Defaults to "image_data".
        datatype (np.dtype, optional): _description_. Defaults to np.float32.

    Raises:
        ValueError: If the path is an empty string
        NameError: If the path does not end with .h5
        TypeError: If the path is not of Type String
        TypeError: If the dataset name is not of Type String

    Returns:
        bool: Returns True if write successful, False if an error occurs.
    """
    try:
        # Validate the path argument
        if dir_ == "":
            raise ValueError("path is an empty String")
        if not dir_.endswith(".h5"):
            raise NameError("Invalid file type")
        if not isinstance(dir_, str):
            raise TypeError("path must be of type String")

        # Validate the dataset name
        if not isinstance(dataset_name, str):
            raise TypeError("h5 dataset name must be of type String")

        # Creating the HDF5 file
        h5_file = h5py.File(dir_, 'w')

        # Creating the dataset
        h5_file.create_dataset(name=dataset_name,
                               data=input_image,
                               dtype=datatype)

        # Closing the file
        h5_file.close()

        # Returns True to signify successful write
        return True
    except (RuntimeError, ValueError,
            TypeError) as error:
        # Returns False if there are errors
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return False
