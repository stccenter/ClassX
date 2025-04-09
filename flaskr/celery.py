"""
    This module contains the celery tasks that are used to process
    images and upload them to the database. The tasks are called by the celery
    worker when an image is uploaded to the server.
"""

# Python standard imports
import os
from typing import List, AnyStr
from datetime import datetime, timezone

# third party imports


# local imports
from classxlib.database.model import OriginalImage, CropImage
from classxlib.database import is_default_user

from classxlib.file import merge_directory, get_file_size, format_database_path
from classxlib.image import (
    write_cv_image,
    write_hdf5_image,
    read_cv_image,
    read_hdf5_image,
)
from classxlib.image.process import (
    process_research_image,
    process_image_grid,
    crop_grid_square,
)

from . import celery
from .globals import STATIC_FOLDER, IMAGE_FOLDER, USER_UPLOAD_FOLDER
from .database import get_db


@celery.task(name="tasks.upload_original_image", track_started=True)
def upload_original_image(
    user_id: int,
    files: List[AnyStr],
    processed_savepath: AnyStr,
    research_field_id: int,
    upload_time: int,
) -> dict:
    """Post processing of the original image. This function is called when celery's
    queue has detected an image has been uploaded and sent to it.
    Created the actual database row of the image.

    Args:
        user_id (int): user id of the user who uploaded the image
        files (List[AnyStr]): file paths of the images
        processed_savepath (AnyStr): folder pass of where to store proceesed images of the user
        research_field_id (int): The research field id to associate the image with
        upload_time (int): when the image was uploaded

    Raises:
        error: Throws an error if failed to be viewable by celery

    Returns:
        dict: original image IDs as an array and the user id who uploaded them if successful
    """
    db = get_db()
    original_image_obj_id_list = []
    research_field = db.research_field_service
    original_image = db.original_image_service

    research_field_obj = research_field.get_by_id(research_field_id)

    upload_time = datetime.fromtimestamp(upload_time, timezone.utc)
    try:
        # Looping through each file
        for original_image_filepath in files:
            print(original_image_filepath, files)
            file_name = os.path.basename(original_image_filepath)

            # Calculating the size of the file in Megabytes
            file_size_mb = get_file_size(original_image_filepath)

            # Database Save Path
            original_image_database_filepath = format_database_path(
                original_image_filepath
            )

            # Functions to process the image by which domain it belongs.
            # Default domains have specialized processing pipelines
            image_db_path_dict, image_dim, creation_date, metadata_dict = (
                process_research_image(
                    image_path=original_image_filepath,
                    image_savepath=processed_savepath,
                    file_name=file_name,
                    research_field_obj=research_field_obj,
                )
            )

            # Creates a object under the OriginalImage class defined in model.py
            original_image_obj = OriginalImage(
                user_id=user_id,
                shared_by=None,
                shared_from=None,
                research_id=research_field_obj.id,
                name=file_name,
                alias=file_name,
                path=original_image_database_filepath,
                h5_path=image_db_path_dict["h5"],
                visualization_path=image_db_path_dict["visual"],
                thumbnail_path=image_db_path_dict["thumbnail"],
                crop_grid_path=image_db_path_dict["grid"],
                upload_time=upload_time,
                creation_date=creation_date,
                last_modified_date=upload_time,
                width=image_dim[0],
                height=image_dim[1],
                size=file_size_mb,
                file_type=research_field_obj.protocols["file_type"],
                mode=research_field_obj.protocols["mode"],
                metadata=metadata_dict,
            )
            # add fully proccessed image
            original_image.add_image(original_image_obj)
            original_image_obj_id_list.append(original_image_obj.id)
    except Exception as error:
        # print(traceback.print_tb(error.__traceback__))
        # file_list['invalid'].append(file_name)
        raise error
        # message = "Error Uploading"
        # return {'status':400, 'message':message,
        # "original_images":[], 'invalidfiles' : [], 'duplicatefiles':[]}

    celery.send_task(
        "tasks.auto_crop_image",
        args=[
            original_image_obj_id_list[0],
            research_field_obj.protocols["auto_grid_size"],
        ],
    )

    return {"original_images": original_image_obj_id_list, "uploader_id": user_id}


