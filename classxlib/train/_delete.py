"""This module contains functions to delete images from training files"""

# Python Third Party Imports
import numpy as np
import h5py

__all__ = ["delete_image_from_file"]


def delete_image_from_file(file_path: str, segment_image_id: int):
    """Deletes a segment image from a traning file

    Args:
        file_path (str): filepath of the image
        segment_image_id (int): the segment image id to remove
    """

    with h5py.File(file_path, "a") as training_file:
        # Setting segment image id to a variable to avoid excess memory usage during enumerate call
        # enumerate will duplicate class objects during each call causing large memory calls
        segment_id_link = training_file["segment_id_link"][:]

        # List of segment ids in training file
        if np.any(segment_id_link[:, 1] == segment_image_id):
            mask = np.zeros(segment_id_link[:, 1].shape, dtype=bool)
            mask[segment_id_link[:, 1] == segment_image_id] = True
            for variable_name in ["feature_matrix", "srgb", "segment_id_link"]:
                if variable_name in training_file:
                    new_dataset = training_file[variable_name][mask != True]
                    del training_file[variable_name]
                    training_file.create_dataset(
                        variable_name, data=new_dataset, chunks=True
                    )
