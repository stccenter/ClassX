"""Module for counting segments"""

# Python Third Party Imports
import numpy as np

__all__ = ["get_image_segment_count", "get_labeled_segment_count"]


def get_image_segment_count(segment_image: np.ndarray):
    """Counts the number of segments in a segment mask"""
    return len(np.unique(segment_image))


def get_labeled_segment_count(segment_info: np.ndarray) -> tuple:
    """Counts the total, labeled, and unlabeled segments
    from the segment information"""
    total_segment_count = len(segment_info)
    labeled_segment_count = np.count_nonzero(segment_info[:, 1])
    unlabeled_segment_count = total_segment_count - labeled_segment_count

    return total_segment_count, labeled_segment_count, unlabeled_segment_count
