"""ClassX image module that stores all functions related to reading images"""

# Python Standard Library Imports
import os
import traceback
import json

# Python Third Party Imports
import cv2
import numpy as np
import h5py
from osgeo import gdal, osr
from astropy.io import fits
from sunpy.map import Map
from aiapy.calibrate import register, update_pointing

# Local Library Imports
from .transform import rescale_intensity

__all__ = ["read_cv_image", "read_hdf5_image", "read_geotiff_image"]


# Function to read Images using OpenCV
def read_cv_image(
    path: str,
    reverse_channel: bool = True,
    flag: int = cv2.IMREAD_ANYCOLOR,
    noflag: bool = False,
) -> np.ndarray:
    """Read image from file path and return image array
    utilizing OpenCV

    Args:
        path (str): File directory of image. Default uses working directory as base directory.
        reverse_channel (bool, optional): Reverses the color channel when reading an image.
        This is ignored for single channel images. Defaults to True.
        flag (int, optional): OpenCV Imread flags. Defaults to cv2.IMREAD_ANYDEPTH.
        noflag(bool, optional): Disables OpenCV Imread flags. Defaults to False.
    Raises:
        FileNotFoundError: If path is an empty string, file does not exist
        TypeError: If path is not a string
    Returns:
        cv_image: Returns a ndarray
    """
    #try:
    # Validate function arguments
    if path == "" or os.path.exists(path) is False:
        raise FileNotFoundError("path is empty or file does not exist")
    if not isinstance(path, str):
        raise ValueError("path must be a string")
    if not isinstance(reverse_channel, bool):
        raise ValueError("reverse_channel must be bool")

    # Ignores reverse_channel if set to load single channel images
    if flag == cv2.IMREAD_GRAYSCALE:
        reverse_channel = False

    # Reverses the color channels if set to true.
    if reverse_channel is True:
        cv_image = cv2.imread(path) if noflag is True else cv2.imread(path, flag)
        # Ignores reversing the channels if the image is single channel
        cv_image = (
            cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            if len(cv_image.shape) == 3
            else cv_image
        )
    else:
        cv_image = cv2.imread(path) if noflag is True else cv2.imread(path, flag)
    return cv_image
    # This is added because cv2 is not recognized properly
    # pylint: disable=catching-non-exception
    # except (cv2.error, RuntimeError, ValueError, FileNotFoundError) as error:
    #     print("Error:", error)
    #     traceback.print_tb(error.__traceback__)
    #     return None


def read_hdf5_image(
    path: str,
    dataset_name: str = "image_data",
    mode: str = "standard",
    dtype:np.dtype=np.float32) -> np.ndarray:
    """Reads an image array from an HDF5 file

    Args:
        path (str): The path to the HDF5 file
        dataset_name (str, optional): The name of the dataset stored in
                                        the HDF5 file. Defaults to ``"image_data"``.

    Raises:
        FileNotFoundError: If the path is an empty string or if the path does not end with .h5
        ValueError: If the path is not a String
        TypeError: If the dataset name is not of Type String
        KeyError: If the dataset_name does not exist within the file

    Returns:
        np.ndarray: numpy array stored within the HDF5 file
    """
    try:
        # Validate function arguments
        if path == "" or os.path.exists(path) is False:
            raise FileNotFoundError("path is empty or file does not exist")
        if not path.endswith((".h5", ".png")):
            raise NameError("Invalid file type")
        if not isinstance(path, str):
            raise ValueError("path must be of type String")

        # Validate the dataset name
        if not isinstance(dataset_name, str):
            raise KeyError("h5 dataset name must be of type String")

        if path.endswith(".h5"):
            # Reading the HDF5 file
            h5_file = h5py.File(path, "r")

            # Verifying the dataset exists in the HDF5 file
            if dataset_name not in h5_file:
                raise KeyError("Error dataset name:" + dataset_name + " Does not exist")

            # Extracting the image array
            image_array = np.array(h5_file[dataset_name][:], dtype=dtype)

            # Closing the file
            h5_file.close()

            # Training mode needs to be formatted a certain way.
            if mode == "training":
                # Checking if it's a single channel image
                if len(image_array.shape) == 2:
                    image_array = np.dstack((image_array, image_array, image_array))
                # Image needs to be in a unsigned 8 bit integer format
                if np.issubdtype(image_array.dtype, np.floating):
                    image_array = rescale_intensity(
                        image_array, old_range=(0, 1), target_dtype=np.uint8
                    )
                else:
                    image_array = rescale_intensity(image_array, target_dtype=np.uint8)
                image_array = image_array.transpose(2, 0, 1)
            # Returning the image array
            return image_array
        # Backwards compatibility feature for the older image storage format
        if path.endswith(".png"):
            image_array = read_cv_image(path, flag=cv2.IMREAD_UNCHANGED)
            return image_array
        raise KeyError("Unsupported File Type")
    except (
        NameError,
        RuntimeError,
        FileNotFoundError,
        FileExistsError,
        ValueError,
        KeyError,
    ) as error:
        # Returns None if there are errors
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None


