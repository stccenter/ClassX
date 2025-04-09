"""
This module contains the endpoints for the original image API.
"""

# Python Standard Library Imports
import traceback
from datetime import datetime, timezone

# Python Third Party Imports
from flask import (
    redirect,
    render_template,
    request,
    session,
    jsonify,
    make_response,
    Blueprint,
    url_for,
)
from werkzeug.utils import secure_filename

# Local Library Imports
from classxlib.file import merge_directory, validate_upload_files
from classxlib.database import is_default_user
from classxlib.database.model import User
from .oauth import get_oauth
from .database import get_db
from .globals import ADMIN_UPLOAD_FOLDER, USER_UPLOAD_FOLDER

from .celery import upload_original_image


ORIGINAL_IMAGE = Blueprint("original", __name__, template_folder="/templates")


@ORIGINAL_IMAGE.route(
    "/changeImageAlias", methods=["GET", "POST"], endpoint="changeImageAlias"
)
def change_image_alias():
    """Changes the alias of an original image to a new alias set by the user.

    Args:
        original_image_id(int): The original image id used to locate which image to update.
        new_alias(str): The new alias to set received from form data.

    Returns:
        status: Status code 200 if successful, 400 if an error occurs.
    """

    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    original_image_service = db.original_image_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If we get false its not valid!
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    try:
        # New Alias to set on image
        new_alias = request.form.get("alias", type=str)

        # Id of the original image to change alias
        original_image_id = request.form.get("original_id", type=int)

        # Retrieving the object from the database to verify the user has access to it.
        original_image_obj = original_image_service.get_user_image(
            original_image_id=original_image_id, user_id=user_obj.id
        )

        # If the image isn't found then the user doesn't have access to it.
        if original_image_obj is None:
            return {"status": 400, "error": "User does not have access to this image"}

        # Update the image alias after completion
        original_image_obj = original_image_service.update_alias(
            original_image_id=original_image_obj.id, new_alias=new_alias
        )

        # Returns 200 to signify everything ran correctly
        return {"status": 200, "original_image": original_image_obj}
    except Exception as error:
        traceback.print_tb(error.__traceback__)
        return {"status": 400}


