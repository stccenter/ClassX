"""Module for Exporting Training Files"""

# Python Standard Library Imports
import shutil
import traceback

import numpy as np

# Python Third Party Imports
from pycocotools import mask as maskUtils

# Local imports
from classxlib.image import read_hdf5_image, write_cv_image, write_hdf5_image
from classxlib.image.transform import rescale_intensity

__all__ = ['extract_label_mask_from_image',
           'export_image_file_type',
           'export_mask_file_type',
           'export_as_coco',
           'coco_init']

def extract_label_mask_from_image(segment_image:np.ndarray,
                            segment_info:np.ndarray,
                            label_id_list:list[int],
                            unknown_label_id:int,
                            export:bool = True)->np.ndarray:
    """ Gets the label mask of the specified segmented image.

    Args:
        segment_image (np.ndarray): The segment mask should be single channel.
        segment_info (np.ndarray): Segment label information stored (uses training data h5 file).
        label_id_list (list[int]): List of unique label ids in the image.
        unknown_label_id (int): The id of the "unknown" label.

    Raises:
        TypeError: If any of the specified parameters are the wrong type.

    Returns:
        np.ndarray: Single channel label mask.
    """
    try:        
        # Empty mask of the segment
        label_mask = np.zeros(segment_image.shape)

        # Creates a mask for every label id
        for label_id in label_id_list:            
            # skips masking if the label is 'unknown'
            if label_id == unknown_label_id:
                continue
            
            # Boolean mask where to the segment number and label id match
            # Utilizing segment label data from the segment_info it
            # finds all pixels where the segment numbers/current label match
            if export:
                mask = np.isin(
                    segment_image,
                    np.where(segment_info[:, 0] == label_id, 
                            segment_info[:, 1], 
                            0),
                )
            else:
                mask = np.isin(
                    segment_image,
                    np.where(segment_info[:, 1] == label_id, 
                            segment_info[:, 0], 
                            0),
                )
            
            # Wherever the mask is equal to True it puts the label id of the pixel
            label_mask = np.where(mask, label_id, label_mask)
            
        return label_mask
    except TypeError as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return segment_image

def export_image_file_type(crop_image_path:str,
                           export_image_dir:str,
                           new_file_type:str) -> None:
    """ Takes the h5 file of the training data and converts to the desired file type.
    Supports ("h5", "png_16", "png_8", and "jpg") file types.

    Args:
        crop_image_path (str): Path of the image's h5 file.
        export_image_dir (str): Path of where the file will be written (export image directory).
        new_file_type (str): Desired filetype.
        
    Raises:
        TypeError: Exporting in unsupported file type.
    """
    try:
        match new_file_type:
            case "h5":
                shutil.copyfile(crop_image_path, export_image_dir)
            case _:
                crop_image = read_hdf5_image(crop_image_path)
                if new_file_type == "png_16":
                    crop_image = rescale_intensity(input_image=crop_image,
                                                    old_range=(0.0,1.0),
                                                    target_dtype=np.uint16)
                else:
                    crop_image = rescale_intensity(input_image=crop_image,
                                                    old_range=(0.0,1.0),
                                                    target_dtype=np.uint8)
                write_cv_image(crop_image, export_image_dir)
    except TypeError as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        
def export_mask_file_type(label_mask:np.ndarray,
                          export_mask_dir:str,
                          new_file_type:str) -> None:
    """ Writes the given mask array in the desired filetype. 
    Supports ("h5", "png_16", "png_8", "txt", "npy", and "jpg") file types. 

    Args:
        label_mask (np.ndarray): Mask array to write.
        export_mask_dir (str): Path of where the file will be written (export mask directory).
        new_file_type (str): Desired filetype.
        
    Default:
        The default mask image type is 16 bit PNG.
    
    Raises:
        TypeError: Exporting in unsupported file type.
    """
    try:
        match new_file_type:
            case "h5":
                write_hdf5_image(label_mask, export_mask_dir)
            case "txt":
                np.savetxt(export_mask_dir, label_mask)
            case "npy":
                np.save(export_mask_dir, label_mask)
            case _:
                # Stacks masks for 3 channel images (JPG and PNG)
                label_mask = np.dstack((label_mask, label_mask, label_mask))
                if new_file_type != "png_8" and new_file_type != "jpg":
                    label_mask = label_mask.astype(np.uint16)
                else:
                    label_mask = label_mask.astype(np.uint8)
                write_cv_image(label_mask, export_mask_dir, reverse_channel=False)
    except TypeError as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        
