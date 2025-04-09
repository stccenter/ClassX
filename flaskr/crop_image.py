"""

crop image blue print has all api methods releating to cropping an image.

"""

# Python Standard Library Imports
import os
import traceback
from datetime import datetime, timezone

# Python Third Party Imports
from flask import (
    request,
    session,
    jsonify,
    make_response,
    Blueprint,
    render_template,
    url_for,
    redirect,
)

# Local Library Imports
from classxlib.file import merge_directory, format_database_path
from classxlib.image import (
    read_cv_image,
    read_hdf5_image,
    write_cv_image,
    write_hdf5_image,
)
from classxlib.image.process import create_crop
from classxlib.image.analysis import is_image_black
from classxlib.database import is_default_user
from classxlib.database.model import CropImage, User
from .oauth import get_oauth
from .database import get_db
from .globals import USER_UPLOAD_FOLDER, IMAGE_FOLDER, STATIC_FOLDER
from .celery import auto_crop_image


CROP_IMAGE = Blueprint("crop", __name__, template_folder="/templates")


@CROP_IMAGE.route("/saveCropImage/", methods=["GET", "POST"], endpoint="saveCropImage")
def save_crop_image():
    """API ENDPOINT
    Crops an original image and saves it to the database

    Request Args:
       username(str): Username retrieved from the current session
       POST DATA: request_dict(list(dict)): List of arguments in the form of a dict
       Example:
           [
               {'name': 'yNavName_{image_id}', 'value': '880'},
               {'name': 'xNavName_{image_id}', 'value': '740'},
               {'name': 'rangeZoomName_{image_id}', 'value': '256'},
               {'name': 'id', 'value': '{image_id}'},
               {'name': 'zoom', 'value': 256}
           ]

    output: {'status': 200, 'image_id'} if successful, image_id - inserted cropped image id
            {'status': 404, 'error': "user not found"} if error
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    original_image_service = db.original_image_service
    crop_image_service = db.crop_image_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # request_dict = {}
    try:
        # Getting the request data from front-end (UPDATE)
        request_dict = request.get_json()
        print("data:", request_dict)
        # Sorting the data into a dict
        # for i in range(0, len(data)):
        #     request_dict[data[i]['name']] = data[i]['value']

        # Retrieving the data from the dict
        original_image_id = request_dict["id"]
        click_location_x = int(request_dict["x"])
        click_location_y = int(request_dict["y"])
        crop_size = int(request_dict["zoom"])
    except Exception as error:
        # If any dict key doesn't work it means arguments aren't being received correctly
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return {"status": 404, "error": "Error 404: Bad Request"}

    # Load the original image associated with the id
    original_image_obj = original_image_service.get_user_image(
        original_image_id=original_image_id,
        user_id=user_obj.id,
        default_id=db.DEFAULT_ID,
    )

    # Verifying the user has access to the image.
    if original_image_obj is None:
        return {"status": 400, "error": "User does not have access to this image"}

    # Printing where the user clicked
    print(
        f"User clicked on {original_image_obj.name} at \
        {click_location_x} {click_location_y} span dimension {crop_size} {crop_size}"
    )

    # Setting the correct file paths for later
    if is_default_user(user_obj):
        crop_file_path = merge_directory(
            IMAGE_FOLDER, user_obj.username + "/WriteGUI/CropImages"
        )
    else:
        crop_file_path = merge_directory(
            USER_UPLOAD_FOLDER, user_obj.username + "/WriteGUI/CropImages"
        )

    try:
        # Getting current time to put as file name
        date_utc = datetime.now(timezone.utc)
        date_time = date_utc.strftime("%m_%d_%Y_%H_%M_%S")

        # Formatting the processed image path
        visual_original_image_path = merge_directory(
            STATIC_FOLDER, original_image_obj.visualization_path
        )

        # Reading processed image
        visual_image = read_cv_image(visual_original_image_path)

        # Checking if the original adjusted path is available
        if original_image_obj.h5_path is not None:
            h5_original_image_path = merge_directory(
                STATIC_FOLDER, original_image_obj.h5_path
            )
            # Verifying what format to read the image in.
            h5_original_image = read_hdf5_image(h5_original_image_path)
        else:
            h5_original_image = None

        # Image cropping based off the click location and crop_size
        crop_image, h5_crop_image = create_crop(
            visual_image=visual_image,
            h5_image=h5_original_image,
            crop_point_x=click_location_x,
            crop_point_y=click_location_y,
            crop_size=crop_size,
        )

        # Checking if the cropped image is over 20% black
        if is_image_black(crop_image, 0.80):
            return {"status": 400, "error": "Image is over 20 percent black"}

        # Checking if the original adjusted image is available for saving
        # Will not be if the path is None
        if h5_crop_image.any():
            # Formatting the save path
            h5_crop_file_name = "h5_" + date_time + ".h5"
            h5_crop_savepath = merge_directory(crop_file_path, h5_crop_file_name)
            h5_crop_db_savepath = format_database_path(h5_crop_savepath)
        else:
            h5_crop_db_savepath = None

        # Formatting the save path for the visualization image
        crop_file_name = "croppedImage_" + date_time + ".png"
        crop_savepath = merge_directory(crop_file_path, crop_file_name)
        crop_db_save_path = format_database_path(crop_savepath)

        # Creating the crop image object for the database
        # Mode is set to "man"(Manual) because the image is not from an auto crop
        crop_image_obj = CropImage(
            name=crop_file_name,
            user_id=user_obj.id,
            shared_by=None,
            shared_from=None,
            original_image_id=original_image_obj.id,
            research_id=original_image_obj.research_id,
            width=click_location_x + crop_size,
            height=click_location_y + crop_size,
            visualization_path=crop_db_save_path,
            h5_path=h5_crop_db_savepath,
            last_modified_date=date_utc,
            crop_size=crop_size,
            crop_type="man",
        )

        # Saving the images to disk
        print(f"Creating object for cropped image {crop_file_name} at {crop_savepath}")
        write_cv_image(crop_image, crop_savepath)

        # Checking if the original_cropped_image is available to save
        if h5_crop_image.any():
            write_hdf5_image(h5_crop_image, h5_crop_savepath)
        print("Saving cropped image")

        crop_image_obj = crop_image_service.add_image(crop_image_obj)

        # Returns status 200 and the image_id
        return {
            "status": 200,
            "crop_image": crop_image_obj,
            "original_image": original_image_obj,
        }

    except Exception as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return {"status": 400, "error": "Error 400: Image Cropping failed"}


@CROP_IMAGE.route(
    "/deleteCropImage", methods=["GET", "POST"], endpoint="deleteCropImage"
)
def delete_crop_image():
    """API ENDPOINT
        Deletes a crop image from a user account.
        Deletes all related segment images as well and also removes files.

    Session Args:
        username(str): Username retrieved from the current session.

    Request Args:
        crop_image_id(int): The id of the crop image to
        delete retrieved request.args.get('crop_image_id').

    Returns:
        dict: Formatted return dict object
        for front-end, converted to json during during return contents.
            status(int): HTTP Request status code.
            Returns 200 if successful or 400 if there is authorization issues and/or errors.
            message(str): Informational message for user.
            Only returned if status code is 200.
            error(str): Informational error message for user.
            Only returned if status code is a 400 series code.
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    crop_image_service = db.crop_image_service
    segment_image_service = db.segment_image_service
    label_image_service = db.label_image_service
    training_file_service = db.training_file_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving crop image id from front end
    crop_image_id = request.args.get("crop_image_id", type=int)

    # Getting the associated crop image id
    crop_image_obj = crop_image_service.get_user_image(
        crop_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # Verifying user has access to delete this image
    if crop_image_obj.user_id != user_obj.id and user_obj.user_level != 3:
        return {
            "status": 400,
            "error": "You do not have authorization to delete this image",
        }

    try:
        # If the image was shared just remove the shared row
        if crop_image_obj.shared_by is not None:
            # Deleting entry from database
            crop_image_service.remove_image(crop_image_obj)
            return {
                "status": 200,
                "message": "This image was shared so we have removed your access. \
                To regain access you will need to have the image reshared",
            }
        # If the image is owned by the user and not shared
        # Get all related segment images to crop image
        segment_image_obj_list = segment_image_service.get_images_from_parent_image(
            crop_image_obj.id
        )

        # Looping through each segment image
        for segment_image_obj in segment_image_obj_list:
            # Checking if there are any label_files the segment image is under
            label_image_obj_list = label_image_service.get_images_from_parent_image(
                segment_image_obj.id
            )

            # If the list is not empty that means it exists in a dataset
            if len(label_image_obj_list) != 0:
                message = ""

                # Compiling list of all related datasets
                for label_image_obj in label_image_obj_list:
                    training_file_obj = training_file_service.get_file(
                        label_image_obj.training_file_id
                    )
                    message = message + str(training_file_obj.file_name) + " "

                # Informing user which datasets to remove image from before continuing
                return {
                    "status": 400,
                    "error": "Please remove this image from the \
                    following training files before deleting: "
                    + message,
                }

            # Formatting the segment image paths
            segment_image_path = merge_directory(
                STATIC_FOLDER, segment_image_obj.segment_path
            )
            marked_image_path = merge_directory(
                STATIC_FOLDER, segment_image_obj.marked_image_path
            )

            # Removing them
            os.remove(segment_image_path)
            os.remove(marked_image_path)

            # Removing entry from database
            segment_image_service.remove_image(segment_image_obj)

        # Formatting crop image paths
        crop_image_path = merge_directory(
            STATIC_FOLDER, crop_image_obj.visualization_path
        )
        h5_crop_image_path = merge_directory(STATIC_FOLDER, crop_image_obj.h5_path)

        # Removing the images
        os.remove(crop_image_path)
        os.remove(h5_crop_image_path)

        # Deleting from database
        crop_image_service.remove_image(crop_image_obj)
    except Exception as error:
        traceback.print_tb(error.__traceback__)
        return {
            "status": 400,
            "error": "Error deleting image. Please try again. \
            If issue persists please consult an admin for help",
        }

    return {"status": 200, "message": "Crop Image Successfully Deleted"}


@CROP_IMAGE.route("/getUserCropImage/", methods=["GET"], endpoint="getUserCropImage")
def get_user_crop_image():
    """API ENDPOINT
    Retrieves a cropped image by its ID for the current user.

    Session Args:
        uuid(str): uuid of the currnet logged in user
        verifying session token against database.

    Request Args:
        crop_image_id(int): The id of the crop image to
        delete retrieved request.args.get('crop_image_id').

    Returns:
        dict object for the front-end
            -status(int):HTTP Status code returns 404/400
                        if there are errors
            -error(str):Informational error message ONLY
                        returned when status 400/404 is returned
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    crop_image_service = db.crop_image_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving crop image id from front end
    crop_image_id = request.args.get("crop_image_id", type=int)
    if crop_image_id is None:
        return {"status": 400, "error": "invalid image Id"}

    # Getting the associated crop image id
    crop_image_obj = crop_image_service.get_user_image(
        crop_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # Verifying the image was retrieved
    if crop_image_obj is None:
        return {"status": 404, "error": "image not found"}

    return make_response(jsonify(crop_image_obj))


@CROP_IMAGE.route(
    "/getUserCropImages", methods=["GET", "POST"], endpoint="getUserCropImages"
)
def get_user_crop_images():
    """API ENDPOINT
    Function to get all the cropped images associated with a User.
    By default will also get the default user crop images.

    Session Args:
        uuid(str): uuid of the current user taken from the session.

    Request Args:
        None

    GET Response:
        render_template(``segment.html``):
            Renders the segmentation page
        images(list(dict)):
            List of formatted dict objects for crop images and associated
            original image information associated with crop images
            only retrieves manual crop images
        user(User):
            Database user object
        mode(str):
            If the mode is auto or manual

    POST Response:
        images(original_image_service):
            List of original image objects that correspond to the user domain
        user(User):
            Database user object
        mode(str):
            If the mode is auto or manual
    """

    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    original_image_service = db.original_image_service
    crop_image_service = db.crop_image_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = request.path
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    if request.method == "GET":
        crop_image_obj_list = crop_image_service.get_user_research_images(
            research_field_id=session["research_field"]["id"],
            user_id=user_obj.id,
            crop_type="man",
        )
        original_image_obj_list = original_image_service.get_user_research_images(
            research_field_id=session["research_field"]["id"],
            user_id=user_obj.id,
            default_id=db.DEFAULT_ID,
        )
        return render_template(
            "segment.html",
            crop_images=crop_image_obj_list,
            original_image=original_image_obj_list,
        )
    if request.method == "POST":
        # POST is called whenever the automatic cropping button is called
        mode = "auto"
        original_image_obj_list = original_image_service.get_user_research_images(
            research_field_id=session["research_field"]["id"],
            user_id=user_obj.id,
            default_id=db.DEFAULT_ID,
        )

        return {"images": original_image_obj_list, "user": user_obj, "mode": mode}

    return {"status": 400, "error": "Invalid Request"}


@CROP_IMAGE.route(
    "/getAutoCropImage/", methods=["GET", "POST"], endpoint="getAutoCropImage"
)
def get_autocrop_image():
    """API ENDPOINT
    Returns an auto-cropped portion of an image based off of click location

    Verifies the session is valid using the
    `validate_user_session` function from `oauth.keycloak` module.
    If the session is not valid and cant be refreshed, renders an error page.

    Session Args:
        uuid(str): User's uuid if their session is vaild
    Request Args:
        original_image_id(int): The id of the original image.
        click_location_x(float): The position along the x-axis that was clicked
        click_location_y(float): The position along the y-axis that was clicked
        grid_length(float): Length of the original image
        grid_height(float): Height of the original image

    Returns:
        JSON:Formatted response dict object for front-end
            -status(int): HTTP Status code returns 200 if successful
                        returns 404/400 if there are errors
            -error(str): Informational error message ONLY returned when status 400/404
                        is returned
            -crop_image_obj(CroppedImage): Cropped image object retrieved from database
    """

    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    original_image_service = db.original_image_service
    crop_image_service = db.crop_image_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = request.path
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving the image id of the auto cropped image
    original_image_id = request.args.get("image_id", type=int)
    if original_image_id is None:
        return {"status": 400, "error": "invalid image Id"}

    # Getting the current domain from session
    research_field = session["research_field"]

    # Click Positions on gridded original image
    click_location_x = request.args.get("click_x", type=float)
    click_location_y = request.args.get("click_y", type=float)

    # Dimensions of Gridded Image
    # Note this may be different from the original
    # image dimensions depending on if part of the grid was cropped or padded to meet crop sizes
    grid_length = request.args.get("grid_length", type=float)
    grid_height = request.args.get("grid_height", type=float)

    # Checks to make sure click position is valid
    if click_location_x > grid_length or click_location_y > grid_height:
        return {"status": 400, "error": "Invalid click position"}

    # Dimensions are divided by 8 so we divide the auto crop size by 8.
    # Integer divide the click locations by the scaled auto crop size
    # The grid positions are their positions in terms of grid square counts
    grid_position_x = click_location_x // int((research_field["grid_size"] / 8))
    grid_position_y = click_location_y // int((research_field["grid_size"] / 8))

    # Find the grid position and adjust to be the crop width and height dimensions
    # The grid position is now the actual crop point from the image.
    # The crop point is the bottom right corner of a cropped image.
    # The auto grid size is added on at the end due to it being the bottom right corner.
    grid_position_x = (grid_position_x * research_field["grid_size"]) + research_field[
        "grid_size"
    ]
    grid_position_y = (grid_position_y * research_field["grid_size"]) + research_field[
        "grid_size"
    ]

    # Getting the database object for the cropped image
    # by matching the original image id and crop point.
    # This function only retrieves 'auto'(automatic)
    # cropped images to avoid crop point overlaps with 'man'(manual) cropped images

    crop_image_obj = crop_image_service.get_user_image_from_grid(
        original_image_id=original_image_id,
        grid_point=(grid_position_x, grid_position_y),
        user_id=user_obj.id,
        default_id=db.DEFAULT_ID,
    )

    # Verifying if the image was found.
    if crop_image_obj is None:
        print("Crop image not found")
        # Try statement since multiprocessing can have errors
        try:
            # Creates a process thread for the auto cropping
            # Redoes the auto cropping
            original_image_obj = original_image_service.get_image(original_image_id)
            # If it was shared from an image it needs to be cropped under the original image.
            if original_image_obj.shared_from is not None:
                original_image_obj = original_image_service.get_image(
                    original_image_obj.shared_from
                )

            auto_crop_image.delay(original_image_obj.id, research_field["grid_size"])

        except Exception as error:
            print("Auto Cropping TASK FAILED")
            traceback.print_tb(error.__traceback__)
        return {
            "status": 404,
            "error": "Image not found, verifying crop grid. Please try again in a few minutes.",
        }

    if crop_image_obj.user_id not in [user_obj.id, db.DEFAULT_ID]:
        print("User attempted access to unauthorized image")
        return {"status": 400, "error": "User does not have access to this image"}
    print(crop_image_obj)
    return {"status": 200, "image": crop_image_obj}
