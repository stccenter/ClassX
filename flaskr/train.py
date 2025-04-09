"""
this module contains the API endpoints for training images
"""

# pylint: disable=invalid-name

# Python Standard Library Imports
import io
import json
import os
import shutil
import traceback
from datetime import datetime, timezone

import cv2
import numpy as np

# Python Third Party Imports
from flask import (
    Blueprint,
    make_response,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from flask import current_app as app
from skimage.util import img_as_ubyte

from classxlib.color import color_labeled_image
from classxlib.database import is_default_user
from classxlib.database.model import (
    LabelImage,
    TrainingFile,
    User,
)

# Local Library Imports
from classxlib.file import format_database_path, merge_directory, verify_directory
from classxlib.image import image_as_b64, read_cv_image, read_hdf5_image, write_cv_image
from classxlib.image._read import read_fits_image
from classxlib.label import get_unknown_label_from_research_field, remove_small_labels
from classxlib.segment import (
    get_labeled_segment_count,
    read_segment_image,
    update_segment_image_info,
)
from classxlib.train import (
    classify_image,
    delete_image_from_file,
    get_unique_parent_ids_from_link,
    read_training_file,
    write_training_file,
)
from classxlib.train._export import (
    coco_init,
    export_as_coco,
    export_image_file_type,
    export_mask_file_type,
    extract_label_mask_from_image,
)

from .database import get_db
from .globals import ADMIN_UPLOAD_FOLDER, STATIC_FOLDER, USER_UPLOAD_FOLDER
from .oauth import get_oauth

TRAIN = Blueprint("train", __name__, template_folder="/templates")


@TRAIN.route("/saveTrainingFile/", methods=["GET", "POST"], endpoint="saveTrainingFile")
def save_training_file():
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service
    research_field_service = db.research_field_service
    crop_image_service = db.crop_image_service
    original_image_service = db.original_image_service
    training_file_service = db.training_file_service
    label_image_service = db.label_image_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # get request arguments
    # Save Type for the training file if 1 then creating a new file,
    # if 2 we are appending to an existing dataset
    save_type = request.args.get("save_type", type=str)

    # File Type of the training file
    file_type = request.args.get("file_type", type=str)

    # Name of the training file
    training_dataset_filename = request.args.get("training_file_name", type=str)

    # ID of the segment image to process into the training file
    segment_image_id = request.args.get("segment_image_id", type=int)

    # Flag to remove small labels before saving training file
    remove_small = request.args.get("remove_small_labels", type=bool)

    # The precentage that segments
    area_removal_percentage = request.args.get("area_removal_percentage", type=float)

    # get segmented image object
    segment_image_obj = segment_image_service.get_user_image(
        segment_image_id=segment_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # Formatting path to segment image
    segment_image_path = merge_directory(STATIC_FOLDER, segment_image_obj.segment_path)

    # Reading segment image into memory
    segment_image, segment_info = read_segment_image(segment_image_path)

    # Gettting cropped image object
    crop_image_obj = crop_image_service.get_image(
        crop_image_id=segment_image_obj.crop_image_id
    )

    # Getting the original image associated with crop image
    original_image_obj = original_image_service.get_image(
        original_image_id=crop_image_obj.original_image_id
    )

    # Getting research associated with the segment image object
    research_field_obj = research_field_service.get_by_id(segment_image_obj.research_id)

    # Verifying research field exsistence
    if research_field_obj is None:
        return {"status": 404, "error": "Research Field not found"}

    print("Saving the file....")

    # alert for duplicated cropped image in the same file
    alert = None

    print(
        f"Segmented image {segment_image_obj.name} {segment_image_obj.id} \
        is being processed {segment_image_obj.segment_path}."
    )

    # Remove small labels
    if remove_small:
        print("Removing small labels...")
        unknown_label_id = get_unknown_label_from_research_field(research_field_obj)
        unique_label_id_list: np.ndarray = np.unique(segment_info[:, 1])
        unique_label_id_list[np.where(unique_label_id_list == unknown_label_id)] = 0
        segment_info = remove_small_labels(
            segment_image,
            segment_info,
            unique_label_id_list,
            area_removal_percentage,
            unknown_label_id,
        )
        update_segment_image_info(segment_info, segment_image_path)

    # pylint: disable=unused-variable
    total_segment_count, labeled_segment_count, unlabeled_segment_count = (
        get_labeled_segment_count(segment_info)
    )

    # Verifying all segments are labeled
    if unlabeled_segment_count > 0:
        return {"status": 400, "error": "Not all segments are labeled"}

    # Setting OS file path for training dataset
    if is_default_user(user_obj):
        if file_type == "HDF5":
            file_path = merge_directory(
                ADMIN_UPLOAD_FOLDER, user_obj.username + "/WriteGUI/HDF5"
            )
    else:
        if file_type == "HDF5":
            file_path = merge_directory(
                USER_UPLOAD_FOLDER, user_obj.username + "/WriteGUI/HDF5"
            )

    # This is a future proof function incase there is
    # additional datasets supported it will ensure the filepath for them exists
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    try:
        # SAVE TYPE 1:Saving a new training dataset file
        if save_type == "1":
            if file_type == "HDF5":
                print("inside save type 1 HDF5")
                training_file_obj = training_file_service.get_user_file_by_name(
                    training_file_name=training_dataset_filename, user_id=user_obj.id
                )
                if training_file_obj is not None:
                    return {
                        "status": 400,
                        "alert": alert,
                        "error": "File already exists under that name",
                    }

                # Formatting the save path for the training file
                training_file_save_path = merge_directory(
                    file_path, training_dataset_filename
                )

                # Creating the HDF5 file
                write_training_file(
                    training_file_save_path,
                    STATIC_FOLDER,
                    segment_image_obj,
                    crop_image_obj,
                    original_image_obj,
                    overwrite=True,
                )

                # Creating the database save paths
                training_file_database_path = format_database_path(
                    file_path + "/" + training_dataset_filename
                )
                model_database_path = format_database_path(file_path)

                # save the numbers as 0 for now, we will alter later
                training_file_obj = TrainingFile(
                    user_id=user_obj.id,
                    research_id=research_field_obj.id,
                    shared_by=None,
                    shared_from=None,
                    file_name=training_dataset_filename,
                    file_path=training_file_database_path,
                    model_path=model_database_path,
                    label_count={"labels": "none"},
                )
                training_file_service.add_file(training_file_obj)

        else:
            # with h5py.File(tds_filename, "r") as infile:
            # after saving label file, save colored image, name it as labelid_segid_color_image.png
            # check if the image already exists, if so remove it and save again

            print("inside save 2")
            if file_type == "HDF5":
                print("inside save type 2 HDF5")
                training_file_obj = training_file_service.get_user_file_by_name(
                    training_file_name=training_dataset_filename, user_id=user_obj.id
                )
                if training_file_obj is None:
                    return {
                        "status": 400,
                        "alert": alert,
                        "error": "User does not have permission to edit this dataset",
                    }

                if training_file_obj.shared_from is not None:
                    training_file_obj = training_file_service.get_file(
                        training_file_obj.shared_from
                    )
                    user_obj = user_service.get_by_id(training_file_obj.user_id)
                    # Setting OS file path for training dataset
                    if is_default_user(user_obj):
                        if file_type == "HDF5":
                            file_path = merge_directory(
                                ADMIN_UPLOAD_FOLDER,
                                user_obj.username + "/WriteGUI/HDF5",
                            )
                    else:
                        if file_type == "HDF5":
                            file_path = merge_directory(
                                USER_UPLOAD_FOLDER, user_obj.username + "/WriteGUI/HDF5"
                            )

                training_file_path = merge_directory(
                    file_path, training_dataset_filename
                )

                # Creating the HDF5 file
                write_training_file(
                    training_file_path,
                    STATIC_FOLDER,
                    segment_image_obj,
                    crop_image_obj,
                    original_image_obj,
                    overwrite=False,
                )

        # Getting the visual image
        visual_image_path = merge_directory(
            STATIC_FOLDER, crop_image_obj.visualization_path
        )
        visual_image = read_cv_image(visual_image_path)

        # Colored label image
        color_image = color_image = color_labeled_image(
            input_image=visual_image,
            segment_image=segment_image,
            segment_info=segment_info,
            research_label_map=research_field_obj.label_map,
            alpha=0.7,
        )
        print("Color image is generated.")

        # Getting current date
        date = datetime.now(timezone.utc)

        # Setting save path for color image
        if is_default_user(user_obj):
            color_image_path = merge_directory(
                ADMIN_UPLOAD_FOLDER, user_obj.username + "/WriteGUI/ColorImages"
            )
        else:
            color_image_path = merge_directory(
                USER_UPLOAD_FOLDER, user_obj.username + "/WriteGUI/ColorImages"
            )

        # Name of the color image file
        color_image_file_name = (
            str(training_file_obj.id) + "_" + str(segment_image_id) + "_color_image.png"
        )

        # Save path for the colored image
        color_image_save_path = merge_directory(color_image_path, color_image_file_name)

        # Checking to see if there is an already existing jump
        label_image_obj = label_image_service.get_image_from_parents(
            segment_image_id=segment_image_id, training_file_id=training_file_obj.id
        )

        # Check if the file already exists
        if label_image_obj is not None:
            # Remove old color image
            old_color_image_path = merge_directory(
                STATIC_FOLDER, label_image_obj.color_image_path
            )
            os.remove(old_color_image_path)

            # Write the new color image
            write_cv_image(color_image, color_image_save_path)

            # Alter the table with the new date
            label_image_service.update_last_modified(
                segment_image_id=segment_image_id,
                training_file_id=training_file_obj.id,
                new_date=date,
            )
        else:
            # if it doesn't exist write the new image
            write_cv_image(color_image, color_image_save_path)

            # Formatting the path for database
            color_image_database_path = format_database_path(color_image_save_path)

            # Creating the object for the database
            label_image_obj = LabelImage(
                user_id=training_file_obj.user_id,
                training_file_id=training_file_obj.id,
                segment_image_id=segment_image_id,
                color_image_path=color_image_database_path,
                last_modified=date,
            )

            # Saving to database
            label_image_service.add_image(label_image_obj)

        # fetch all training files
        training_file_obj_list = training_file_service.get_user_research_files(
            research_field_id=research_field_obj.id,
            user_id=user_obj.id,
            default_id=db.DEFAULT_ID,
        )
        return {"status": 200, "alert": alert, "label_files": training_file_obj_list}
    except Exception as error:
        print(error)
        traceback.print_tb(error.__traceback__)
        return {"status": 400, "alert": alert, "error": "Saving Image to file failed"}


@TRAIN.route("/autoLabelImage/", methods=["GET", "POST"], endpoint="autoLabelImage")
def auto_label_image():
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service
    crop_image_service = db.crop_image_service
    research_field_service = db.research_field_service
    training_file_service = db.training_file_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving segment image id from front-end
    segment_image_id = request.args.get("segment_image_id", type=int)
    if segment_image_id is None:
        return {"status": 400, "error": "invalid segmented image id"}

    # Probability threshold for the algorithm to use. Also could be called the confidence threshold
    probability_threshold = request.args.get("prob_threshold", type=float)
    if probability_threshold is None:
        return {"status": 400, "error": "invalid probability threshold"}

    # ID of the model algorithm to use
    algorithm_id = request.args.get("algorithm_id", type=int)
    if algorithm_id is None or algorithm_id < 0 or algorithm_id > 3:
        return {"status": 400, "error": "invalid algorithm"}

    # Retrieving the id of the label file to use
    training_file_id = request.args.get("training_file_id", type=int)
    training_file_obj = training_file_service.get_file(
        training_file_id=training_file_id
    )
    print(training_file_obj)
    print("LABEL ID", training_file_id)
    # Dictionary mapping for each model algorithm id
    model_mapping = {0: "svm", 1: "rf", 2: "xgb", 3: "knn"}

    # Loading the segment image object from database
    segment_image_obj = segment_image_service.get_user_image(
        segment_image_id=segment_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # Formatting segment image path
    segment_image_path = merge_directory(STATIC_FOLDER, segment_image_obj.segment_path)

    # Retrieving the segment image and info from disk
    segment_image, segment_info = read_segment_image(segment_image_path)

    # Getting the associated crop image from database
    crop_image_obj = crop_image_service.get_image(segment_image_obj.crop_image_id)

    # Formatting the path to load the correct crop image
    if crop_image_obj.h5_path is not None:
        h5_crop_image_path = merge_directory(STATIC_FOLDER, crop_image_obj.h5_path)
        crop_image = read_hdf5_image(h5_crop_image_path)
        if len(crop_image.shape) == 2:
            crop_image = np.dstack((crop_image, crop_image, crop_image))
    else:
        crop_image_path = merge_directory(
            STATIC_FOLDER, crop_image_obj.visualization_path
        )
        crop_image = read_cv_image(crop_image_path)

    # This is a compatibility feature that will be removed in the future
    # Calc Attributes requires unsigned 8 bit style images
    crop_image = img_as_ubyte(crop_image)

    # Another compatibility feature since tif images are
    # originally in the shape (3,x,y) unlike standard images which are (x,y,3)
    # Reshaping the image color channels
    r, g, b = cv2.split(crop_image)
    cropped_image_reshape = np.stack((r, g, b))
    # original_image_obj = app.original_image_service.get_image_by_id(crop_image_obj.original_id)

    research_field_obj = research_field_service.get_by_id(
        research_id=segment_image_obj.research_id
    )
    research_label_map = research_field_obj.label_map
    for label in research_label_map:
        if label["name"].lower() == "unknown":
            unknown_label_id = label["id"]
            break

    # File directory for the model file
    model_file_directory = merge_directory(STATIC_FOLDER, training_file_obj.model_path)

    # Naming convention is {label_file_id} + _ + {file_name} + _ + {algorithm_id}
    model_file_name = (
        str(training_file_obj.id)
        + "_"
        + training_file_obj.file_name.split(".")[0]
        + "_"
        + model_mapping[algorithm_id]
        + ".pkl"
    )

    # List of files in model directory
    model_files = os.listdir(model_file_directory)

    # File path for the model file
    model_file_path = merge_directory(model_file_directory, model_file_name)

    # Checking if the model already exists/has been trained
    if model_file_name in model_files:

        # If it exists do not need to retrain
        needs_retrain = False

        # Getting the last time the file was modified
        timestamp = os.path.getmtime(model_file_path)
        last_modified = datetime.fromtimestamp(timestamp, timezone.utc)

        # Today's time
        now = datetime.now(timezone.utc)

        # retrain if it is too long since last modify date
        # TODO make this check for new images or auto retrain with new images
        if (now - last_modified).days >= app.config["MODEL_RETRAIN_SPAN"]:
            needs_retrain = True
    else:
        # If file doesn't exist its needs to be trained
        needs_retrain = True
    needs_retrain = True
    # Image type for model analysis
    image_type = "srgb"

    # The training file to use
    target_training_file = merge_directory(STATIC_FOLDER, training_file_obj.file_path)

    # Loading the training dataset
    training_dataset = read_training_file(
        target_training_file, image_type, int(unknown_label_id)
    )

    # classify image
    classified_flags = classify_image(
        cropped_image_reshape,
        segment_image,
        training_dataset,
        [image_type, research_field_obj.name],
        probability_threshold,
        algorithm_id,
        model_file_path,
        needs_retrain,
    )

    # loop through to do return count for front end
    for segment in segment_info:
        if classified_flags[segment[0]] == -1:
            segment_info[segment[0] - 1][1] = 0
        else:
            segment_info[segment[0] - 1][1] = int(classified_flags[segment[0]])
    update_segment_image_info(segment_info, segment_image_path)

    # Gettting the counts of labeled and unlabeled segments
    total_segment_count, labeled_segment_count, unlabeled_segment_count = (
        get_labeled_segment_count(segment_info)
    )

    # Formatting path to marked image
    marked_image_path = merge_directory(
        STATIC_FOLDER, segment_image_obj.marked_image_path
    )

    # Reading marked image
    marked_image = read_cv_image(marked_image_path, noflag=True)
    # done labeling, draw the color image
    # Color the labeled segments in the image
    # Skips logic if there is no labeled segments to avoid unnecessary processing
    if unlabeled_segment_count == total_segment_count:
        color_image = marked_image
    else:
        color_image = color_labeled_image(
            input_image=marked_image,
            segment_image=segment_image,
            segment_info=segment_info,
            research_label_map=research_field_obj.label_map,
            alpha=session["label_opacity"],
        )
    print("Color image is generated.")

    # Converting image to base 64 for front-end return
    base64_image = image_as_b64(color_image)

    return {
        "status": 200,
        "image_string": base64_image,
        "labeled_segments": labeled_segment_count,
        "total_segments": labeled_segment_count,
        "label_class_list": np.column_stack(
            np.unique(segment_info[:, 1], return_counts=True)
        ).tolist(),
    }


@TRAIN.route(
    "/deleteImageFromTrainingFile/",
    methods=["GET", "POST"],
    endpoint="deleteImageFromTrainingFile",
)
def delete_image_from_training_file():
    """Delete an image from a training file

    Request Args:
        uuid(str): User's uuid to verify the session token against database.
        training_file_id(int): The id of the training file.
        segment_image_id(int): The id of the segment image.

    Returns:
        dict: {"status": 200}
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    training_file_service = db.training_file_service
    label_image_service = db.label_image_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # get request arguments
    training_file_id = request.args.get("training_file_id", type=int)
    segment_image_id = request.args.get("segment_image_id", type=int)
    print(training_file_id)
    training_file_obj = training_file_service.get_user_file(
        training_file_id=training_file_id, user_id=user_obj.id
    )

    file_path = merge_directory(STATIC_FOLDER, training_file_obj.file_path)
    delete_image_from_file(file_path, segment_image_id)
    label_image_obj = label_image_service.get_image_from_parents(
        segment_image_id=segment_image_id, training_file_id=training_file_obj.id
    )
    color_image_path = merge_directory(STATIC_FOLDER, label_image_obj.color_image_path)
    os.remove(color_image_path)
    label_image_service.remove_image(label_image_obj)

    return {"status": 200}


# TODO Redo this logic with the new shared_from and shared_by
@TRAIN.route(
    "/shareTrainingFileToUsers/", methods=["POST"], endpoint="shareTrainingFileToUsers"
)
def share_training_file_to_users():
    """Share traning file to other users

    Request Args:
        uuid(str): User's uuid to verify the session token against database.
        recipient_name_list(list): List of usernames to share the file with.
        training_file_id(int): The id of the training file.

    Returns:
        _type_: _description_
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    training_file_service = db.training_file_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    request_data = request.get_json()

    username_share_list = request_data["recipient_name_list"]
    training_file_id = request_data["training_file_id"]

    # read label file and get all original image, crop image, segmented image
    training_file_obj = training_file_service.get_file(training_file_id)

    if training_file_obj is None:
        return {"status": 404, "error": "Label file not found"}

    if training_file_obj.shared_from is not None and (
        training_file_obj.user_id != user_obj.id and user_obj.user_level != 3
    ):
        return {"status": 404, "error": "User does not have access to share this file"}

    if len(username_share_list) <= 0:
        return {"status": 404, "error": "Recipient list is empty"}

    failed_recipients, passed_recipient = [], []

    # Looping through each user
    for username in username_share_list:
        try:
            # Creating the share file object with reference to user it was shared from
            share_training_file_obj = TrainingFile(
                user_id=user_service.get_by_username(username).id,
                research_id=training_file_obj.research_id,
                shared_by=user_obj.id,
                shared_from=training_file_obj.id,
                file_name=training_file_obj.file_name,
                file_path=training_file_obj.file_path,
                model_path=training_file_obj.model_path,
                label_count=training_file_obj.label_count,
            )
            # Adding it to database
            training_file_service.add_file(share_training_file_obj)
            passed_recipient.append(username)
        except Exception as error:
            print("SHARING FAILED")
            traceback.print_tb(error.__traceback__)
            # Appending the failed name list if something goes wrong
            failed_recipients.append(username)

    # after everything is done, return 200
    return {
        "status": 200,
        "failed_list": failed_recipients,
        "passed_list": passed_recipient,
    }


@TRAIN.route(
    "/getTrainingFileContents/", methods=["GET"], endpoint="getTrainingFileContents"
)
def view_training_file():
    """View the contents of a training file

    Request Args:
        uuid(str): User's uuid to verify the session token against database.
        training_file_id(int): The id of the training file

    Returns:
        render_template: viewlabeledfiles.html template with the training file contents
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service
    crop_image_service = db.crop_image_service
    label_image_service = db.label_image_service
    training_file_service = db.training_file_service
    research_field_service = db.research_field_service
    original_image_service = db.original_image_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving label file id from arguments
    training_file_id = request.args.get("training_file_id", type=int)
    print("training_file_id:", training_file_id)
    # read label file and get all original image, crop image, segmented image
    training_file_obj = training_file_service.get_user_file(
        training_file_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )
    if training_file_obj is None:
        return {"status": 404, "error": "training file not found"}
    if training_file_obj.shared_from is not None:
        training_file_id = training_file_obj.shared_from

    # Getting domain associated with the segment image object
    research_field_obj = research_field_service.get_by_id(training_file_obj.research_id)

    # Verifying Domain exsistence
    if research_field_obj is None:
        return {"status": 404, "error": "Research Field not found"}

    segment_image_obj_list, crop_image_obj_list = [], []

    if ".h5" in training_file_obj.file_name:
        h5_path = os.path.join(STATIC_FOLDER, training_file_obj.file_path)
        segment_id_link = read_training_file(h5_path, "srgb", return_id_link=True)[2]
        segment_image_id_list, crop_image_id_list, original_image_id_list = (
            get_unique_parent_ids_from_link(
                segment_id_link, return_crop_id=True, return_original_id=True
            )
        )
        segment_image_obj_list = segment_image_service.get_images(segment_image_id_list)
        crop_image_obj_list = crop_image_service.get_images(crop_image_id_list)
        original_image_obj_list = original_image_service.get_images(
            original_image_id_list
        )

        label_image_obj_list = label_image_service.get_images_from_parent_file(
            training_file_id
        )
        return {
            "training_file":training_file_obj,
            "training_file_id":training_file_obj.id,
            "file_type":"HDF5",
            "crop_images":crop_image_obj_list,
            "segment_images":segment_image_obj_list,
            "original_images":original_image_obj_list,
            "label_images":label_image_obj_list,
            "label_map":research_field_obj.label_map,
        }


# TODO: Add page offset
@TRAIN.route("/getTrainingFiles/", methods=["GET"], endpoint="getTrainingFiles")
def get_training_files():
    """Get all training files associated with a user

    Request Args:
        uuid(str): User's uuid to verify the session token against database.

    Returns:
        _type_: _description_
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    training_file_service = db.training_file_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving domain object from session
    research_field_id = session["research_field"]["id"]
    training_file_obj_list = training_file_service.get_user_research_files(
        research_field_id=research_field_id,
        user_id=user_obj.id,
        default_id=db.DEFAULT_ID,
    )

    return {"status": 200, "training_files": training_file_obj_list}


@TRAIN.route("/viewTrainingFiles/", methods=["GET"], endpoint="viewTrainingFiles")
def view_training_files():
    """View all training files associated with a user

    request Args:
        uuid(str): User's uuid to verify the session token against database.

    Returns:
        render_template: "view.html" template with the training files
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    label_image_service = db.label_image_service
    training_file_service = db.training_file_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving domain object from session
    research_field = session["research_field"]
    training_file_obj_list = training_file_service.get_user_research_files(
        # TODO: set to solaor for now, need make it dynamic
        research_field_id=research_field['id'],
        user_id=user_obj.id,
        default_id=db.DEFAULT_ID,
    )

    file_uploader_id_list = list(
        map(
            lambda training_file_obj: (
                training_file_obj.shared_by
                if training_file_obj.shared_by is not None
                else training_file_obj.user_id
            ),
            training_file_obj_list,
        )
    )
    uploader_names = list(
        map(
            lambda user_id: (
                user_service.get_by_id(user_id).username
                if user_id is not None
                else user_obj.username
            ),
            file_uploader_id_list,
        )
    )

    last_modified_dates = list(
        map(
            lambda training_file_obj: (
                label_image_service.get_last_modified_from_parent_file(
                    training_file_obj.shared_from
                )
                if training_file_obj.shared_from is not None
                else label_image_service.get_last_modified_from_parent_file(
                    training_file_obj.id
                )
            ),
            training_file_obj_list,
        )
    )

    last_modified_dates = [
        (
            label_image_obj.last_modified.replace(tzinfo=timezone.utc)
            if label_image_obj is not None
            else datetime.now(timezone.utc)
        )
        for label_image_obj in last_modified_dates
    ]

    combined_data = list(
        zip(training_file_obj_list, last_modified_dates, uploader_names)
    )
    sorted_data = sorted(combined_data, key=lambda x: x[1], reverse=True)
    # return render_template("view.html", sorted_data=sorted_data)
    return sorted_data


@TRAIN.route("/exportTrainingImages/", methods=["GET"], endpoint="exportTrainingImages")
def export_training_images():
    """API ENDPOINT
    Exports training hdf5 images and masks, also creates a JSON with their relative paths.
    Currently supports export in:

    Session Args:
        uuid(str): User's uuid to verify the session token against database.

    Request Args:
        training_file_id (int): ID of the training file to export
        image_file_type (str): desired image file type
        mask_file_type (str): desired mask file type
        visual_image_check(bool): flag that determines if crop images are also exported.

    Returns:
        str: Path of the zipped folder.
    """

    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service
    crop_image_service = db.crop_image_service
    training_file_service = db.training_file_service
    research_field_service = db.research_field_service
    original_image_service = db.original_image_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving desired data types from front-end request
    user_image_file_type = request.args.get("image_file_type", type=str)
    user_mask_file_type = request.args.get("mask_file_type", type=str)
    visual_image_check = request.args.get("visual_image_check", type=int)

    # Getting the user's training files
    training_file_id = request.args.get(
        "training_file_id", type=int
    )  # For front-end requests

    training_file_obj = training_file_service.get_file(
        training_file_id=training_file_id
    )

    if training_file_obj is None:
        response = make_response(("", 404, {"error": "training file not found"}))
        return response

    # Paths for new directories
    TRAINING_FILE_NAME = training_file_obj.file_name.split(".")[0]
    if is_default_user(user_obj):
        EXPORT_DIR_PATH = merge_directory(
            ADMIN_UPLOAD_FOLDER, f"{user_obj.username}/export"
        )
    else:
        EXPORT_DIR_PATH = merge_directory(
            USER_UPLOAD_FOLDER, f"{user_obj.username}/export"
        )

    FULL_TRANING_DIR_PATH = merge_directory(EXPORT_DIR_PATH, TRAINING_FILE_NAME)
    FULL_EXPORT_IMAGES_PATH = merge_directory(FULL_TRANING_DIR_PATH, "images")
    FULL_EXPORT_MASKS_PATH = merge_directory(FULL_TRANING_DIR_PATH, "masks")
    if visual_image_check == 1:
        FULL_EXPORT_VISUAL_PATH = merge_directory(FULL_TRANING_DIR_PATH, "visuals")
        verify_directory(FULL_EXPORT_VISUAL_PATH)

    # Create a new export directory and its sub dirs
    verify_directory(FULL_TRANING_DIR_PATH)
    verify_directory(FULL_EXPORT_IMAGES_PATH)
    verify_directory(FULL_EXPORT_MASKS_PATH)

    # Full path of the training image
    training_file_path = merge_directory(STATIC_FOLDER, training_file_obj.file_path)

    # Get research field for labels
    research_field_obj = research_field_service.get_by_id(
        research_id=training_file_obj.research_id
    )
    if research_field_obj is None:
        return make_response(("", 404, {"error": "research field not found"}))

    research_field_label_map = research_field_obj.label_map
    unknown_label_id = get_unknown_label_from_research_field(research_field_obj)

    # Initializes 2 fields
    # label_vector: label ids for each row of the training data
    # segment_id_link: contains the row id, segment id, crop id, original image id
    label_vector, _, segment_id_link = read_training_file(
        training_file_path, "srgb", return_id_link=True
    )

    # Increase the dimensions of label_vector to merge with segment_id_link (from 1D to 2D)
    label_vector = label_vector[:, np.newaxis]

    # Combines label_vector and segment_id_link to form one table (label_vector is now column 0)
    combined_data = np.hstack((label_vector, segment_id_link))

    # Array of all segment ids (used to access rows of segement_id_link
    segment_id_array = segment_id_link[:, 1]

    # Gets each unique segment in the training file
    unique_segment_id_list = np.unique(segment_id_link[:, 1])

    # Creates a key to the label ids at the top of the JSON file
    training_file_label_ids = np.unique(combined_data[:, 0])
    master_dict = coco_init(
        training_file_label_ids,
        research_field_obj.name,
        research_field_label_map,
        unknown_label_id,
    )

    # Exctracting labels and masks from each segment for exporting
    image_ind = 0
    coco_id = [1]
    original_images = {}
    for segment_image_id in unique_segment_id_list:
        segment_image_obj = segment_image_service.get_image(segment_image_id)
        segment_image, _ = read_segment_image(
            segment_image_path=segment_image_obj.segment_path,
            base_directory=STATIC_FOLDER,
        )
        if segment_image_obj is None:
            return make_response(("", 404, {"error": "segment image not found"}))

        # Getting user's cropped images
        crop_image_obj = crop_image_service.get_image(
            crop_image_id=segment_image_obj.crop_image_id  # for testing
        )
        if crop_image_obj is None:
            return make_response(("", 404, {"error": "crop image not found"}))

        crop_image_h5_path = merge_directory(STATIC_FOLDER, crop_image_obj.h5_path)

        # Data of specified segment
        specified_segment = combined_data[segment_id_array == segment_image_id]

        # Get original image metadata and add to JSON
        original_image_obj = original_image_service.get_image(
            original_image_id=specified_segment[
                0, 4
            ]  # original image id (row 0, col 4)
        )
        if original_image_obj is None:
            return make_response(("", 404, {"error": "original image not found"}))

        # Extract all unique label ids within one image
        # JSON is update with a list of label ids
        unique_label_id_list: np.ndarray = np.unique(specified_segment[:, 0])
        unique_label_id_list[np.where(unique_label_id_list == unknown_label_id)] = 0

        # Updating training dict (JSON)
        master_dict["images"].append(
            {
                "original_image_metadata": original_image_obj.metadata,
                "file_name": crop_image_obj.name,
                "height": crop_image_obj.height,
                "width": crop_image_obj.width,
                "date_captured": original_image_obj.creation_date.isoformat(),
                "image_path": str,
                "mask_path": str,
                "visual_path": str,
                "id": crop_image_obj.id,
            }
        )
        export_paths = master_dict["images"][image_ind]
        image_ind += 1
        
        # Export solar data
        # if research_field_obj.name == "Heliophysics":
        #     try:
        #         original_solar_img_path = merge_directory(STATIC_FOLDER, original_image_obj.path)
        #         solar_img_data, _, solar_img_map = read_fits_image(original_solar_img_path, index=1)
        #         print("Fits size:", solar_img_data.shape)
                
        #         solar_img_viz_path = merge_directory(STATIC_FOLDER, original_image_obj.visualization_path)
        #         solar_img_viz = read_cv_image(solar_img_viz_path)
        #         print("Viz size:", solar_img_viz.shape)
                
        #         bottom_right = (crop_image_obj.width, crop_image_obj.height)
        #         top_right = (bottom_right[0], bottom_right[1] - crop_image_obj.crop_size)
        #         bottom_left = (bottom_right[0] - crop_image_obj.crop_size, bottom_right[1])
        #     except Exception as error:
        #         print(error)
        #         traceback.print_tb(error.__traceback__)
        #         return make_response(("", 404, {"error": "solar data not exported"}))
        
        # Moves all cropped images into images folder for export (file type determined by user)
        # Updates JSON with image relative path (tries to find cropped images)
        try:
            full_image_name = os.path.basename(crop_image_h5_path)
            image_file_name, _ = os.path.splitext(full_image_name)
            image_file_type = (
                "png" if "png" in user_image_file_type else user_image_file_type
            )
            export_image_path = merge_directory(
                FULL_EXPORT_IMAGES_PATH, image_file_name + f".{image_file_type}"
            )
            export_image_file_type(
                crop_image_h5_path, export_image_path, user_image_file_type
            )
            export_paths["image_path"] = merge_directory(
                TRAINING_FILE_NAME, f"images/{image_file_name}.{image_file_type}"
            )
        except Exception as error:
            print(error)
            traceback.print_tb(error.__traceback__)
            return make_response(
                ("", 404, {"error": "Crop image could not be converted"})
            )

        # Copies cropped images (visuals) onto the export directory
        try:
            if visual_image_check == 1:
                crop_image_visual_path = merge_directory(
                    STATIC_FOLDER, crop_image_obj.visualization_path
                )
                file_name = os.path.basename(crop_image_visual_path)
                visual_export_path = merge_directory(FULL_EXPORT_VISUAL_PATH, file_name)
                shutil.copyfile(crop_image_visual_path, visual_export_path)
                export_paths["visual_path"] = merge_directory(
                    TRAINING_FILE_NAME, f"visuals/{file_name}"
                )
            else:
                export_paths["visual_path"] = None
        except Exception as error:
            print(error)
            traceback.print_tb(error.__traceback__)
            return make_response(("", 404, {"error": "Visual image export failed"}))

        # Getting label mask from segmented image
        label_mask = extract_label_mask_from_image(
            segment_image, specified_segment, unique_label_id_list, unknown_label_id
        )

        # Converts masks into coco format
        try:
            export_as_coco(
                coco_id, crop_image_obj.id, label_mask, master_dict, unique_label_id_list
            )
        except Exception as error:
            print(error)
            traceback.print_tb(error.__traceback__)
            return make_response(("", 404, {"error": "coco could not be made."}))

        # Copies masks into "masks" sub-directory in export dir
        # Converts masks into desired file type
        try:
            # Changing file extensions if png_16, png_8, or COCO
            mask_file_type = (
                "png" if "png" in user_mask_file_type else user_mask_file_type
            )
            mask_file_name = f"label_masks_{segment_image_id}.{mask_file_type}"
            mask_path = merge_directory(FULL_EXPORT_MASKS_PATH, mask_file_name)
            export_mask_file_type(label_mask, mask_path, user_mask_file_type)
            export_paths["mask_path"] = merge_directory(
                TRAINING_FILE_NAME, f"masks/{mask_file_name}"
            )
        except Exception as error:
            print(error)
            traceback.print_tb(error.__traceback__)
            return make_response(("", 404, {"error": "Mask could not be converted."}))

    # If the selected mask type is coco: write master_dict as a json
    with open(
        f"{FULL_TRANING_DIR_PATH}/coco_{TRAINING_FILE_NAME}.json", "w"
    ) as json_obj:
        json.dump(master_dict, json_obj, indent=4)
        json_obj.close()

    # Attempts to create zip folder
    try:
        export_zip_file_path = shutil.make_archive(
            FULL_TRANING_DIR_PATH, "zip", FULL_TRANING_DIR_PATH
        )
    except Exception as error:
        print(error)
        traceback.print_tb(error.__traceback__)
        return make_response(("", 500, {"error": "Couldn't create zip folder"}))

    export_file_zip_name = TRAINING_FILE_NAME + ".zip"

    with open(export_zip_file_path, "rb") as file_data:
        file_buffer = io.BytesIO(file_data.read())
        file_data.close()
    file_buffer.seek(0)

    # Clear export directory
    shutil.rmtree(FULL_TRANING_DIR_PATH)

    response = send_file(
        file_buffer, download_name=export_file_zip_name, as_attachment=True
    )

    response = make_response(response)
    response.headers["file-name"] = export_file_zip_name
    # Clear zip
    os.remove(export_zip_file_path)

    return response