def export_as_coco(id:int,
                   label_mask: np.ndarray,
                   master_dict:dict,
                   unique_label_id_list:list[int],
                   segment_image_id:int) -> None:
    """Exports segment images in COCO format (JSON).

    Args:
        id (int): Id of the sub masks.
        label_mask (np.ndarray): Label mask to be converted into COCO.
        master_dict (dict): Stores information about the sub masks in RLE format (under ["annotations"]["counts"])
        unique_label_id_list (list[int]): Unique label ids of the segment image.
        segment_image_id (int): Segment image id.
    """
    _ = _create_sub_masks(label_mask, 
                          unique_label_id_list, 
                          create_coco=True,
                          crop_image_id=id, 
                          master_dict=master_dict, 
                          segment_image_id=segment_image_id)
        
def coco_init(label_ids:list[int],
              research_field:str,
              research_field_label_map:dict,
              unknown_label_id:int) -> dict:
    """Initializes COCO file.

    Args:
        label_ids (list[int]): List of all label ids found in the training dataset.
        research_field (str): Current research field the tool is set to.
        research_field_label_map (dict): List of all label ids and their names in the research field.
        unknown_label_id (int): The id of the unknown label.

    Returns:
        dict: Dictionary format of the COCO file.
    """
    master_dict = {
        "images": [],  # list of all images in the dataset
        "annotations": [],  # list of all annotations in the dataset
        "categories": [],  # list of all categories
    }
    
    for label_id in label_ids:
        if label_id == unknown_label_id:
            continue
        
        master_dict["categories"].append({
            "supercategory": research_field,
            "id":  research_field_label_map[label_id-1]["id"],
            "name": research_field_label_map[label_id-1]["name"]
        })
    
    return master_dict
        
def _create_sub_masks(label_mask:np.ndarray,
                      unique_label_id_list:list[int],
                      create_coco:bool = False,
                      crop_image_id:int = None,
                      master_dict:dict = None,
                      segment_image_id:int = None) -> dict:
    """Creates a dictionary of all sub masks of a segmented image. 
    If create_coco is true: creates a COCO file (json) of all sub masks converted to RLE format.

    Args:
        label_mask (np.ndarray): Label mask that will have sub masks extracted.
        unique_label_id_list (list[int]): All unique labels found in the segment image.
        create_coco (bool, optional): Flag to create a COCO file. Defaults to False.
        id (int, optional): Required for COCO, id of each mask. Defaults to None.
        master_dict (dict, optional): Required for COCO, dict that rle masks (COCO format) are added onto. Defaults to None.
        crop_image_id (int, optional): Required for COCO, image id (used to relate masks). Defaults to None.

    Returns:
        dict: All sub masks of a segmented image.
        
    Raises:
        Exception: Sub mask could not be created.        
    """
    try:
        sub_masks = {}
         # Creates a mask for every label id
        for label_id in unique_label_id_list:
            sub_masks[label_id] = np.zeros(label_mask.shape)            
            # Wherever the mask is equal to True it puts the label id of the pixel
            sub_masks[label_id] = np.where(label_mask == label_id, label_id, sub_masks[label_id])
            
            # Converts all masks of a segmented image into an RLE mask
            if create_coco and label_id != 0:
                sub_mask = sub_masks[label_id].astype(np.uint8)
                rle_mask = maskUtils.encode(np.asfortranarray(sub_mask))
                rle_mask['counts'] = rle_mask['counts'].decode('ascii')
                segment_area = maskUtils.area(rle_mask).astype(int)
                segment_box = maskUtils.toBbox(rle_mask).astype(int)
                master_dict["annotations"].append({
                    "id": crop_image_id,
                    "image_id": int(segment_image_id),
                    "category_id": int(label_id),
                    "segmentation": rle_mask,
                    "iscrowd": 0,
                    "area": segment_area.tolist(),
                    "bbox": segment_box.tolist()
                })              
                
        return sub_masks
    except Exception as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)