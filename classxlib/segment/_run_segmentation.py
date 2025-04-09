"""Submodule for segmenting an image with preset parameters"""

# Python Standard Library Imports
import traceback
from multiprocessing import Pool
from ctypes import c_uint32
import requests

# Python Third Party Imports
import numpy as np
from skimage.util import img_as_float32

# Local Library Imports
from ..image import read_cv_image, read_hdf5_image
from ..image.transform import equalize_image, stretch_image_contrast, quantize_image
from .algorithm import (
    watershed_transformation,
    slic_transformation,
    quickshift_transformation,
    felzenszwalb_transformation,
    maskrcnn_transformation
)
from .process import mark_segment_boundaries, merge_segments, remove_small_segments

__all__ = ["run_segmentation"]


def run_segmentation(
    image_path: str, h5_image_path: str, parameter_dict: dict
) -> tuple:
    """Function to segment images

    Args:
        image_path (str): File path to the visualzation image
        h5_image_path (str): Path to the original image data
        parameter_dict (dict): Parameter dictionary

    Returns:
        tuple: Tuple of marked image and segment image mask
    """
    # Reading the visualization image
    image = read_cv_image(image_path)

    # Opening the original image data
    # If the original image doesn't exist or it fails
    # reading the image use the visualization image
    # instead
    try:
        if h5_image_path is not None:
            h5_image = read_hdf5_image(h5_image_path)
        else:
            print("No HDF5 Image found")
            h5_image = image.copy()
    except (OSError, FileNotFoundError, RuntimeError):
        print("Failed to read H5 Image")
        h5_image = image.copy()

    # Some images are single channel so we copy the channels to make it
    # into an RGB format
    if len(h5_image.shape) == 2:
        h5_image = np.dstack((h5_image, h5_image, h5_image))
    #print("IMAGE BEFORE")
    #print(h5_image)
    # Checking if the image is already a float type image
    # if not np.issubdtype(h5_image.dtype, np.floating):
    #     h5_image = img_as_float32(h5_image)
    print(h5_image.dtype)
    # Pre-process the image data
    preprocessed_image = _preprocess_image(
        input_image=np.copy(h5_image), parameter_dict=parameter_dict
    )

    # Process the segmentation & post processing for the image
    if parameter_dict["multi_processing_check"] == 1:
        segment_image = _multi_process_segment_image(
            preprocessed_image=preprocessed_image, parameter_dict=parameter_dict
        )
    else:
        segment_image = _process_segment_image(
            preprocessed_image=preprocessed_image, parameter_dict=parameter_dict
        )

    # Marking the boundaries of the segment image
    marked_image = mark_segment_boundaries(
        input_image=image, segment_image=segment_image, light=parameter_dict["light"]
    )

    # None is returned here as a default since the label data is not filled yet.
    return marked_image, segment_image


#### Preprocessing ####
def _preprocess_image(input_image: np.ndarray, parameter_dict: dict) -> np.ndarray:
    """Preprocesses an image before segmentation

    Args:
        input_image (np.ndarray): An image array
        parameter_dict (dict): The parameter settings for
        preprocessing

    Returns:
        np.ndarray: preprocessed image array
    """
    try:
        # Clipping the image to the correct range
        input_image = np.clip(input_image, -1, 1)

        # Check for adjusting image light
        if parameter_dict["light_adjustment_check"] == 1:
            input_image = equalize_image(
                input_image=input_image, method=parameter_dict["histogram_method"]
            )
        # Check for stretching contrast of image
        if parameter_dict["contrast_stretch_check"] == 1:
            input_image = stretch_image_contrast(
                input_image=input_image, percentile_range=(2, 98)
            )

        # Check for reducing or quantizing the amount of
        # colors in an image
        if parameter_dict["color_cluster_check"] == 1:
            input_image = quantize_image(
                input_image=input_image,
                method=parameter_dict["color_cluster_method"],
                n_colors=parameter_dict["color_clusters"],
            )
        return input_image
    except (ValueError, TypeError, RuntimeError, RuntimeWarning) as error:
        print("Failure Preprocessing Image")
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None


