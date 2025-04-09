"""
this module contains the API endpoints for segmenting images
"""

# Python Standard Library Imports
import json
import traceback
from ctypes import c_uint32
from datetime import datetime, timezone
import ast
import requests

# Python Third Party Imports
from flask import Blueprint, jsonify, make_response, redirect, request, session, url_for

from classxlib.database import is_default_user
from classxlib.database.model import SegmentImage, User
import numpy as np

# Local Library Imports
from classxlib.file import format_database_path, merge_directory
from classxlib.image import image_as_b64, write_cv_image, read_cv_image
from classxlib.segment import (
    run_segmentation,
    write_segment_image,
)
from classxlib.segment.process import process_segment_parameters
from flaskr import crop_image, user

from .database import get_db
from .globals import ADMIN_UPLOAD_FOLDER, STATIC_FOLDER, USER_UPLOAD_FOLDER
from .oauth import get_oauth

SEGMENT_IMAGE = Blueprint("segment", __name__, template_folder="/templates")


@SEGMENT_IMAGE.route(
    "/previewSegmentImage/", methods=["GET", "POST"], endpoint="previewSegmentImage"
)
def preview_segment_image():
    """Takes a front-end request to segment a image. Processes parameters related to it

     Session Args:
        username(str): Username retrieved from the current session.

     Request Args:
        parameter_data(dict): The paramter of the data


    Returns:
        dict: Contains preview images and information for front-end processing.
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    crop_image_service = db.crop_image_service
    original_image_service = db.original_image_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    if request.method == "POST":
        # Processing the segment parameters from front-end
        print("request: ", request.get_json())
        parameter_data = process_segment_parameters(request.get_json())
        print("parameter_data:", parameter_data)
        # Setting the session image to empty
        session["image"] = {}

        # Retrieving the crop image object
        crop_image_obj = crop_image_service.get_user_image(
            crop_image_id=parameter_data["crop_image_id"],
            user_id=user_obj.id,
            default_id=db.DEFAULT_ID,
        )

        # Getting the associated original image object
        original_image_obj = original_image_service.get_user_image(
            original_image_id=crop_image_obj.original_image_id,
            user_id=user_obj.id,
            default_id=db.DEFAULT_ID,
        )
        print(f"Segmenting {crop_image_obj.name} for user {user_obj.username}")
        # If domain dataset supports light metadata collection check it
        try:
            parameter_data["light"] = "Invalid"
            if "light" in original_image_obj.metadata:
                parameter_data["light"] = original_image_obj.metadata["light"]
        except Exception:
            parameter_data["light"] = "Invalid"

        for name, value in parameter_data.items():
            if "check" in name:
                value = value == 1
            # print("Name:", name, "Value:", value)

        # Warnings for certain use of settings
        if (
            (parameter_data["light"] == "poor")
            and (parameter_data["light_adjustment_check"] == 0)
            and (parameter_data["confirm"] == 0)
        ):
            return {
                "status": 199,
                "error": "Notice: We have detected that the original image's this was \
                cropped from lighting is poor we recommend enabling \
                Light Adjustment, Continue Anyways?",
            }
        if (
            (parameter_data["color_cluster_check"] == 1)
            and (parameter_data["color_clusters"] == 1)
            and (parameter_data["confirm"])
        ):
            return {
                "status": 199,
                "error": "Notice: You've selected only 1 Color Cluster this will likely \
                result in 1 segment being generated, Continue Anyways?",
            }
        if (
            (parameter_data["segment_method_id"] == 2)
            and (parameter_data["region_merge_check"] == 0)
            and (parameter_data["confirm"] == 0)
        ):
            return {
                "status": 199,
                "error": "Notice: It's recommended to use region \
                    merging with SLIC Segmentation, Continue Anyways?",
            }
        if (
            (parameter_data["segment_method_id"] == 3)
            and (parameter_data["region_merge_check"] == 0)
            and (parameter_data["confirm"] == 0)
        ):
            return {
                "status": 199,
                "error": "Notice: It's recommended to use region merging \
                    with Quickshift Segmentation, Continue Anyways?",
            }
        if (
            (parameter_data["segment_method_id"] == 4)
            and (parameter_data["region_merge_check"] == 0)
            and (parameter_data["confirm"] == 0)
        ):
            return {
                "status": 199,
                "error": "Notice: It's recommended to use region merging \
                    with Felzenswab Segmentation, Continue Anyways? ",
            }

        # Sending request back to confirm settings were good and should continue the request
        if parameter_data["confirm"] == 0:
            return {"status": 100}

        # Return object list for front-end
        # Stores the base64 images to be used as previews
        return_object = []

        # Formatting the image paths to retrieve the crop image
        crop_image_path = merge_directory(
            STATIC_FOLDER, crop_image_obj.visualization_path
        )
        print(crop_image_obj)
        # Getting the hdf5 image if available
        if crop_image_obj.h5_path is not None:
            h5_crop_image_path = merge_directory(STATIC_FOLDER, crop_image_obj.h5_path)
        else:
            h5_crop_image_path = None

        print("H5 PATH", h5_crop_image_path)
        # Dict for the lighting adjustment algorithms
        histogram_method_name = {
            0: "Default",
            1: "Histogram Equalization",
            2: "Adaptive Equalization",
            3: "CLAHE",
        }

        # If lighting adjustment isn't checked then the other algorithms will never be used
        histogram_range = 1 if parameter_data["light_adjustment_check"] == 0 else 4
        parameter_data["model_id"] = session["research_field"]["id"]
        print(len(session["research_field"]["label_map"]))
        parameter_data["num_classes"] = len(session["research_field"]["label_map"])
        #try:
        print("Running Segmentation for", crop_image_obj.name)
        for histogram_method in range(histogram_range):
            parameter_data["histogram_method"] = histogram_method

            # Marking the boundaries of whole image
            marked_image, segment_image = run_segmentation(
                image_path=crop_image_path,
                h5_image_path=h5_crop_image_path,
                parameter_dict=parameter_data,
            )

            #response = requests.get("http://mask-rcnn-cpu:5002/process_image/", json=data)
            #marked_image = np.fromstring(ast.literal_eval(response["marked_image"])
                                         #,dtype=np.uint8).reshape(response['marked_image_shape'])
            #segment_image = np.fromstring(ast.literal_eval(response["segment_image"])
                                          #,dtype=np.uint32).reshape(response['segment_image_shape'])
            print(histogram_method_name[histogram_method])
            base64_image = image_as_b64(marked_image)
            session["image"][histogram_method] = {
                "marked_image": marked_image,
                "segment_image": segment_image,
                "status": 200,
            }
            return_object.append(
                {
                    "hist_method": histogram_method,
                    "image": base64_image,
                    "hist_name": histogram_method_name[histogram_method],
                }
            )
        return make_response(jsonify(return_object))
        # except Exception as error:
        #     traceback.print_tb(error.__traceback__)
        #     print("EXCEPTION AT previewSegmentation")
        #     return {'status' : 400,'error':"Segmentation Failed Cause: Unknown"}
    return {"status": 400, "error": "Segmentation Failed Cause: Unknown"}

@SEGMENT_IMAGE.route(
    "/process_model_image_test/", methods=["GET", "POST"], endpoint="process_model_image_test"
)
def process_model_image_test():
    """_summary_

    Returns:
        JSON: Formatted dict for the frontend
            - status(int): HTTP Status code returns 200 if successful
            - error(str): Informational error message ONLY returned when status 400/404
            - data(json): A formatted dict/json containing all relevant data
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service
    crop_image_service = db.crop_image_service

    #Verifying the session is valid
    valid_session = oauth.validate_user_session()

    #If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    request_data = request.get_json()
    crop_image_path = request_data["crop_image_path"]
    h5_crop_image_path = request_data["h5_image_path"]
    parameter_data = request_data["parameter_dict"]
    try:
        #Marking the boundaries of whole image
        marked_image, segment_image = run_segmentation(
            image_path=crop_image_path,
            h5_image_path=h5_crop_image_path,
            parameter_dict=parameter_data,
        )

        response_data = {
            "marked_image_shape" : marked_image.shape,
            "marked_image": str(marked_image.tostring()),
            "segment_image_shape": segment_image.shape,
            "segment_image": str(segment_image.tostring())
        }
        # res = requests.get("http://mask-rcnn-cpu:5002/process_image/", json=data)
        # print(res)
        # data = res.json()
        # #print(data['data'])
        # crop_image = np.fromstring(ast.literal_eval(data['data']['image']),dtype=np.uint8).reshape(data['data']['image_shape'])
        
        #print(crop_image)
        return jsonify(response_data)

    except Exception as error:
        print(error)
        traceback.print_tb(error.__traceback__)
        return make_response(("", 500, {"error": "Couldn't locate image"}))

