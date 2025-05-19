"""Module for writing segmented images to disk"""
# Python Standard Library Imports
import traceback
from ctypes import c_uint32

# Python Third Party Imports
import numpy as np
import h5py

__all__ = ['write_segment_image','update_segment_image_info']

def write_segment_image(segment_image:np.ndarray,
                       savepath:str,
                       segment_dataset_name:str="segment_data",
                       segment_info_dataset_name:str="segment_info",
                       datatype:np.dtype=c_uint32) -> bool:
    """Writes an segment image mask to disk in an HDF5 file.

    Args:
        segment_image (np.ndarray): Segment image mask array
        savepath (str): Save path to write to
        segment_dataset_name (str, optional): Name of the dataset
        where the segment image will be stored. Defaults to "segment_data".
        segment_info_dataset_name (str, optional): Name of the dataset where
        the segment label information will be stored. Defaults to "segment_info".
        datatype (np.dtype, optional): _description_. Defaults to c_uint32.

    Raises:
        ValueError: If the path is an empty string or
        if the path does not end with .h5
        TypeError: If the path is not of Type String
        TypeError: If the dataset name is not of Type String

    Returns:
        bool: Returns True if write successful, False if an error occurs.
    """
    try:
        # Validate the path argument
        if savepath == "":
            raise ValueError("path is an empty String")
        if not savepath.endswith(".h5"):
            raise ValueError("Invalid file type")
        if not isinstance(savepath, str):
            raise TypeError("path must be of type String")

        # Validate the dataset name
        if not isinstance(segment_dataset_name, str):
            raise TypeError("h5 dataset name must be of type String")
        if not isinstance(segment_info_dataset_name, str):
            raise TypeError("h5 dataset name must be of type String")

        # converting the segment image to the proper datatype
        segment_data = np.array(segment_image, dtype=datatype)

        # Getting the number of segments and their total area counts.
        # Area counts are just the number of pixels each segment takes up.
        segment_numbers, segment_area_count = np.unique(segment_data,
                                                        return_counts=True)

        # Creating an empty array of zeros for the labels
        # since a segment image is initially unlabelled
        segment_labels = np.zeros(segment_numbers.shape)

        # Combining segment numbers, segment labels, and segment areas
        # into a 3 column array of shape (3 x number of segments)
        # This will be stored in the HDF5 file
        segment_info = np.column_stack((segment_numbers,
                                        segment_labels,
                                        segment_area_count))

        # Creating the HDF5 file
        segment_h5_file = h5py.File(savepath, 'w')

        # Creating the segment image dataset
        segment_h5_file.create_dataset(name=segment_dataset_name,
                                       data=segment_data,
                                       dtype=datatype)

        # Creating the segment info dataset
        segment_h5_file.create_dataset(name=segment_info_dataset_name,
                                       data=segment_info,
                                       dtype=datatype)

        # Closing the file to complete the writing
        segment_h5_file.close()

        # Returns True to signify successful write
        return True
    except (OSError, RuntimeError,
            ValueError, TypeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return False

def update_segment_image_info(segment_info:np.ndarray,
                              path:str,
                              segment_info_dataset_name:str="segment_info") -> bool:
    """Updates the segment info section in a segment image file

    Args:
        path (str): Path to write to
        segment_info_dataset_name (str, optional): Name of the dataset where
        the segment label information will be stored. Defaults to "segment_info".

    Raises:
        ValueError: If the path is an empty string or if the path does not end with .h5
        TypeError: If the path is not of Type String
        TypeError: If the dataset name is not of Type String

    Returns:
        bool: Returns True if write successful, False if an error occurs.
    """
    try:
        # Validate the path argument
        if path == "":
            raise ValueError("path is an empty String")
        if not path.endswith(".h5"):
            raise ValueError("Invalid file type")
        if not isinstance(path, str):
            raise TypeError("path must be of type String")

        # Validate the dataset name
        if not isinstance(segment_info_dataset_name, str):
            raise TypeError("h5 dataset name must be of type String")

        # HDF5 File to write
        segment_h5_file = h5py.File(path, 'r+')

        # Deleting old/updating data
        segment_h5_file[segment_info_dataset_name][:] = segment_info

        # Closing the file to complete the writing
        segment_h5_file.close()

        # Returns True to signify successful write
        return True
    except (OSError, RuntimeError,
            ValueError, TypeError,
            FileNotFoundError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return False
