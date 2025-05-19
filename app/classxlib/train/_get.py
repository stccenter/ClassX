"""Module for getting specific data from training files"""

# Python Third Party Imports
import numpy as np

__all__ = ['get_unique_parent_ids_from_link']

def get_unique_parent_ids_from_link(segment_id_link:np.ndarray,
                                    return_crop_id:bool=False,
                                    return_original_id:bool=False):
    """Gets all of the unique image ids from a training file's
    segment id link

    Args:
        segment_id_link (np.ndarray): The segment id link from a training file
        return_crop_id (bool, optional): Option to return the parent
        the crop image ids. Defaults to False.
        return_original_id (bool, optional): Option to return the parent
        original image ids. Defaults to False.

    Returns:
        tuple: returns a tuple of the lists with ids requested in this order;
        tuple(segment_id_list, crop_id_list, original_id_list)
    """
    # Dict object to store results
    return_dict = {}
    # Getting the segment image id list
    return_dict['segment_id_list'] = np.unique(segment_id_link[:,1])

    # Checking to return the crop image id list
    if return_crop_id is True:
        return_dict['crop_id_list'] = np.unique(segment_id_link[:,2])

    # Checking to return the original image id list
    if return_original_id is True:
        return_dict['original_id_list'] = np.unique(segment_id_link[:,3])

    # Converts the dict to values and then converts to a tuple
    return tuple(return_dict.values())
