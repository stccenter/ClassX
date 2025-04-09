"""
Module for the dashboard blueprint. This module contains the routes for the dashboard
basically the entire app
"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
from flask import Blueprint, render_template, request, session, redirect, url_for

# Local Library Imports
from classxlib.database import is_default_user
from classxlib.database.model import User
from .oauth import get_oauth
from .database import get_db


# Creating the blueprint route for Dashboard
DASHBOARD = Blueprint("dashboard", __name__)


@DASHBOARD.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    """API ENDPOINT
    Renders the dashboard home page and acts as a
    endpoint for searching/filtering original images.

    Args:
        username(str): Username retrieved from the current session.
        research_field_obj(ResearchField): Current ResearchField Object from
        session if none is available sets a default one from the user account.
        index_request(dict): Contains the search filters and query. only used for POST Request.

    Returns:
        return_object: List of images formatted
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    original_image_service = db.original_image_service
    research_field_service = db.research_field_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If we get false its not valid!
    if not valid_session:
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving the default id sets to none if it's already
    # default user to avoid duplicate return objects
    default_id = None if is_default_user(user_obj) else db.DEFAULT_ID

    # Retrieving the domain object from session
    current_research_field_id = request.args.get("research_field_id", 1, type=int)
    if current_research_field_id > 2:
        return {
            "success": False,
            "message": "Invalid Research Field",
        }

    research_field_obj = research_field_service.get_by_id(current_research_field_id)

    # Formatting the return dict for front end
    current_research_field = {
        "id": research_field_obj.id,
        "name": research_field_obj.name,
        "label_map": research_field_obj.label_map,
        "metadata_map": research_field_obj.metadata_map,
        "grid_size": research_field_obj.protocols["auto_grid_size"],
    }
    session["research_field"] = current_research_field

    # TODO We should have this appended in the front-end automatically
    # Appending the upload time and creation date to the metadata map
    # of the current domain since they are columns that don't exist in the normal map
    research_field_obj.metadata_map["upload_time"] = {
        "type": "date",
        "data": {"startdate": "-1", "enddate": "-1"},
    }
    research_field_obj.metadata_map["creation_date"] = {
        "type": "date",
        "data": {"startdate": "-1", "enddate": "-1"},
    }

    try:
        # Retrieving the Search Query and Image Filters if available
        # The JSON request only is available during POST Requests
        index_request = request.get_json() if request.method == "POST" else {}

        # Setting the search query and image filter arguments
        # The arguments are set to none or empty if they are not available
        search_query = index_request["query"] if "query" in index_request else ""
        image_filters = (
            index_request["image_filters"] if "image_filters" in index_request else None
        )

        print(research_field_obj.id)

        # Retrieving Images from Database with filters
        original_image_obj_list = original_image_service.search_images(
            query=search_query,
            user_id=user_obj.id,
            research_field_id=research_field_obj.id,
            search_filters=image_filters,
            default_id=default_id,
        )

        # Formatting images into dict list
        # This formatting is mainly for
        # setting the uploader names otherwise we could just return the object list
        return_object = [
            {
                "id": original_image_obj.id,
                "name": original_image_obj.name,
                "uploader_name": user_service.get_by_id(
                    original_image_obj.user_id
                ).username,
                "upload_time": original_image_obj.upload_time,
                "creation_date": original_image_obj.creation_date,
                "size": original_image_obj.size,
                "width": original_image_obj.width,
                "height": original_image_obj.height,
                "metadata": original_image_obj.metadata,
                "alias": original_image_obj.alias,
                "thumbnail_path": original_image_obj.thumbnail_path,
            }
            for original_image_obj in original_image_obj_list
        ]

        if request.method == "GET":
            # If the request type is GET then render the page freshly
            # TODO User list needs to be updated later on for image sharing purposes
            return return_object

        else:
            # If the request type is post then send the newly filtered image data.
            if len(original_image_obj_list) == 0:
                return render_template("error/400.html")
            else:
                return {
                    "status": 200,
                    "images": return_object,
                    "research_field": research_field_obj,
                }  # update
    except Exception as error:
        traceback.print_tb(error.__traceback__)
        return render_template("error/400.html")


@DASHBOARD.route("/dashboard/<int:original_image_id>", methods=["GET", "POST"])
def view_dashboard_image(original_image_id: int):
    """Get single image by image id for the dashboard focus view.

    Args:
        username(str): Username retrieved from the current session.
        original_image_id(int): The ID of the original image to load.

    Returns:
        status: Status code 200 if successful and target image,
        400 if an error occurs.
    """

    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    original_image_service = db.original_image_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    try:
        # ID of the original image to load
        original_image_id = int(original_image_id)
        print(original_image_id)
        # Retrieving the object from the database to verify the user has access to it.
        original_image_obj = original_image_service.get_user_image(
            original_image_id=original_image_id,
            user_id=user_obj.id,
            default_id=db.DEFAULT_ID,
        )
        # print("Original Image",original_image_obj)
        # If the image isn't found then the user doesn't have access to it.
        if original_image_obj is None:
            return render_template("404.html", status=400, error="Image not found")

        # Returns 200 to signify everything ran correctly
        return render_template(
            "dashboard/statistic.html",
            original_id=original_image_id,
            original_image=original_image_obj,
        )
    except Exception as error:
        print(error)
        traceback.print_tb(error.__traceback__)
        return render_template(
            "error/400.html",
            status=400,
            error="Failed to load dashboard if issue persists please contact IT support",
        )