@ORIGINAL_IMAGE.route(
    "/uploadOriginalImages/", methods=["POST"], endpoint="uploadOriginalImages"
)
def upload_original_images():
    """API ENDPOINT
    Processes uploaded files into the ClassX Database.
    Validates file formats and naming structure. Only allows 5 files at a time.
    Files are processed and validated based off their research field. In the celery worker

    Args:
        username(str): Username retrieved from the current session.
        file_upload_list(list(file)): List of file objects received from front-end.
        research_field_obj(ResearchField):The research field object currently stored in the session.

    Returns:
        status: 200 if successful 400 if an error occurs.
        message: Info message for front-end to display
        listobj: List of successfully processed images
        username: username of the uploader
        invalid_files: String list of invalid files uploaded
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()
    print("dasdsad")

    # Setting up services
    user_service = db.user_service
    original_image_service = db.original_image_service
    research_field_service = db.research_field_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If we get false its not valid!
    if not valid_session:
        print("session invalid")
        return {"success": False, "message": "Session is invalid"}, 404

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieves the uploaded files from front end
    file_upload_list = [request.files["file"]]

    # Getting the session domain
    research_field = session["research_field"]
    research_field_obj = research_field_service.get_by_id(
        (request.headers.get("domainid") or 1)
    )

    # Will return an error if more than 5 files uploaded at a time.
    if len(file_upload_list) > 5:
        print("Error: Only 5 files can be uploaded at a time!")
        return {"status": 400, "message": "Only 5 files can be uploaded!"}
    # prints the number of files being uploaded to console
    print(len(file_upload_list), "Files being uploaded!")

    # The upload time of the file
    upload_time = datetime.now(timezone.utc)

    # Checks whether user is default/admin or a normal user
    # Sets the save file path to the correct directory depending on user
    if is_default_user(user_obj):
        original_savepath = merge_directory(
            ADMIN_UPLOAD_FOLDER, user_obj.username + "/ReadGUI"
        )
        processed_savepath = merge_directory(
            ADMIN_UPLOAD_FOLDER, user_obj.username + "/ProcessedImages"
        )
    else:
        original_savepath = merge_directory(
            USER_UPLOAD_FOLDER, user_obj.username + "/ReadGUI"
        )
        processed_savepath = merge_directory(
            USER_UPLOAD_FOLDER, user_obj.username + "/ProcessedImages"
        )

    print("Validating Files")
    # A function that validates the files and makes sure there are no duplicates.
    file_list = validate_upload_files(
        file_upload_list,
        user_obj.id,
        research_field_obj.protocols,
        original_image_service,
    )
    print(file_list)

    if len(file_list["validated"]) == 0:
        message = "All files are invalid or duplicates"
        if len(file_list["invalid"]) > 0:
            message = message + "<b> Invalid Files:" + ",".join(file_list["invalid"])

        if len(file_list["duplicate"]) > 0:
            message = (
                message + "<b> Duplicate Files:" + ",".join(file_list["duplicate"])
            )

        return {
            "status": 400,
            "message": message,
            "valid": [],
            "invalid": file_list["invalid"],
            "duplicate": file_list["duplicate"],
        }

    file_paths = []
    # Looping through each file
    for original_image_file in file_list["validated"]:

        # Retrieves the name of the file
        print("asdsadad")
        print(original_image_file)
        file_name = secure_filename(original_image_file.filename)
        print("Saving File:", file_name)

        # File path for the original image
        original_image_filepath = merge_directory(original_savepath, file_name)

        # Saving the Original Image File to Folder
        original_image_file.save(original_image_filepath)

        # Add to files paths that will be sent to celery worker
        file_paths.append(original_image_filepath)

    print(file_paths)
    # The task takes time depending how many
    # are in the queue so we sent the upload time that we set earlier

    if len(file_paths) > 0:
        res = upload_original_image.delay(
            user_obj.id,
            file_paths,
            processed_savepath,
            research_field_obj.id,
            upload_time.timestamp(),
        )

        pending_alerts = session.get("pending_alerts", [])
        pending_alerts.append(res.id)  # Add the task id to the pending alerts
        session["pending_alerts"] = pending_alerts

    # Formatting return message for front-end
    if len(file_list["validated"]) == len(file_upload_list):
        message = "All files successfully uploaded they are being proccessed"
    else:
        message = f"{len(file_list['validated'])} Files Successfully \
        Uploaded {len(file_upload_list)-len(file_list['validated'])} \
        Files Invalid or Duplicate. Others are being processed."

    if len(file_list["invalid"]) > 0:
        message = message + "<b> Invalid Files:" + ",".join(file_list["invalid"])

    if len(file_list["duplicate"]) > 0:
        message = message + "\n Duplicate Files:" + ",".join(file_list["duplicate"])

    valid = [file.filename for file in file_list["validated"]]

    return {
        "status": 200,
        "message": message,
        "invalid": file_list["invalid"],
        "duplicate": file_list["duplicate"],
        "valid": valid,
    }


@ORIGINAL_IMAGE.route("/crop/", methods=["GET", "POST"], endpoint="crop")
def crop_original_image():
    """API ENDPOINT
    Function called to load the crop.html page.
    Retrieves an original image from database then sends the object to front-end.

    Args:
        username(str): Username retrieved from the current session.
        original_image_id (int): The id of the original image to crop.

    Returns:
        render_template: crop.html
        image: the original image database object
        user: user database object.
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    original_image_service = db.original_image_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving the image id argument from request
    original_image_id = request.args.get("original_image_id", type=int)

    # Verifying data was retrieved correctly
    if original_image_id is None:
        return {"status": 404, "message": "Invalid image id"}

    # Load the associated image
    original_image_obj = original_image_service.get_user_image(
        original_image_id=original_image_id,
        user_id=user_obj.id,
        default_id=db.DEFAULT_ID,
    )

    # Getting an adjustable max crop size.
    max_crop_size = min(
        original_image_obj.height - original_image_obj.height % 256,
        original_image_obj.width - original_image_obj.width % 256,
    )

    # Verifying the image was found.
    if original_image_obj is None:
        return {"status": 404, "error": "image not found or user does not have access"}

    # Renders the crop.html page
    return render_template(
        "crop.html",
        original_image=original_image_obj,
        user=user_obj,
        max_crop_size=max_crop_size,
    )


@ORIGINAL_IMAGE.route(
    "/getOriginalImageById/", methods=["GET", "POST"], endpoint="getOriginalImageById"
)
def get_original_image_by_id():
    """API ENDPOINT
    Get a specific original image from a

    input: request.arg "name"  - username
            request.arg "image_id"
    output: {'status':200, 'image' : image} image is the image object if successful
              {'status': 404, 'error': "user not found"} if error
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    original_image_service = db.original_image_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    if request.method == "GET":

        # Retrieving the image id argument from request
        original_image_id = request.args.get("original_image_id", type=int)

        # Verifying Arguments
        if original_image_id is None:
            return {"status": 400, "error": "invalid image Id"}

        # load user's original images
        original_image_obj = original_image_service.get_user_image(
            original_image_id=original_image_id,
            user_id=user_obj.id,
            default_id=db.DEFAULT_ID,
        )
        if original_image_obj is None:
            original_image_obj = original_image_service.get_image(
                original_image_id=original_image_id
            )

        # Verifying original image
        if original_image_obj is None:
            return {"status": 404, "error": "image not found"}

        # Verifying the user has access to the image.
        # if original_image_obj.user_id != user_obj.id
        # and original_image_obj.user_id != db.DEFAULT_ID:
        # return {'status': 400, 'error': "User does not have access to this image"}

        return make_response(jsonify(original_image_obj))

    return {"status": 400, "error": "Invalid Request"}
