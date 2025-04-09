"""Submodule for removing small segments from an image"""

# Python Local Library Imports
import traceback

# Python Third Party Imports
import numpy as np
from skimage.graph import rag_mean_color
from skimage.segmentation import relabel_sequential

__all__ = ['remove_small_segments']

def remove_small_segments(segment_image:np.ndarray,
                          preprocessed_image:np.ndarray,
                          size_removal_threshold:int) -> np.ndarray:
    """Function to detect all segments within a certain pixel count
    threshold, then removes/merges them with their closest color neighbour

    Args:
        segment_image (np.ndarray): Segment image mask
        preprocessed_image (np.ndarray): The image used for comparision
        size_removal_threshold (int): The minimum count for a segment,
        this number gets times by 5

    Returns:
        np.ndarray: Segment image after all small objects are removed
    """
    try:
        print("SMALL FEATURE REMOVAL USED")
        size_removal_threshold = size_removal_threshold*5
        removal_list = _get_remove_list(segment_image,size_removal_threshold)
        # create region adjacency graph
        mean_color_rag = rag_mean_color(preprocessed_image, segment_image)
        for node, data in mean_color_rag.nodes(data=True):
            data['labels'] = node

        # merge selected segments
        for segment in removal_list:
            # check if the segment is still below the threshold
            if np.count_nonzero(segment_image == segment) > size_removal_threshold:
                continue
            # store adjacent segments
            adj_segments = mean_color_rag.adj[segment]  # {segment_num: {'weight': value}, ... }
            # find the segmenent with minimum color difference
            min_segment = next(iter(adj_segments.keys()))

            for adj in adj_segments:
                weight = adj_segments[adj]['weight']
                if weight < adj_segments[min_segment]['weight']:
                    min_segment = adj

            # merge segment with minimum segment
            segment_image[segment_image == segment] = min_segment
            # update RAG
            mean_color_rag.merge_nodes(segment, min_segment)

        # re-sequentialize segment labels
        segment_image = relabel_sequential(segment_image)[0]

    except (ValueError, IndexError,
            TypeError, RuntimeError,
            RuntimeWarning) as error:
        print("EXCEPTION AT SMALL FEATURE REMOVAL")
        traceback.print_tb(error.__traceback__)
        return segment_image
    return segment_image

def _get_remove_list(segment_image:np.ndarray, removal_threshold:int) -> list:
    """Helper function to find all segments
    that fall under the threshold

    Args:
        segment_image (np.ndarray): Segment image array
        removal_threshold (int): The size threshold for removal

    Returns:
        list: List of segment IDs to remove
    """

    # find segments that meet pixel threshold
    segment_list, segment_lengths = np.unique(segment_image, return_counts=True)
    removal_list = []

    for i in range(segment_list.size):
        if segment_lengths[i] <= removal_threshold:
            removal_list.append(segment_list[i])
    print(f"{len(removal_list)} segments to be removed")
    return removal_list
