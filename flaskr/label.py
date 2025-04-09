"""
label module for classx all endpoints related to labeling
"""

# Python Standard Library Imports
from datetime import datetime

import numpy as np

# Python Third Party Imports
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from classxlib.color import color_labeled_image
from classxlib.database.model import (
    User,
)

# Local Library Imports
from classxlib.file import merge_directory
from classxlib.image import image_as_b64, read_cv_image
from classxlib.label import get_unknown_label_from_research_field, remove_small_labels
from classxlib.segment import (
    get_labeled_segment_count,
    read_segment_image,
    update_segment_image_info,
)


from .database import get_db
from .globals import STATIC_FOLDER
from .oauth import get_oauth

LABEL = Blueprint("label", __name__, template_folder="/templates")


@LABEL.route("/label/", methods=["GET", "POST"], endpoint="label")
def load_label_tool():
    """API ENDPOINT
    Labels files accordingly

    Verifies the session is valid using the `validate_user_session`
    function from `oauth.keycloak` module.
    If the session is not valid and cant be refreshed, renders an error page.

    Session Args:
        uuid(str): User's uuid to verify the session token against database.

    Request Args:
        crop_image_id(int): The id of the cropped image.

    Returns:
        JSON:Formatted response dict object for front-end
            -status(int): HTTP Status code returns 404 if there are errors
            -error(str): Informational error message ONLY returned when status 400/404
                        is returned
            -render_template(template): A template created based on the label criteria
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    crop_image_service = db.crop_image_service
    segment_image_service = db.segment_image_service
    research_field_service = db.research_field_service
    training_file_service = db.training_file_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If we get false its not valid!
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
    if crop_image_obj is None:
        return redirect(url_for("error.error/404"))

    # Getting associated Research field  from the crop image object
    research_field_obj = research_field_service.get_by_id(crop_image_obj.research_id)

    if research_field_obj is None:
        return redirect(url_for("error.error/404"))

    # Getting all images associated with user.
    segment_image_obj_list = segment_image_service.get_user_images_from_parent(
        crop_image_id=crop_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # Default research field is Heliophysics in cases that no Research field  is found

    # TODO Change this to get default files and Research field specific files
    # Retrieving the label file objects associated with user
    training_file_obj_list = training_file_service.get_user_research_files(
        research_field_id=research_field_obj.id,
        user_id=user_obj.id,
        default_id=db.DEFAULT_ID,
    )

    # Getting all the ids of the uploaders
    uploader_ids = list(
        map(
            lambda segment_image_obj: segment_image_obj.shared_by,
            segment_image_obj_list,
        )
    )

    # Setting the names of the uploader based off the name
    uploader_names = list(
        map(
            lambda user_id: (
                user_service.get_by_id(user_id).name
                if user_id is not None
                else user_obj.username
            ),
            uploader_ids,
        )
    )

    # Formatting a list of the dates created
    date_created_list = list(
        map(
            lambda x: datetime.strptime(x.name[12:30], "%m_%d_%Y_%H_%M_%S").date(),
            segment_image_obj_list,
        )
    )

    # Rendering the label.html page with arguments
    return render_template(
        "label.html",
        user=user_obj,
        packed=zip(segment_image_obj_list, uploader_names, date_created_list),
        label_map=research_field_obj.label_map,
        training_files=training_file_obj_list,
        opacity=session["label_opacity"],
    )


@LABEL.route(
    "/updateLabelOpacity/", methods=["GET", "POST"], endpoint="updateLabelOpacity"
)
def update_label_opacity():
    """
    API ENDPOINT Updates the label opacity of the labeled segments in the image.

    Verifies the session is valid using the `validate_user_session`
    function from `oauth.keycloak` module.
    If the session is not valid and cant be refreshed, renders an error page.

    Session Args:
        uuid(str): User's uuid to verify the session token against database.

    Request Args:
        segment_image_id(int): The id of the segmented image.
        new_opacity(float): The opacity value of the segmented image

    Returns:
        JSON:Formatted response dict object for front-end
            -status(int): HTTP Status code returns 200 if successful
                          returns 404 if there are errors
            -error(str): Informational error message ONLY returned when status 404
                        is returned
            -image_string(String): Path to the image
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service
    research_field_service = db.research_field_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    print("Request to change opacity of boundaries")
    segment_image_id = request.args.get("segment_image_id", type=int)
    new_opacity = request.args.get("opacity_value", type=float)

    session["label_opacity"] = new_opacity

    # Retrieve segment image object from database
    segment_image_obj = segment_image_service.get_user_image(
        segment_image_id=segment_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # Getting research associated with the segment image object
    research_field_obj = research_field_service.get_by_id(segment_image_obj.research_id)

    # Verifying research field exsistence
    if research_field_obj is None:
        return {"status": 404, "error": "Research Field not found"}

    # Formatting path to segment image
    segment_image_path = merge_directory(STATIC_FOLDER, segment_image_obj.segment_path)

    # Reading segment image file
    segment_image, segment_info = read_segment_image(segment_image_path)

    research_field_label_map = {}
    for label in research_field_obj.label_map:
        research_field_label_map[label["id"]] = {
            "name": label["name"],
            "color": label["color"],
        }

    # Gettting the counts of labeled and unlabeled segments
    # pylint: disable=unused-variable
    total_segment_count, labeled_segment_count, unlabeled_segment_count = (
        get_labeled_segment_count(segment_info)
    )

    # Formatting path to marked image
    marked_image_path = merge_directory(
        STATIC_FOLDER, segment_image_obj.marked_image_path
    )
    # Reading marked image
    marked_image = read_cv_image(marked_image_path, noflag=True)

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
    # print('Color image is generated.')

    # Converting image to base 64 for front-end return
    base64_image = image_as_b64(color_image)

    return {"status": 200, "image_string": base64_image}


@LABEL.route("/getLabelImage/", methods=["GET", "POST"], endpoint="getLabelImage")
def get_label_image():
    """
     Retrieves segmented image data and associated information.

     Session Args:
         uuid(str): User's uuid to verify the session token against database.

     Request Args:
         segment_image_id(int): The id of the segmented image.

    Returns:
         JSON:Formatted response dict object for front-end
             -status(int): HTTP Status code returns 200 if successful
                           returns 404 if there are errors
             -error(str): Informational error message
             ONLY returned when status 404 is returned
             - image_string(str): Base64 encoded string of the colored image.
             - labeled_segments(int): Count of labeled segments.
             - total_segments(int): Total count of segments.
             - label_class_list(list): List of tuples
             containing label IDs and their respective counts.
             - label_map(dict): Mapping of label IDs to their names and colors.
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service
    research_field_service = db.research_field_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    segment_image_id = request.args.get("segment_image_id", type=int)

    # Retrieve segment image object from database
    segment_image_obj = segment_image_service.get_user_image(
        segment_image_id=segment_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # Getting research associated with the segment image object
    research_field_obj = research_field_service.get_by_id(segment_image_obj.research_id)

    # Verifying research field exsistence
    if research_field_obj is None:
        return {"status": 404, "error": "Research Field not found"}

    # Formatting path to segment image
    segment_image_path = merge_directory(STATIC_FOLDER, segment_image_obj.segment_path)

    # Reading segment image file
    segment_image, segment_info = read_segment_image(segment_image_path)

    research_label_map = {}
    for label in research_field_obj.label_map:
        research_label_map[label["id"]] = {
            "name": label["name"],
            "color": label["color"],
        }

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
    # print('Color image is generated.')

    # Converting image to base 64 for front-end return
    base64_image = image_as_b64(color_image)

    return {
        "status": 200,
        "image_string": base64_image,
        "labeled_segments": labeled_segment_count,
        "total_segments": total_segment_count,
        "label_class_list": np.column_stack(
            np.unique(segment_info[:, 1], return_counts=True)
        ).tolist(),
        "label_map": research_label_map,
    }


######################################################################
# endpoint called when segmented image is clicked in labeling process
######################################################################
# TODO: we need to update the charts here onclick so when user click a
# segment to relabel, chart would update, same to all 3 endpoints
@LABEL.route("/labelSegment/", methods=["GET", "POST"], endpoint="labelSegment")
def label_segment():
    """
    A function that uses the coordinates of a click to
    get the segment number

    Session Args:
        uuid(str): User's uuid to verify the session token against database.

    Request Args:
        segment_image_id(int): The id of the segmented image.
        label_id(int): The research id of the label
        click_location_x(float): The position along the x-axis that was clicked
        click_location_y(float): The position along the y-axis that was clicked

     Returns:
        JSON:Formatted response dict object for front-end
            -status(int): HTTP Status code returns 200 if successful
                          returns 404 if there are errors
            -error(str): Informational error message ONLY returned when status 404
                        is returned
            - image_string(str): Base64 encoded string of the colored image.
            - labeled_segments(int): Count of labeled segments.
            - total_segments(int): Total count of segments.
            - label_class_list(list): List of tuples containing label IDs
            and their respective counts.
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service
    research_field_service = db.research_field_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving segment image ID
    segment_image_id = request.args.get("segment_image_id", type=int)
    research_label_id = request.args.get("label_id", type=int)

    # Retrieve segment image object from database
    segment_image_obj = segment_image_service.get_user_image(
        segment_image_id=segment_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # Getting research associated with the segment image object
    research_field_obj = research_field_service.get_by_id(segment_image_obj.research_id)

    # Verifying research field exsistence
    if research_field_obj is None:
        return {"status": 404, "error": "Research Field not found"}

    # User click locations on x,y axis
    click_location_x = request.args.get("x", type=int)
    click_location_y = request.args.get("y", type=int)
    actual_size = request.args.get("actualSize", type=int)

    # Checking if both click location arguments were received
    if None in (click_location_x, click_location_y):
        return {"status": 400, "error": "no x or y in request arguments"}
    if actual_size is None:
        actual_size = 512
    # scaling factor it's 512 because that's the sizing used in front-end display
    adjusted_location_x = int(
        (segment_image_obj.crop_size / actual_size) * click_location_x
    )
    adjusted_location_y = int(
        (segment_image_obj.crop_size / actual_size) * click_location_y
    )

    # Formatting path to segment image
    segment_image_path = merge_directory(STATIC_FOLDER, segment_image_obj.segment_path)

    # Reading segment image file
    segment_image, segment_info = read_segment_image(segment_image_path)

    # Retrieving the clicked segment number
    selected_segment_id = int(segment_image[adjusted_location_y, adjusted_location_x])

    # print(f'clicked seg id {selected_segment_id}')

    # Updating the segment label map of the segment image object in database
    if research_label_id is not None and research_label_id != "None":
        # Updating segment label id on the segment info
        # The -1 is because the index starts from 0 in the array but segment numbers start from 1
        segment_info[selected_segment_id - 1][1] = research_label_id
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
    # print('Color image is generated.')

    # Converting image to base 64 for front-end return
    base64_image = image_as_b64(color_image)
    return {
        "status": 200,
        "image_string": base64_image,
        "labeled_segments": labeled_segment_count,
        "total_segments": total_segment_count,
        "label_class_list": np.column_stack(
            np.unique(segment_info[:, 1], return_counts=True)
        ).tolist(),
    }


######################################################################
# endpoint called when next segment button is clicked in labeling process
######################################################################
@LABEL.route("/labelNextSegment/", methods=["GET", "POST"], endpoint="labelNextSegment")
def label_next_segment():
    """
    A function that counts labeled and unlabeled
    segments. Afterwards, colors the segments and
    sends it front-end as base 64 image.

    Session Args:
        uuid(str): User's uuid to verify the session token against database.

    Request Args:
        segment_image_id(int): The id of the segmented image.
        label_id(int): The research id of the label

     Returns:
        JSON:Formatted response dict object for front-end
            -status(int): HTTP Status code returns 200 if successful
                          returns 404 if there are errors
            -error(str): Informational error message ONLY returned when status 404
                        is returned
            - image_string(str): Base64 encoded string of the colored image.
            - labeled_segments(int): Count of labeled segments.
            - total_segments(int): Total count of segments.
            - label_class_list(list): List of tuples containing label IDs
            and their respective counts.
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service
    research_field_service = db.research_field_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving segment image ID
    segment_image_id = request.args.get("segment_image_id", type=int)
    research_label_id = request.args.get("label_id", type=int)

    # Retrieve segment image object from database
    segment_image_obj = segment_image_service.get_user_image(
        segment_image_id=segment_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # Getting research associated with the segment image object
    research_field_obj = research_field_service.get_by_id(segment_image_obj.research_id)

    # Verifying research field exsistence
    if research_field_obj is None:
        return {"status": 404, "error": "Research Field not found"}

    # Formatting path to segment image
    segment_image_path = merge_directory(STATIC_FOLDER, segment_image_obj.segment_path)

    # Reading segment image file
    segment_image, segment_info = read_segment_image(segment_image_path)

    # Index list of all unlabeled segments
    unlabeled_segment_indices = np.argwhere(segment_info[:, 1] == 0)

    if len(unlabeled_segment_indices) != 0:
        # Getting the first unlabeled segment index
        unlabeled_segment_index = unlabeled_segment_indices[0][0]
        # Updating the segment label map of the segment image object in database
        if research_label_id is not None and research_label_id != "None":
            # Updating segment label id on the segment info
            segment_info[unlabeled_segment_index][1] = research_label_id
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
    # print('Color image is generated.')

    # Converting image to base 64 for front-end return
    base64_image = image_as_b64(color_image)

    return {
        "status": 200,
        "image_string": base64_image,
        "labeled_segments": labeled_segment_count,
        "total_segments": total_segment_count,
        "label_class_list": np.column_stack(
            np.unique(segment_info[:, 1], return_counts=True)
        ).tolist(),
    }


######################################################################
# endpoint to fill all unlabeled segments to unknown
######################################################################
@LABEL.route(
    "/setUnlabeledUnknown/", methods=["GET", "POST"], endpoint="setUnlabeledUnknown"
)
def set_unlabeled_unknown():
    """
    An endpoint called to label all unlabeled segments to unknown

     Session Args:
        uuid(str): User's uuid to verify the session token against database.

    Request Args:
        segment_image_id(int): The id of the segmented image.

    Returns:
        JSON:Formatted response dict object for front-end
            -status(int): HTTP Status code returns 200 if successful
                          returns 404 if there are errors
            -error(str): Informational error message ONLY returned when status 404
                        is returned
            - image_string(str): Base64 encoded string of the colored image.
            - labeled_segments(int): Count of labeled segments.
            - total_segments(int): Total count of segments.
            - label_class_list(list): List of tuples containing label IDs
            and their respective counts.
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service
    research_field_service = db.research_field_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving segment image ID
    segment_image_id = request.args.get("segment_image_id", type=int)

    # Flag to remove small labels before saving training file
    remove_small = request.args.get("remove_small_labels", type=bool)

    # The precentage that segments
    area_removal_percentage = request.args.get("area_removal_percentage", type=float)

    # Retrieve segment image object from database
    segment_image_obj = segment_image_service.get_user_image(
        segment_image_id=segment_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )

    # Getting research associated with the segment image object
    research_field_obj = research_field_service.get_by_id(segment_image_obj.research_id)

    # Verifying research field exsistence
    if research_field_obj is None:
        return {"status": 404, "error": "Research Field not found"}

    # Formatting path to segment image
    segment_image_path = merge_directory(STATIC_FOLDER, segment_image_obj.segment_path)

    # Reading segment image file
    segment_image, segment_info = read_segment_image(segment_image_path)

    # Retrieves the unknown label category id from the domain
    unknown_label_id = get_unknown_label_from_research_field(research_field_obj)

    # Splitting the segment info
    # pylint: disable=unbalanced-tuple-unpacking
    segment_numbers, segment_labels, segment_area_count = np.hsplit(segment_info, 3)

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

    # Updating all unlabeled segments to unknown
    segment_labels = np.where(segment_labels == 0, unknown_label_id, segment_labels)

    # Recombining the segment info
    segment_info = np.column_stack(
        (segment_numbers, segment_labels, segment_area_count)
    )

    # Updating segment info after changes
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
    # print('Color image is generated.')

    # Converting image to base 64 for front-end return
    base64_image = image_as_b64(color_image)

    return {
        "status": 200,
        "image_string": base64_image,
        "labeled_segments": labeled_segment_count,
        "total_segments": total_segment_count,
        "label_class_list": np.column_stack(
            np.unique(segment_info[:, 1], return_counts=True)
        ).tolist(),
    }


@LABEL.route("/getLabelArea/", methods=["GET", "POST"], endpoint="getLabelArea")
def get_label_area():
    """
    A function that gets the total area for each label

    Session Args:
        uuid(str): User's uuid to verify the session token against database.

    Request Args:
        segment_image_id(int): The id of the segmented image

    Returns:
        JSON:Formatted response dict object for front-end
            -status(int): HTTP Status code returns 200 if successful
                          returns 404 if there are errors
            -error(str): Informational error message ONLY returned when status 404
                        is returned
            -segment_area(dict): a dict of unique label ids

    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    segment_image_service = db.segment_image_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    # Retrieving segment image id from front-end
    segment_image_id = request.args.get("segment_image_id", type=int)

    # Retrieving associated segment image object from database
    segment_image_obj = segment_image_service.get_user_image(
        segment_image_id=segment_image_id, user_id=user_obj.id, default_id=db.DEFAULT_ID
    )
    # TODO we need to add validation for checking if it's under a shared file
    if segment_image_obj is None:
        segment_image_obj = segment_image_service.get_image(
            segment_image_id=segment_image_id
        )

    # Formatting path to segment image
    segment_image_path = merge_directory(STATIC_FOLDER, segment_image_obj.segment_path)

    # Reading segment image file
    segment_info = read_segment_image(segment_image_path)[1]

    # List of all the different labels
    unique_label_ids = np.unique(segment_info[:, 1])

    # Setting dict variable
    label_area_dict = {}

    for label_id in unique_label_ids.tolist():
        # Gets the total area sum for each label
        label_area_dict[label_id] = int(
            np.sum(np.where(segment_info[:, 1] == label_id, segment_info[:, 2], 0))
        )
    print(label_area_dict)
    return {"status": 200, "segment_area": label_area_dict}


@LABEL.route("/checkSegmentLabel/", methods=["GET"], endpoint="checkSegmentLabel")
def check_segment_label():
    """Check if all segments are labeled

    Returns:
        dict: front end response if we should display an error or not
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    segment_image_service = db.segment_image_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    # Retrieving segment image id from front-end
    segment_image_id = request.args.get("segment_image_id", type=int)

    # Retrieving associated segment image object from database
    segment_image_obj = segment_image_service.get_image(segment_image_id)

    # Formatting path to segment image
    segment_image_path = merge_directory(STATIC_FOLDER, segment_image_obj.segment_path)

    # Reading segment image file
    segment_info = read_segment_image(segment_image_path)[1]

    # Gettting the counts of labeled and unlabeled segments
    unlabeled_segment_count = get_labeled_segment_count(segment_info)[2]

    if unlabeled_segment_count != 0:
        print("NOT ALL SEGMENTS LABELED")
        return {
            "status": 400,
            "error": "Not all segments filled. Save incomplete \
            segments in 'Unknown' class by clicking OK.",
        }

    return {"status": 200}
