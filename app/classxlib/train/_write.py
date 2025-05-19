# Python Standard Library Imports
from multiprocessing import Pool
import os
from functools import partial

# Python Third Party Imports
import numpy as np
import h5py

# Local Library Imports
from ..database.model import (SegmentImage, CropImage,
                              OriginalImage)
from ..segment import read_segment_image
from ..file import merge_directory
from ..image import read_hdf5_image, read_cv_image


from .analysis import attr_calc

__all__ = ['write_training_file']

def write_training_file(save_path:str,
                        base_directory:str,
                        segment_image_obj:SegmentImage,
                        crop_image_obj:CropImage,
                        original_image_obj:OriginalImage,
                        overwrite:bool):

    label_vector, feature_matrix, segment_id_link = \
                _prepare_dataset(base_directory=base_directory,
                                 segment_image_obj=segment_image_obj,
                                 crop_image_obj=crop_image_obj,
                                 original_image_obj=original_image_obj)
    if overwrite is True:
        # Creating the training file
        _write_new_training_dataset(save_path=save_path,
                                    label_vector=label_vector,
                                    feature_matrix=feature_matrix,
                                    segment_id_link=segment_id_link)
    else:
        _write_append_training_dataset(save_path=save_path,
                                       segment_image_id=segment_image_obj.id,
                                       new_label_vector=label_vector,
                                       new_feature_matrix=feature_matrix,
                                       new_segment_id_link=segment_id_link)

def _calc_attributes(original_image, secondary_image, segment_id):
    feature_array = []
    # pylint: disable=c-extension-no-member
    feature_array = attr_calc.analyze_srgb_image(original_image,
                                                secondary_image,
                                                segment_id=segment_id)
    feature_array = feature_array[0]
    return feature_array

def _prepare_dataset(base_directory:str,
                     segment_image_obj:SegmentImage,
                     crop_image_obj:CropImage,
                     original_image_obj:OriginalImage):
    # Formatting path to segment image
    segment_image_path = merge_directory(base_directory,
                                         segment_image_obj.segment_path)

    # Reading segment image into memory
    segment_image, segment_info = read_segment_image(segment_image_path)

    # Formatting path to HDF5 crop image
    if crop_image_obj.h5_path is not None:
        crop_image_path = merge_directory(base_directory,crop_image_obj.h5_path)
        # Reading original crop image into memory
        crop_image = read_hdf5_image(crop_image_path, mode="training")
    else:
        crop_image_path = merge_directory(base_directory,crop_image_obj.visualization_path)
        crop_image = read_cv_image(crop_image_path)

    segment_count = len(segment_info)
    # Creating a array to store the link between segments using database
    # IDs
    segment_id_link = np.zeros((segment_count, 4), dtype=np.uint32)
    # Segment numbers
    segment_id_link[:,0] = segment_info[:,0]
    # Segment Image ID the segments belong to
    segment_id_link[:,1] = segment_image_obj.id
    # Crop image ID the segment image belongs to
    segment_id_link[:,2] = crop_image_obj.id,
    # Original Image ID the segment belongs to
    segment_id_link[:,3] = original_image_obj.id

    # Label Vector that stores the label ids
    label_vector = segment_info[:,1]

    feature_matrix = _get_feature_matrix(crop_image=crop_image,
                                         segment_image=segment_image,
                                         segment_info=segment_info,
                                         segment_count=segment_count)

    return label_vector, feature_matrix, segment_id_link

def _get_feature_matrix(crop_image, segment_image, segment_info, segment_count):
    # This holds the feature analysis matrix for all the segments
    # We check for 1000+ segments because the initialization of multiprocessing
    # can take longer than it takes to loop normally.
    if segment_count > 1000:
        with Pool(int(os.cpu_count()/2)) as pool:
            func = partial(_calc_attributes,
                           crop_image,
                           segment_image)
            # pylint: disable=no-member
            feature_matrix = pool.map(func, segment_info[:,0].tolist())
    else:
        feature_matrix = []
        # Creating the dataset
        for segment in segment_info[:,0].tolist():
            feature_matrix.append(_calc_attributes(crop_image,
                                                   segment_image,
                                                   segment_id = segment))
    feature_matrix = np.array(feature_matrix)
    return feature_matrix

def _write_new_training_dataset(save_path:str,
                                label_vector:np.ndarray,
                                feature_matrix:np.ndarray,
                                segment_id_link:np.ndarray):
    # Creating the training file
    # All the lists are converted to numpy arrays because HDF5 files are encoded in binary
    with h5py.File(save_path, 'w') as training_file:
        training_file.create_dataset('feature_matrix',
                                     data=feature_matrix,
                                     chunks=True,
                                     maxshape=(None,None))
        training_file.create_dataset('srgb',
                                     data=label_vector,
                                     chunks=True,
                                     maxshape=(None,))
        training_file.create_dataset('segment_id_link',
                                     data=segment_id_link,
                                     chunks=True,
                                     maxshape=(None,None))
        # Closing the file after finished
        training_file.close()

def _write_append_training_dataset(save_path:str,
                                   segment_image_id:int,
                                   new_label_vector:np.ndarray,
                                   new_feature_matrix:np.ndarray,
                                   new_segment_id_link:np.ndarray):
    with h5py.File(save_path, 'a') as training_file:
        new_srgb = new_label_vector
        # Setting segment image id to a variable to avoid excess memory usage during enumerate call
        # enumerate will duplicate class objects during each call causing large memory calls
        segment_id_link = training_file['segment_id_link'][:]

        # List of segment ids in training file
        if np.any(segment_id_link[:,1] == segment_image_id):
            print("Training image already exists in the current file replacing with new data.")
            mask = np.zeros(segment_id_link[:,1].shape, dtype=bool)
            mask[segment_id_link[:,1] == segment_image_id] = True
            for variable_name in ['feature_matrix', 'srgb',
                                  'segment_id_link']:
                if variable_name in training_file:
                    original_dataset = training_file[variable_name][mask != True]
                    temp_name = 'new_' + variable_name
                    new_dataset = locals()[temp_name]
                    combined_dataset = np.concatenate((original_dataset, new_dataset))
                    del training_file[variable_name]
                    training_file.create_dataset(variable_name,
                                                 data=combined_dataset,
                                                 chunks=True)
        else:
            for variable_name in ['feature_matrix', 'srgb',
                                  'segment_id_link']:
                if variable_name in training_file:
                    original_dataset = training_file[variable_name][:]
                    temp_name = 'new_' + variable_name
                    new_dataset = locals()[temp_name]
                    combined_dataset = np.concatenate((original_dataset, new_dataset))
                    del training_file[variable_name]
                    training_file.create_dataset(variable_name,
                                                 data=combined_dataset,
                                                 chunks=True)