#### Processing/Segmentation ####
def _process_segment_image(
    preprocessed_image: np.ndarray, parameter_dict: dict, index: tuple = None
) -> np.ndarray:
    """Processes the segmentation and
    post processing of the segment image

    Args:
        preprocessed_image (np.ndarray): The preprocessed image to segment
        parameter_dict (dict): Parameter data to use
        index (tuple, optional): The mutliprocessing index only used
        if multiprocessing is true. Defaults to None.

    Returns:
        np.ndarray: The segmented image mask
    """

    # Segmenting image based off
    # which segment method id is set
    print("parameter_data['segment_method_id']", parameter_dict["segment_method_id"])
    segment_image = None
    # Watershed algorithm
    if parameter_dict["segment_method_id"] == 1:
        segment_image = watershed_transformation(
            input_image=preprocessed_image,
            gausian_kernal_size=parameter_dict["parameter_1"],
            gradient_cut=parameter_dict["parameter_3"],
        )
    # SLIC algorithm
    elif parameter_dict["segment_method_id"] == 2:
        segment_image = slic_transformation(
            input_image=preprocessed_image,
            n_segments=parameter_dict["parameter_1"],
            compactness=parameter_dict["parameter_2"],
            gausian_kernal_size=parameter_dict["parameter_3"],
        )
    # Quickshift Algorithm
    elif parameter_dict["segment_method_id"] == 3:
        segment_image = quickshift_transformation(
            input_image=preprocessed_image,
            kernel_size=parameter_dict["parameter_1"],
            max_distance=parameter_dict["parameter_2"],
            gausian_kernal_size=parameter_dict["parameter_3"],
        )
    # Felzenswalb Algorithm
    elif parameter_dict["segment_method_id"] == 4:
        segment_image = felzenszwalb_transformation(
            input_image=preprocessed_image,
            scale=parameter_dict["parameter_1"],
            minimum_size=parameter_dict["parameter_2"],
            gausian_kernal_size=parameter_dict["parameter_3"],
        )  # pylint: disable=line-too-long

    # Mask-RCNN Algorithm
    elif parameter_dict["segment_method_id"] == 5:
        segment_image = maskrcnn_transformation(input_image=preprocessed_image,
                                                model_id=parameter_dict["model_id"],
                                                num_classes=parameter_dict["num_classes"])

        #marked_image = np.fromstring(ast.literal_eval(response["marked_image"])
                                        #,dtype=np.uint8).reshape(response['marked_image_shape'])
        #segment_image = np.fromstring(ast.literal_eval(response["segment_image"])
                                        #,dtype=np.uint32).reshape(response['segment_image_shape'])




    # Post processing segments
    postprocessed_segment_image = _postprocess_segment_image(
        segment_image=segment_image,
        preprocessed_image=preprocessed_image,
        parameter_dict=parameter_dict,
    )

    # This is here because of the multiprocessing
    # If its a multiprocessing call we return the index of the
    # grid portion that was being worked on
    if index is None:
        return postprocessed_segment_image
    return postprocessed_segment_image, index


def _multi_process_segment_image(
    preprocessed_image: np.ndarray, parameter_dict: dict
) -> np.ndarray:
    """function for utilizing multiprocessing on an
    segmenting an image array, does this by splitting the image into
    multiple crops and running simultaneous segmentations

    Args:
        preprocessed_image (np.ndarray): preprocessed image array
        parameter_dict (dict): settings for processing

    Returns:
        np.ndarray: The segmented image array
    """
    # Crop size for the multi-processing
    crop_size = 256

    # Creating list to store the asynchronus process references in
    process_list = []

    # The index counts of the image
    # functions like a grid index of which crop to work on
    crop_index_count = (
        preprocessed_image.shape[1] // crop_size,
        preprocessed_image.shape[0] // crop_size,
    )

    # Process pool that handles all the processes running asynchronusly
    with Pool(processes=10) as process_pool:

        # looping through each index region
        for x_index in range(crop_index_count[0]):
            for y_index in range(crop_index_count[1]):
                # x and y pixel spans of where to crop out an image
                x_span = x_index * crop_size
                y_span = y_index * crop_size

                # Creating the asynchronus call
                print("Starting process async", x_index, y_index)
                async_process = process_pool.apply_async(
                    _process_segment_image,
                    args=(
                        preprocessed_image[
                            y_span : y_span + crop_size, x_span : x_span + crop_size
                        ],
                        parameter_dict,
                        (x_index, y_index),
                    ),
                )

                # Appending the reference to the process list
                process_list.append(async_process)

        # The segment image to apply all the asynchronus calls to
        segment_image = np.zeros(
            (preprocessed_image.shape[0], preprocessed_image.shape[1]), dtype=np.uint32
        )
        # Retrieving all the processes after completion
        for process in process_list:
            # Retrieves the result of the process
            # NOTE this will hold until the process is completed
            crop_segment_image, (x_index, y_index) = process.get()
            print("Process ID", x_index, y_index, "Complete")

            # Recreating the x and y spans based off index retrieved
            x_span = x_index * crop_size
            y_span = y_index * crop_size

            # Adding max of the crop image to the result
            # This is because each image is processed separately so
            # there are overlaps in segment ID numbers so we need to make
            # sure overlaps are handled correctly
            crop_segment_image += np.max(segment_image)
            segment_image[y_span : y_span + crop_size, x_span : x_span + crop_size] = (
                crop_segment_image
            )
        # This lets the class know there are no more processes to add
        # after all processes are completed it will close.
        process_pool.close()

    return segment_image


#### Postprocessing ####
def _postprocess_segment_image(
    segment_image: np.ndarray, preprocessed_image: np.ndarray, parameter_dict: dict
) -> np.ndarray:
    """function for post-processing the segments in a segment image

    Args:
        segment_image (np.ndarray): Segment image mask
        preprocessed_image (np.ndarray): The image used for comparision
        parameter_dict (dict): The parameter settings

    Returns:
        np.ndarray: Returns post processed segment image
    """
    # Region Merging Check
    if parameter_dict["region_merge_check"] == 1:
        segment_image = merge_segments(
            segment_image=segment_image,
            preprocessed_image=preprocessed_image,
            region_merge_method=parameter_dict["region_merge_method"],
            region_merge_threshold=parameter_dict["region_merge_threshold"],
        )
    # Small Feature removal check
    if parameter_dict["small_item_removal_check"] == 1:
        segment_image = remove_small_segments(
            segment_image=segment_image,
            preprocessed_image=preprocessed_image,
            size_removal_threshold=parameter_dict["small_item_removal_threshold"],
        )
    # Making sure the Segment ID minimum is 1 not 0
    segment_image = segment_image + 1 if np.min(segment_image) == 0 else segment_image

    # Converting to a 32 bit array before returning
    segment_image = np.ndarray.astype(segment_image, c_uint32)
    return segment_image
