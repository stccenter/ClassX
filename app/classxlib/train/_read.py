# Python Third Party Imports
import h5py
import numpy as np

__all__ = ['read_training_file']

#### Load Training Dataset (TDS) (Label Vector and Feature Matrix)
def read_training_file(path:str, image_type:str, unknown_label_id:int=None, return_id_link:bool=False):
    """
    INPUT:
        input_directory of .h5 training data
        file_name of .h5 training data
        list_name of label vector contained within file_name
    RETURNS:
        tds = [label_vector, training_feature_matrix]
    """

    ## Load the training data
    with h5py.File(path, 'r') as training_file:
        # Try loading the dataset with the provided name. If that doesnt work,
        #   try loading with the default name
        if image_type in training_file.keys():
            label_vector = training_file[image_type][:]
            if unknown_label_id is not None:
                mask = np.zeros(label_vector.shape, dtype=bool)
                mask[label_vector == unknown_label_id] = True
                label_vector = label_vector[mask != True]
                print("vector",label_vector.shape)
                print("mask",mask.shape)
                feature_matrix = training_file['feature_matrix'][:]
                print("feature matrix", feature_matrix.shape)
                feature_matrix = training_file['feature_matrix'][mask != True]
            else:
                feature_matrix = training_file['feature_matrix'][:]
                if return_id_link is True:
                    segment_id_link = training_file['segment_id_link'][:]

    # Combine the label vector and training feature matrix into one variable.
    if return_id_link is True:
        training_dataset = [label_vector,feature_matrix, segment_id_link]
    else:
        training_dataset = [label_vector,feature_matrix]

    return training_dataset