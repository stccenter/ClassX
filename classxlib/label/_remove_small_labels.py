"""Submodule for removing small segments from an image"""

# Python Local Library Imports
import traceback

import numpy as np

# Python Third Party Imports
from flask import make_response
from skimage import morphology

# Local imports
from classxlib.train._export import _create_sub_masks, extract_label_mask_from_image

__all__ = ["remove_small_labels"]


def remove_small_labels(
    segment_image: np.ndarray,
    segment_info: np.ndarray,
    unique_label_ids: list[int],
    area_removal_percentage: float,
    unknown_label_id: int,
) -> np.ndarray:
    """Removes small segments from an image based on a percentage of the total image area.

    Args:
        segment_image (np.ndarray): Array of the image to remove small segments from
        segment_info (np.ndarray): Segment information array
        unique_label_ids (list[int]): List of unique label ids
        area_removal_percentage (float): Percentage of the total image area to remove
        unknown_label_id (int): The unknown label id

    Returns:
        np.ndarray: Updated segment information array (removed small segments)s
    """
    try:
        print("SMALL LABEL REMOVAL USED")
        label_mask = extract_label_mask_from_image(
            segment_image, segment_info, unique_label_ids, unknown_label_id, False
        )
        sub_masks = _create_sub_masks(label_mask, unique_label_ids)
        image_area = segment_image.shape[0] * segment_image.shape[1]
        area_removal_threshold = int(image_area * area_removal_percentage)

        for label_id in sub_masks.keys():
            sub_mask = np.zeros(label_mask.shape, dtype=bool)
            if label_id == 0:  # Change to unknown label id
                continue

            sub_mask[label_mask == label_id] = True
            # sub_mask:np.ndarray = sub_masks[label_id]
            # sub_mask = sub_mask.astype(np.uint8)
            new_sub_mask = morphology.remove_small_holes(
                np.copy(sub_mask), area_removal_threshold
            )

            # print(sub_mask[sub_mask != new_sub_mask])
            segment_update = np.unique(
                np.where(sub_mask != new_sub_mask, segment_image, 0)
            ).tolist()
            segment_update.pop(0)

            for segment_number in segment_update:
                segment_info[segment_number - 1][1] = label_id

            # segment_info[:, 1] =
            # np.where(segment_info[:,0] == segment, label_id, segment_info[:,1])
            label_mask = extract_label_mask_from_image(
                segment_image, segment_info, unique_label_ids, unknown_label_id, False
            )
    except (ValueError, IndexError, TypeError, RuntimeError, RuntimeWarning) as error:
        print(error)
        traceback.print_tb(error.__traceback__)
        return make_response(("", 500, {"error": "Couldn't remove small holes."}))
    return segment_info