@celery.task(name="tasks.auto_crop_image")
def auto_crop_image(original_image_id: int, crop_size: int = 512):
    """Automatically crops an image based on a crop grid size.
    Images are trimmed automatically if a crop would
    result in more than 20% black. Due to boundry limits.

    Args:
        original_image_id (int): The id of the original image to crop.
        crop_size (int): The size of each crop plot on the grid.
        default 512 (All research fields use this as of now)
    """
    db = get_db()
    original_image_service = db.original_image_service
    crop_image_service = db.crop_image_service
    user_service = db.user_service

    # Retrieving the original image object based off the id.

    original_image_obj = original_image_service.get_image(original_image_id)

    print("AUTO CROPPING:", original_image_obj.name)
    print("CROP SIZE:", crop_size)

    # Getting the user object associated with the image.
    user_obj = user_service.get_by_id(original_image_obj.user_id)

    # Setting appropriate save directories based off the user
    if is_default_user(user_obj):
        # Default user has a different save directory
        crop_file_path = merge_directory(
            IMAGE_FOLDER, user_obj.username + "/WriteGUI/AutoCropImages"
        )
    else:
        # Standard user save directory
        crop_file_path = merge_directory(
            USER_UPLOAD_FOLDER, user_obj.username + "/WriteGUI/AutoCropImages"
        )

    # Preparing the preprocessed path and original adjusted paths.
    # We dont have a static folder here only ./images!
    visualization_path = merge_directory(
        STATIC_FOLDER, original_image_obj.visualization_path
    )
    h5_path = merge_directory(STATIC_FOLDER, original_image_obj.h5_path)

    print("PREPROCESSED PATH:", visualization_path)
    print("ORIGINAL IMAGE PATH:", h5_path)

    # Reading the images
    visualization_image = read_cv_image(visualization_path)
    h5_image = read_hdf5_image(h5_path)

    # Padding the images to make crop sizes line up correctly
    padded_visualization_image = process_image_grid(
        visualization_image, crop_size=crop_size, draw_lines=False
    )
    padded_h5_image = (
        process_image_grid(h5_image, crop_size=crop_size, draw_lines=False)
        if h5_image.any()
        else None
    )

    # Getting the grid counts for amount of crops/grid squares
    grid_square_count = (
        padded_visualization_image.shape[1] // crop_size,
        padded_visualization_image.shape[0] // crop_size,
    )

    # Getting the time for saving onto the crop images.
    date_utc = datetime.now(timezone.utc)
    date_time = date_utc.strftime("%m_%d_%Y_%H_%M_%S")

    # Loop through each grid square.
    for x in range(grid_square_count[0]):
        for y in range(grid_square_count[1]):
            # Find the grid position and adjust to be the crop width and height dimensions
            # The grid position is now the actual crop point from the image. The crop point
            # is the bottom right corner of a cropped image.
            # The auto grid size is added on at the end due to it being the bottom right corner.
            grid_position_x = (x * crop_size) + crop_size
            grid_position_y = (y * crop_size) + crop_size

            # Getting the database object for the cropped i
            # mage by matching the original image id and crop point.
            # This function only retrieves 'auto'(automatic)
            # cropped images to avoid crop point overlaps with 'man'(manual) cropped images
            crop_image_obj = crop_image_service.get_user_image_from_grid(
                original_image_id,
                (grid_position_x, grid_position_y),
                user_id=user_obj.id,
                default_id=db.DEFAULT_ID,
            )

            # This is checking if the crop image already exists
            if crop_image_obj is not None:
                continue
            # Processing the crop squares
            crop_image, h5_crop_image, x_span, y_span, x_index, y_index = (
                crop_grid_square(
                    padded_visualization_image,
                    padded_h5_image,
                    (x, y),
                    [crop_size, crop_size],
                    [crop_size, crop_size],
                )
            )

            # Grid index of the crop
            crop_index = f"_{x_index:03d}_{y_index:03d}"

            # The file name for the new cropped image
            crop_filename = "cropImage_" + date_time + crop_index + ".png"

            # Preparing file save path and the formatted database path
            crop_file_savepath = merge_directory(crop_file_path, crop_filename)
            crop_database_path = format_database_path(crop_file_savepath)

            # If there is the original adjusted image available save that as well
            if h5_crop_image.any():
                h5_crop_filename = "h5_" + crop_filename.replace(".png", ".h5")
                h5_crop_file_savepath = merge_directory(
                    crop_file_path, h5_crop_filename
                )
                h5_crop_database_path = format_database_path(h5_crop_file_savepath)
                write_hdf5_image(h5_crop_image, h5_crop_file_savepath)
            else:
                h5_crop_database_path = None

            # Writing images to disk
            write_cv_image(crop_image, crop_file_savepath)

            # Creating cropped image object for database
            crop_image_obj = CropImage(
                user_id=user_obj.id,
                shared_by=None,
                shared_from=None,
                original_image_id=original_image_obj.id,
                research_id=original_image_obj.research_id,
                name=crop_filename,
                visualization_path=crop_database_path,
                h5_path=h5_crop_database_path,
                last_modified_date=datetime.utcnow(),
                width=x_span,
                height=y_span,
                crop_size=crop_size,
                crop_type="auto",
            )

            # These statements are removed due to overload on I/O
            # print(f'Creating object for cropped image {crop_filename} at {crop_file_savepath}')
            # print(f'Saving cropped image')
            # Saving the object in the database
            crop_image_service.add_image(crop_image_obj)
