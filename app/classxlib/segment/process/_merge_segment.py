"""Submodule for merging together segments"""
# Python Standard Library Imports
import traceback

# Python Third Party Imports
import numpy as np
from skimage.graph import (cut_threshold, cut_normalized,
                           merge_hierarchical, rag_mean_color)



def merge_segments(segment_image:np.ndarray,
                   preprocessed_image:np.ndarray,
                   region_merge_method:int,
                   region_merge_threshold:float) -> np.ndarray:
    """Function to merge similar color segments within a given image

    Args:
        segment_image (np.ndarray): The segment image mask
        preprocessed_image (np.ndarray): The image to use as a graph
        parameter_data_dict (dict): Parameter settings

    Returns:
        np.ndarray: _description_
    """
    try:
        # Turning the threshold into a percentage of the image range
        region_merge_threshold = region_merge_threshold/100.0
        image_minimum = np.min(preprocessed_image)
        image_maximum = np.max(preprocessed_image)
        image_range = image_maximum - image_minimum
        region_merge_threshold *= image_range

        # Threshold Cut
        if region_merge_method == 1:
            # Getting the color graph for the image
            segment_region_graph = rag_mean_color(image=preprocessed_image,
                                                  labels=segment_image)
            segment_image = cut_threshold(labels=segment_image,
                                          rag=segment_region_graph,
                                          thresh=region_merge_threshold)
        # Normalized Cut
        elif region_merge_method == 2:
            # Getting the color graph for the image
            segment_region_graph = rag_mean_color(image=preprocessed_image,
                                                  labels=segment_image,
                                                  mode='similarity')
            segment_image = cut_normalized(segment_image, segment_region_graph)
        # Hierarchical Merge
        elif region_merge_method == 3:
            # Getting the color graph for the image
            segment_region_graph = rag_mean_color(image=preprocessed_image,
                                                  labels=segment_image)
            segment_image = merge_hierarchical(segment_image,
                                               segment_region_graph,
                                               thresh=region_merge_threshold,
                                               rag_copy=False,
                                               in_place_merge=True,
                                               merge_func=_merge_mean_color,
                                               weight_func=_weight_mean_color)
        return segment_image
    except (ValueError, IndexError,
            TypeError, RuntimeError,
            RuntimeWarning) as error:
        # We still return the segment image here
        # because occasionally there are errors in merging
        # Caused by irregular shapes
        print("EXCEPTION AT REGION MERGING")
        traceback.print_tb(error.__traceback__)
        return segment_image

#pylint: disable=unused-argument
def _weight_mean_color(graph, src, dst, n):
    """Callback to handle merging nodes by recomputing mean color.

    The method expects that the mean color of `dst` is already computed.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    n : int
        A neighbor of `src` or `dst` or both.

    Returns
    -------
    data : dict
        A dictionary with the `"weight"` attribute set as the absolute
        difference of the mean color between node `dst` and `n`.
    """

    diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
    diff = np.linalg.norm(diff)
    return {'weight': diff}


def _merge_mean_color(graph, src, dst):
    """Callback called before merging two nodes of a mean color distance graph.

    This method computes the mean color of `dst`.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    """
    graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
    graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
    graph.nodes[dst]['mean color'] = (graph.nodes[dst]['total color'] /
                                      graph.nodes[dst]['pixel count'])
