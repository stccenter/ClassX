"""Module for cropping and rotating images."""
# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np
import cv2
from imutils.perspective import four_point_transform
from imutils import grab_contours

__all__ = ['crop_rotate_image']

def crop_rotate_image(input_image:np.ndarray) -> np.ndarray:
    """Takes an input image with a black outer background
    crops it and rotates the image to be level.

    Args:
        input_image (np.ndarray): An np.ndarray to be processed

    Raises:
        TypeError: If input image is not np.ndarray

    Returns:
        np.ndarray: Processed image in ndarray format
    """

    try:
        # Verifying arguments
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("input image needs to be an ndarray")

        # Converting image to grayscale to find countour points
        grayscale_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)

        # Finding contours
        contours= cv2.findContours(grayscale_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Extracting contour lines
        contours = grab_contours(contours)
        contours = max(contours, key = cv2.contourArea)
        screen_contours = None

        # Marking the contour points to rotate the image from
        for epsilon in np.linspace(0.001, 0.05, 10):
            # Perimeter of contour
            perimeter = cv2.arcLength(contours, True)

            # Creating a approximate polygon based off the countours
            approx_polygon = cv2.approxPolyDP(contours, epsilon * perimeter, True)

            # When approx is 4 that means we have 4 corner points
            if len(approx_polygon) == 4:
                screen_contours = approx_polygon
                break
        # Shaping the 4 corner points of image
        points = screen_contours.reshape(4, 2)

        # Rotating image based on points to be flat/level
        image_rotated = four_point_transform(input_image, points)

        # Checking if the image was rotated to be vertically
        # taller if so rotate to make it horizontally longer
        x_dim,y_dim = image_rotated.shape[1],image_rotated.shape[0]
        if x_dim < y_dim:
            image_rotated = cv2.rotate(image_rotated, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return image_rotated
    # pylint: disable=catching-non-exception
    except (TypeError, ValueError,
            cv2.error, RuntimeError)as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return np.zeros(input_image.shape)
