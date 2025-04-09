"""Module for creating the auto crop grid for an image"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np
import cv2

# Local Library Imports
from classxlib.color import hex2rgb
from ..transform import pad_image

__all__ = ["process_image_grid"]


def process_image_grid(
    input_image: np.ndarray,
    crop_size: int = 256,
    grid_line_color: str = "#b1ddfc",
    line_thickness: int = 16,
    draw_lines: bool = True,
) -> np.ndarray:
    """Function to draw a cropping grid on a training image

    Args:
        input_image (np.ndarray): Input image to draw over
        crop_size (int, optional): Crop size of grid plots. Defaults to 256.
        grid_line_color (str, optional): Color of the grid lines. Defaults to '#b1ddfc'.
        line_thickness (int, optional): Pixel thickness of grid lines. Defaults to 16.

    Raises:
        TypeError: If input image is not an np.ndarray

    Returns:
        np.ndarray: returns image with lines drawn
    """
    try:
        if not isinstance(input_image, (np.ndarray, np.generic)):
            raise TypeError("input image needs to be an ndarray")

        # Edits the target image dimensions if the crop size
        # would make the image be padded by over 20% of a crop grid
        # This is to avoid having mostly black grid squares from the image padding
        image_target_width, image_target_height = (
            input_image.shape[1],
            input_image.shape[0],
        )
        if (image_target_width % crop_size) < int(crop_size * 0.8):
            image_target_width -= image_target_width % crop_size
        if (image_target_height % crop_size) < int(crop_size * 0.8):
            image_target_height -= image_target_height % crop_size

        # Reducing the image size if necessary
        input_image = input_image[0:image_target_height, 0:image_target_width]

        # Grid Image after processing
        grid_image = _create_grid_image(
            input_image=input_image,
            crop_size=crop_size,
            grid_line_color=hex2rgb(grid_line_color),
            line_thickness=line_thickness,
            draw_lines=draw_lines,
        )
        return grid_image
    except (RuntimeError, TypeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return np.zeros(input_image.shape)


def _create_grid_image(
    input_image: np.ndarray,
    crop_size: int = 256,
    grid_line_color: tuple = (177, 221, 252),
    line_thickness: int = 16,
    draw_lines: bool = True,
) -> np.ndarray:
    """Takes a given image to draw square grid lines.
    If grid shape is incompatible image will be padded to compensate.

    Args:
        image (np.ndarray): An input image of type np.ndarray
        crop_size(int) : Size of the grid squares to create
        grid_line_color (tuple, optional): The color of the grid lines in a RGB format.
        Defaults to (177,221,252).
        line_thickness (int, optional): Pixel thickness of the lines drawn. Defaults to 16.

    Raises:
        TypeError: If the input image is not an np.ndarray

    Returns:
        np.ndarray: Returns the image with the lines drawn and appropriate padding
    """

    if not isinstance(input_image, (np.ndarray, np.generic)):
        raise TypeError("input image needs to be an ndarray")

    try:

        # Amount of grid squares on the x and y dimensions
        grid_x_count = (input_image.shape[1] - 1) // crop_size + 1
        grid_y_count = (input_image.shape[0] - 1) // crop_size + 1

        # Target dimension to pad image so the grid lines fit
        target_x_dim = grid_x_count * crop_size
        target_y_dim = grid_y_count * crop_size

        # Padding the image
        padded_image = pad_image(
            input_image=input_image,
            target_x_dim=target_x_dim,
            target_y_dim=target_y_dim,
        )

        delta_y, delta_x = target_y_dim / grid_y_count, target_x_dim / grid_x_count

        if draw_lines is True:
            # draw vertical lines
            for x in np.linspace(
                start=delta_x, stop=target_x_dim - delta_x, num=grid_x_count - 1
            ):
                cv2.line(
                    img=padded_image,
                    pt1=(int(round(x)), 0),
                    pt2=(int(round(x)), target_y_dim),
                    color=grid_line_color,
                    thickness=line_thickness,
                )

            # draw horizontal lines
            for y in np.linspace(
                start=delta_y, stop=target_y_dim - delta_y, num=grid_y_count - 1
            ):
                cv2.line(
                    img=padded_image,
                    pt1=(0, int(round(y))),
                    pt2=(target_x_dim, int(round(y))),
                    color=grid_line_color,
                    thickness=line_thickness,
                )

        return padded_image
    except (TypeError, ValueError, RuntimeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return np.zeros(input_image.shape)


"""
def process_grid_crop_square(
    input_image: np.ndarray,
    original_adjusted_image: np.ndarray,
    grid_coord,
    tile_shape,
    stride_shape,
):

    x_index = grid_coord[0]
    y_index = grid_coord[1]
    x = x_index * stride_shape[0]
    y = y_index * stride_shape[1]
    crop_image, original_crop_image = createCrop(
        preprocessed_image, original_adjusted_image, x, y, tile_shape[0]
    )

    x_span = x + tile_shape[0]
    y_span = y + tile_shape[1]

    return crop_image, original_crop_image, x_span, y_span, x_index, y_index
"""