@SEGMENT_IMAGE.route(
    "/saveSegmentImage/", methods=["GET", "POST"], endpoint="saveSegmentImage"
)
def save_segment_image():
    """API ENDPOINT
    save a segmented image to server, also saves a masked image to server

    Session Args:
        username(str): Username retrieved from the current session.
        segment_image(): The segment image from the session.
        marked_image(): The marked image from the session.

    Request Args:
        parameter_data(dict): A set of parameters needed for the given argument
    Returns:
        dict: Formatted return dict object for front-end, converted to json during during response
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    crop_image_service = db.crop_image_service
    segment_image_service = db.segment_image_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    if request.method == "POST":
        # Processing the segment parameters from front-end
        parameter_data = process_segment_parameters(request.get_json())

        # Setting correct file paths based off user
        if is_default_user(user_obj):
            segment_image_file_path = merge_directory(
                ADMIN_UPLOAD_FOLDER, user_obj.username + "/WriteGUI/SegmentImages"
            )
            marked_image_file_path = merge_directory(
                ADMIN_UPLOAD_FOLDER, user_obj.username + "/WriteGUI/MarkedImages"
            )
        else:
            segment_image_file_path = merge_directory(
                USER_UPLOAD_FOLDER, user_obj.username + "/WriteGUI/SegmentImages"
            )
            marked_image_file_path = merge_directory(
                USER_UPLOAD_FOLDER, user_obj.username + "/WriteGUI/MarkedImages"
            )

        # get cropped image object from database
        crop_image_obj = crop_image_service.get_user_image(
            crop_image_id=parameter_data["crop_image_id"],
            user_id=user_obj.id,
            default_id=db.DEFAULT_ID,
        )
        try:
            # Getting the current date time for file name
            date_utc = datetime.now(timezone.utc)
            date_time = date_utc.strftime("%m_%d_%Y_%H_%M_%S")

            # Retrieving the segment image and marked image from the session
            segment_image = session["image"][parameter_data["histogram_method"]][
                "segment_image"
            ]
            marked_image = session["image"][parameter_data["histogram_method"]][
                "marked_image"
            ]

            # Setting file name based off algorithm used
            if parameter_data["segment_method_id"] == 1:
                marked_image_filename = "watershedImage" + date_time + ".png"
            elif parameter_data["segment_method_id"] == 2:
                marked_image_filename = "slicImage" + date_time + ".png"
            elif parameter_data["segment_method_id"] == 3:
                marked_image_filename = "quickshiftImage" + date_time + ".png"
            elif parameter_data["segment_method_id"] == 4:
                marked_image_filename = "felzenswabImage" + date_time + ".png"
            elif parameter_data["segment_method_id"] == 5:
                marked_image_filename = "maskrcnnImage" + date_time + ".png"

            # Setting segment image file name
            segment_image_filename = "segmentImage" + date_time + ".h5"

            # Formatting the save paths and database paths
            segment_image_savepath = merge_directory(
                segment_image_file_path, segment_image_filename
            )

            # pylint: disable=possibly-used-before-assignment
            marked_image_savepath = merge_directory(
                marked_image_file_path, marked_image_filename
            )
            segment_image_database_path = format_database_path(segment_image_savepath)
            marked_image_database_path = format_database_path(marked_image_savepath)

            print(
                f"Creating object for segmented image \
                {segment_image_filename} at {segment_image_savepath} for user {user_obj.username}"
            )

            # Getting the total segments

            # Saving marked image and segment image to disk
            write_cv_image(marked_image, marked_image_savepath)

            # Writing the segment image data and segment info to disk
            write_segment_image(
                segment_image=segment_image,
                savepath=segment_image_savepath,
                datatype=c_uint32,
            )

            # Creating segment image object for database
            segment_image_obj = SegmentImage(
                name=segment_image_filename,
                user_id=user_obj.id,
                segment_path=segment_image_database_path,
                shared_by=None,
                shared_from=None,
                last_modified_date=date_utc,
                marked_image_path=marked_image_database_path,
                crop_image_id=crop_image_obj.id,
                research_id=crop_image_obj.research_id,
                segment_method=parameter_data["segment_method_id"],
                param1=parameter_data["parameter_1"],
                param2=parameter_data["parameter_2"],
                param3=parameter_data["parameter_3"],
                region_merge_method=parameter_data["region_merge_method"],
                region_merge_threshold=parameter_data["region_merge_threshold"],
                small_rem_method=parameter_data["small_item_removal_check"],
                small_rem_threshold=parameter_data["small_item_removal_threshold"],
                light_method=parameter_data["histogram_method"],
                contrast_method=parameter_data["contrast_stretch_check"],
                color_method=parameter_data["color_cluster_method"],
                color_clusters=parameter_data["color_clusters"],
                crop_size=crop_image_obj.crop_size,
            )

            # Saving segment image object to database
            segment_image_obj = segment_image_service.add_image(segment_image_obj)

            # print('inserted image to table..')
            # print(f'total segments in the image {total_segments}')

            # Clearing the session to reduce memory
            session["image"] = {}
            return {"status": 200, "image": segment_image_obj}

        except Exception as error:
            traceback.print_tb(error.__traceback__)
            print(error)
            print("EXCEPTION AT saveSegmentImage")
            return {"status": 400, "error": "Segmentation Saving Failed Cause: Unknown"}


@SEGMENT_IMAGE.route(
    "/getSegmentImages/", methods=["GET", "POST"], endpoint="getSegmentImages"
)
def get_segment_images():
    """API ENDPOINT
    Loads and returns a json of all images associated with the user

    Verifies the session is valid
    using the `validate_user_session` function from `oauth.keycloak` module.
    If the session is not valid and cant be refreshed, renders an error page.

    Session Args:
        uuid(str): User's uuid to verify the session token against database.

    Request Args:
        crop_image_id(int): The id of the cropped image.

    Returns:
        JSON:Formatted response dict object for front-end
            -status(int): HTTP Status code returns 200 if successful
                        returns 404/400 if there are errors
            -error(str): Informational error message ONLY returned when status 400/404
                        is returned
            -segment_image_obj_list(json): A formatted dict/json containing all relevant image to
                                           images owned by the user
    """
    print("===getSegmentImages===")
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving crop image id from front-end request
    crop_image_id = request.args.get("crop_image_id", type=int)
    print("crop_image_id:", crop_image_id)
    print("user_obj.id:", user_obj.id)
    print("db.DEFAULT_ID:", db.DEFAULT_ID)

    # Getting all images associated with user.
    segment_image_obj_list = segment_image_service.get_user_images_from_parent(
        crop_image_id=crop_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # print("segment_image_obj_list:",segment_image_obj_list)
    return make_response(jsonify(segment_image_obj_list))

@SEGMENT_IMAGE.route(
    "/process_model_image/", methods=["GET", "POST"], endpoint="process_model_image"
)
def process_model_image():
    """_summary_

    Returns:
        JSON: Formatted dict for the frontend
            - status(int): HTTP Status code returns 200 if successful
            - error(str): Informational error message ONLY returned when status 400/404
            - data(json): A formatted dict/json containing all relevant data
    """
    # Retrieving Database
    db = get_db()
    #oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service
    crop_image_service = db.crop_image_service

    # Verifying the session is valid
    #valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    # if not valid_session:
    #     session["url"] = "go-back"
    #     return redirect(url_for("auth.login"))
    
    try:
        print("TEST1")
        image_id = 82 #request.args.get("image_id", type=int)
        model_id = 5 #request.args.get("model_id", type=int)

        crop_image_obj = crop_image_service.get_image(image_id)
        #user_obj: User = user_service.get_by_uuid(session["uuid"])
        visualization_path = merge_directory(STATIC_FOLDER, crop_image_obj.visualization_path)
        crop_image = read_cv_image(visualization_path)
        crop_image_copy = np.copy(crop_image)
        data = {
            "image_id": image_id,
            "model_id": model_id,
            "filename": crop_image_obj.name,
            "user_id": 1,
            "image_shape": crop_image.shape,
            "image": str(crop_image.tostring()[:1000])
        }
        #res = requests.get("http://mask-rcnn-cpu:5002/process_image/", json=data)
        #print(res)
        #data = res.json()
        #print(data['data'])
       # crop_image = np.fromstring(ast.literal_eval(data['['image']),dtype=np.uint8).reshape(data['data']['image_shape'])
        
        #print(crop_image)
        return data

    except Exception as error:
        print(error)
        traceback.print_tb(error.__traceback__)
        return make_response(("", 500, {"error": "Couldn't locate image"}))