"""Module for coloring labeled images and segments"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np

# Local Library Imports
from ._convert_hex import hex2rgb

def color_labeled_image(input_image:np.ndarray,
                         segment_image:np.ndarray,
                         segment_info:np.ndarray,
                         research_label_map:dict,
                         alpha:float=0.7)->np.ndarray:
    """Takes in an image and a segment image array and
    colors the segments based off the stored labels
    within segment info and research field label map

    Args:
        input_image (np.ndarray): Input image array to be colored
        segment_image (np.ndarray): The segment mask should be single channel
        segment_info (np.ndarray): Segment label information stored
        in an array with each row as (segment_number, segment_label_id, segment_area)
        research_label_map (dict): Label map for the research field retrieved from database
        alpha (float): Percentage value of blending/opacity
        value of labels in range 0-1.0(aka 0%-100%). Defaults to 0.7

    Raises:
        TypeError: If input marked image is not an array
        TypeError: If segment mask is not an array
        Exception: If the input marked image and segment image do not match shapes

    Returns:
        np.ndarray: returns a 3 channel colored image
    """
    try:
        # Validating the input images
        if not isinstance(input_image, (np.ndarray,np.generic)):
            raise TypeError("marked_image needs to be an ndarray")
        if not isinstance(segment_image, (np.ndarray,np.generic)):
            raise TypeError("segmented_image needs to be an ndarray")
        if input_image.shape[:2] != segment_image.shape:
            raise ValueError("marked image and segmented image need to be same shape")


        # Checking if there are any labeled segments before major logic begins
        if len(segment_info) == 0:
            return input_image

        # blank image to be colored
        color_image = np.zeros(input_image.shape)

        # Coloring all labeled areas does a loop for each label type
        for label in research_label_map:
            # Label ID to color image with
            label_id = label["id"]

            # Converting the Hexdecimal code to RGB tuple (R,G,B)
            color = hex2rgb(label["color"])

            # Boolean mask where to the segment number and label id match
            # Utilizing segment label data from the segment_info it
            # finds all pixels where the segment numbers/current label match
            mask = np.isin(segment_image, np.where(segment_info[:,1] == label_id,
                                                   segment_info[:,0],
                                                   0))

            # Stacking the mask to follow the shape of the colored image
            # When using np.where to edit the arrays they need to be of the same shape
            mask = np.dstack((mask,mask,mask))

            # Updating the color image
            # Wherever the mask is equal to True it puts the color pixel values
            color_image = np.where(mask, color, color_image)

        # Everywhere it's still 0 means there was no label
        # to color there so we set it to be the marked image.
        # Merging the color image and marked image together
        # this blends the label ontop of the color image
        color_image = np.where(color_image==[0,0,0],
                               input_image,
                               input_image * (1.0 - alpha) + color_image * alpha)

        # Converting the datatype to uint8 to ensure data
        # consistency since the segment images are uint32
        color_image = color_image.astype(np.uint8)
        return color_image
    except (RuntimeError, TypeError,
            ValueError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return input_image
