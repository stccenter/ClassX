"""Processing Module for creating image crop squares"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np

__all__ = ["create_crop", "crop_grid_square"]


def create_crop(
    visual_image: np.ndarray,
    h5_image: np.ndarray,
    crop_point_x: int,
    crop_point_y: int,
    crop_size: int,
) -> np.ndarray:
    """Crops an image at a point with a variable size

    Args:
        visual_image (np.ndarray): The preprocessed image
        to crop
        h5_image (np.ndarray): The original image
        data if available to crop also.
        crop_point_x (int): X dimension point to crop from
        crop_point_y (int): Y dimension point to crop from
        crop_size (int): The cropping size

    Returns:
        np.ndarray, np.ndarray: Returns the cropped image and the
        cropped image from the original data if available.
    """
    try:
        # Verifying Arguments
        if not isinstance(visual_image, np.ndarray) or not isinstance(
            h5_image, np.ndarray
        ):
            raise TypeError("images need to be numpy array needs to be an ndarray")

        if not isinstance(crop_point_x, int) or not isinstance(crop_point_y, int):
            raise TypeError("crop points need to be int needs to be an int")

        if not isinstance(crop_size, int):
            raise TypeError("zoom needs to be an int")

        # Verifying the click point is not beyond the image boundries
        if (
            crop_point_y >= visual_image.shape[0]
            or crop_point_x >= visual_image.shape[1]
        ):
            return None

        # Verifying the crop size will not go beyond the image boundries
        if crop_point_y + crop_size >= visual_image.shape[0]:
            crop_point_y = visual_image.shape[0] - crop_size
        if crop_point_x + crop_size >= visual_image.shape[1]:
            crop_point_x = visual_image.shape[1] - crop_size

        # Cropping the image
        crop_image = visual_image[
            crop_point_y : crop_point_y + crop_size,
            crop_point_x : crop_point_x + crop_size,
            :,
        ]

        # Checking if the original image data is available
        if h5_image.any():
            # Checking how many channels the data has before cropping to ensure it's correct
            if len(h5_image.shape) == 2:
                h5_crop_image = h5_image[
                    crop_point_y : crop_point_y + crop_size,
                    crop_point_x : crop_point_x + crop_size,
                ]
            elif len(h5_image.shape) > 2:
                h5_crop_image = h5_image[
                    crop_point_y : crop_point_y + crop_size,
                    crop_point_x : crop_point_x + crop_size,
                    :,
                ]
            else:
                return None
        else:
            # Potentially wrong return type with current function annotation?
            h5_crop_image = None

        return crop_image, h5_crop_image
    except (RuntimeError, TypeError, ValueError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None


def crop_grid_square(
    input_image: np.ndarray,
    original_adjusted_image: np.ndarray,
    grid_coord: tuple,
    tile_shape: tuple,
    stride_shape: tuple,
):
    """Function for cropping an image based off a grid square coordinate system

    Args:
        input_image (np.ndarray): Input image to crop
        original_adjusted_image (np.ndarray): If there is original data to crop as well
        grid_coord (tuple): A tuple which contains the coordinates
        tile_shape (tuple): A tuple which holds the grid square shape
        stride_shape (tuple): A tuple that holds the strides of each grid square

    Returns:
        crop_image: The cropped image from the input
        h5_crop_image: The cropped image from the original data
        x_span: The span of the x point coordinate
        y_span: The span of the y point coordinate
        x_index: The x grid index
        y_index: The y grid index
    """
    # Getting the index of the grid square
    x_index = grid_coord[0]
    y_index = grid_coord[1]

    # Changing index into x y dimension
    x = x_index * stride_shape[0]
    y = y_index * stride_shape[1]

    # Cropping the grid square
    crop_image, h5_crop_image = create_crop(
        visual_image=input_image,
        h5_image=original_adjusted_image,
        crop_point_x=x,
        crop_point_y=y,
        crop_size=tile_shape[0],
    )

    # Returning the x and y span
    # This is the crop point + the size of the crop
    x_span = x + tile_shape[0]
    y_span = y + tile_shape[1]

    return crop_image, h5_crop_image, x_span, y_span, x_index, y_index