def read_geotiff_image(
    path: str,
    reverse_axis: bool = True,
    return_metadata: bool = True,
    return_coordinate: bool = True,
    coordinate_system: str = None,
):
    """Function for reading geotiff images

    Args:
        path (str): Path where the tiff image is located
        reverse_axis (bool, optional): Check to reverse the channel axis
        for the image. Defaults to True.
        return_metadata (bool, optional): Check to return metadata of image.
        Defaults to True.
        return_coordinate (bool, optional): Check to return the image coordinates.
        Defaults to True.
        coordinate_system (str, optional): Coordinate system to convert to if needed.
        This is ignored if return coordinate is false. Defaults to None.

    Raises:
        ValueError: If the filepath has the incorrect type

    Returns:
        tuple: Returns the image and associated info if checked
    """
    #try:
    if not path.endswith(".tif"):
        raise ValueError("File type incorrect")

    # Opening the tif image using Gdal Driver
    gdal_image_obj = gdal.Open(path)

    # Extracting the image array data
    image_data = gdal_image_obj.ReadAsArray()

    # Reversing the image channel axis
    if reverse_axis is True:
        image_data = image_data.transpose(1, 2, 0)

    # Initial return object with the image data
    return_obj = image_data

    # Appending the coordindate data
    if return_coordinate is True:
        # Creating a spatial reference object to extract the coordinates
        spatial_system = osr.SpatialReference()
        spatial_system.ImportFromWkt(gdal_image_obj.GetProjectionRef())
        if coordinate_system is not None:
            new_spatial_system = osr.SpatialReference()
            new_spatial_system.ImportFromWkt(coordinate_system)
        else:
            new_spatial_system = spatial_system
        # create a transform object to convert between coordinate systems
        transform = osr.CoordinateTransformation(spatial_system, new_spatial_system)

        # get the point to transform, pixel (0,0) in this case
        image_width = gdal_image_obj.RasterXSize
        image_height = gdal_image_obj.RasterYSize

        # Transformation for coordinates
        geographic_transform = gdal_image_obj.GetGeoTransform()
        minx = geographic_transform[0] + image_width * geographic_transform[1] / 2
        miny = geographic_transform[3] + image_height * geographic_transform[5] / 2

        # get the coordinates in latitude longitude
        latlong = transform.TransformPoint(minx, miny)[:2]

        return_obj = (return_obj, gdal_image_obj.GetMetadata(), latlong)
    return return_obj
    # except (ValueError, TypeError, RuntimeError, OSError) as error:
    #     print("Error loading image:", error)
    #     traceback.print_tb(error.__traceback__)
    #     return None


# pylint: disable=unused-argument
def read_fits_image(path: str, index: int, dtype: np.dtype = np.int16):
    """Reads a fits file object

    Args:
        path (str): File path for the fits image
        index (int): index to access for the image
        flip_axis (bool, optional): Check to flip the image axis. Defaults to True.
        return_header (bool, optional): Check to return the image header. Defaults to True.
        return_map (bool, optional): Check to return the map for the fits image object.
        Defaults to True.
        dtype (np.dtype, optional): Which datatype to read the image as. Defaults to np.int16.

    Returns:
        image_data: The image array of the fits image
        image_header: The image header of the fits image
        image_map: The image map calculated by sunpy
    """

    # Reading the image object into memory
    fits_image_obj = fits.open(path)
    fits_image_obj.verify("silentfix")
    print(fits_image_obj)
    # Extracting the data and header
    image_data = fits_image_obj[index].data
    image_header = fits_image_obj[index].header
    print(image_header)
    print(image_data)
    print("Original 1 max", np.max(image_data))
    print("Original 1 min", np.min(image_data))
    # Update to Level 1.5 Data Product
    try:
        if image_header["LVL_NUM"] < 1.5:
            sunpy_map = Map((image_data, image_header))  # Create Sunpy Map
            print(sunpy_map)
            sunpy_map = update_pointing(sunpy_map)  # Update Header based on Latest Information
            sunpy_map_registrered = register(sunpy_map)  # Recenter and rotate to Solar North
            image_data = sunpy_map_registrered.data
            # Undo Keword Renaming
            H = dict()
            for k in sunpy_map_registrered.meta.keys():
                H[k.upper()] = sunpy_map_registrered.meta[k]
        # Skip if already Level 1.5
        else:
            # Convert header to dictionary
            sunpy_map = Map((image_data, image_header))  # Create Map
            H = dict()
            for k in sunpy_map.meta.keys():
                image_header[k.upper()] = sunpy_map.meta[k]
            image_data = image_data * 1  # Copy image
    except Exception as e:
        print("Error", e)
         # Convert header to dictionary
        sunpy_map = Map((image_data, image_header))  # Create Map
        H = dict()
        for k in sunpy_map.meta.keys():
            image_header[k.upper()] = sunpy_map.meta[k]
        image_data = image_data * 1  # Copy image

    return image_data, image_header, sunpy_map