@DASHBOARD.route(
    "/dashboard/<int:original_image_id>/segment/<int:crop_image_id>",
    methods=["GET", "POST"],
)
def dashboard_segment(original_image_id: int, crop_image_id: int):
    """Get single image by image id.

    Args:
        username(str): Username retrieved from the current session.
        original_image_id(int): The original image id used to locate which image to update.

    Returns:
        status: Status code 200 if successful and target image, 400 if an error occurs.
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    original_image_service = db.original_image_service
    crop_image_service = db.crop_image_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Id of the original image
    original_image_id = int(original_image_id)
    print("original_image_id", original_image_id)
    print("crop_image_id", crop_image_id)

    # Retrieving the object from the database to verify the user has access to it.
    original_image_obj = original_image_service.get_user_image(
        original_image_id=original_image_id,
        user_id=user_obj.id,
        default_id=db.DEFAULT_ID,
    )
    print("1")
    # If the image isn't found then the user doesn't have access to it.
    if original_image_obj is None:
        return render_template("error/404.html", status=404, error="Image not found")
    print("2")
    # Get crop image object from database
    crop_image_obj = crop_image_service.get_user_image(
        crop_image_id=crop_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )
    print("3")
    # Returns 200 to signify everything ran correctly
    return render_template(
        "dashboard/segment.html",
        original_id=original_image_id,
        crop_image_id=crop_image_id,
        original_image=original_image_obj,
        crop_image=crop_image_obj,
    )
    # return {"crop_image": crop_image_obj}


@DASHBOARD.route("/dashboard/crop", methods=["GET", "POST"])
def dashboard_crop():
    """API ENDPOINT
    Function to get all the cropped images associated with a User.
    By default will also get the default user crop images.

    Args:
        uuid(str): user's uuid retrieved from the current session.

    Returns:
        images: list of images for front-end
        user: Database user object
        mode: If the mode is auto or manual
    """

    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    original_image_service = db.original_image_service
    crop_image_service = db.crop_image_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    original_image_id = request.args.get("id", type=int)

    # Retrieving the object from the database to verify the user has access to it.
    original_image_obj = original_image_service.get_user_image(
        original_image_id=original_image_id,
        user_id=user_obj.id,
        default_id=db.DEFAULT_ID,
    )

    # If the image isn't found then the user doesn't have access to it.
    if original_image_obj is None:

        return render_template("error/404.html", status=404, error="Image not found")

    # Getting an adjustable max crop size.
    max_crop_size = min(
        original_image_obj.height - original_image_obj.height % 256,
        original_image_obj.width - original_image_obj.width % 256,
    )

    if request.method == "GET":
        print("get method")
        print("original_image_id: ", original_image_id)
        crop_image_obj_list = crop_image_service.get_user_images_from_parent(
            original_image_id=original_image_id,
            user_id=user_obj.id,
            default_id=db.DEFAULT_ID,
            crop_type="man",
        )

        # return render_template('dashboard/crop.html',
        #                        crop_images=crop_image_obj_list,
        #                        user=user_obj,
        #                        original_id=original_image_id,
        #                        original_image=original_image_obj,
        #                        max_crop_size=max_crop_size)
        return {"crop_image": crop_image_obj_list, "original_image": original_image_obj}


@DASHBOARD.route("/dashboard/label", methods=["GET", "POST"])
def dashboard_label():
    """Route for the dashboard label page.

    Returns:
        Dict: API Response
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    crop_image_service = db.crop_image_service
    research_field_service = db.research_field_service
    training_file_service = db.training_file_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving crop image id from front-end request
    crop_image_id = request.args.get("crop_image_id", type=int)

    # Retrieving crop image object from database
    crop_image_obj = crop_image_service.get_user_image(
        crop_image_id=crop_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # Getting associated domain from the crop image object
    research_field_obj = research_field_service.get_by_id(crop_image_obj.research_id)

    # Default domain is Heliophysics in cases that no domain is found
    if research_field_obj is None:
        return render_template(
            "error/404.html", status=404, error="Research field not found"
        )

    # TODO Change this to get default files and domain specific files
    # Retrieving the label file objects associated with user
    training_file_obj_list = training_file_service.get_user_research_files(
        research_field_id=research_field_obj.id,
        user_id=user_obj.id,
        default_id=db.DEFAULT_ID,
    )

    # Rendering
    return {
        "status": 200,
        "label_map": research_field_obj.label_map,
        "training_files": training_file_obj_list,
        "opacity": session["label_opacity"],
    }
