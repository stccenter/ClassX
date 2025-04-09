"""
This module contains the API endpoints for the research field objects.
"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
from flask import Blueprint, redirect, request, session, url_for

# Local Library Imports
from classxlib.database.model import ResearchField, User
from .oauth import get_oauth
from .database import get_db

RESEARCH_FIELD = Blueprint("research", __name__, template_folder="/templates")


@RESEARCH_FIELD.route(
    "/getDefaultResearchFields",
    methods=["POST", "GET"],
    endpoint="getDefaultResearchFields",
)
def get_default_research_fields():
    """API ENDPOINT
    Retrieves the default research field objects from the database for front-end

    Returns:
        status: Status code 200 if successful, 400 if an error occurs.
        research_fields: formatted dict list of research field information.
        Will be empty in case of error
    """
    # Retrieving Database
    db = get_db()
    
    # Setting up services
    research_field_service = db.research_field_service
    try:
        # TODO: Only give the data the front end actually uses...
        # Formats the research field list for return to front-end
        research_field_list = [
            {
                "id": research_field.id,
                "name": research_field.name,
                "label_map": research_field.label_map,
                "metadata_map": research_field.metadata_map,
                "grid_size": research_field.protocols["auto_grid_size"],
            }
            for research_field in research_field_service.get_default_fields()
        ]

        return {"status": 200, "research_fields": research_field_list}
    except Exception:
        return {"status": 400, "research_fields": {}}


@RESEARCH_FIELD.route(
    "/switchResearchField", methods=["POST", "GET"], endpoint="switchResearchField"
)
def switch_research_field():
    """API ENDPOINT
    Called to switch the current session research field to a new one.
    Verifes if research_field is associated with the user account before switch.

    Args:
        username(str): Username retrieved from the current session.
        new_research_id(int): The id of the new research field to set.


    Returns:
        status: Status code 200 if successful, 400 if an error occurs.
        current_research_field: formatted dict of the newly set research field.
    """

    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    research_field_service = db.research_field_service
    user_research_fields_service = db.user_research_fields_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If we get false its not valid!
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    try:
        # The new research field id to set.
        new_research_id = int(request.args.get("research_field_id"))

        # Verifying user has access to the research field
        # This is to prevent access to unauthorized research fields by manipulating the API Calls
        if not user_research_fields_service.in_research_id(
            user_obj.id, new_research_id
        ):
            return {
                "status": 400,
                "current_research_field": {},
                "error": "User does not have access to this research field",
            }

        # Setting the session research field to the new research field.
        new_research_field_obj = research_field_service.get_by_id(new_research_id)

        # Appending the upload time and creation date
        # to the metadata map of the current research field
        # since they are columns that don't exist in the normal map
        new_research_field_obj.metadata_map["upload_time"] = {
            "type": "date",
            "data": {"startdate": "-1", "enddate": "-1"},
        }
        new_research_field_obj.metadata_map["creation_date"] = {
            "type": "date",
            "data": {"startdate": "-1", "enddate": "-1"},
        }

        # Formatting the return dict for front end
        current_research_field = {
            "id": new_research_field_obj.id,
            "name": new_research_field_obj.name,
            "label_map": new_research_field_obj.label_map,
            "metadata_map": new_research_field_obj.metadata_map,
            "grid_size": new_research_field_obj.protocols["auto_grid_size"],
        }

        # Setting the session research field to the newly selected research field
        session["research_field"] = current_research_field

        return {"status": 200, "current_research_field": current_research_field}
    except Exception as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return {"status": 400, "current_research_field": {}}


@RESEARCH_FIELD.route(
    "/getUserResearchFields", methods=["POST", "GET"], endpoint="getUserResearchFields"
)
def get_user_research_fields():
    """API ENDPOINT
    Gets all associated research fields from a given user. Checks to see if any research fields
    are set inside current session if not then sets it to first research field.
    This function is called whenever a new page is loaded or the research field is changed.

    Request Args:
        username(str): Username retrieved from the current session.

    Returns:
        status: Status code 200 if successful, 400 if an error occurs.
        current_research_field: formatted dict of the current research field in use.
        research fields: full formatted dict list of user research fields.
    """

    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service
    research_field_service = db.research_field_service
    user_research_fields_service = db.user_research_fields_service

    # Verifying the session is valid
    valid_session = oauth.validate_user_session()

    # If we get false its not valid!
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj: User = user_service.get_by_uuid(session["uuid"])

    try:
        research_id_list = [
            field.research_id
            for field in user_research_fields_service.get_user_research_fields(
                user_obj.id
            )
        ]

        # User's associated research field list from the
        # research field ids stored on the account.
        research_field_obj_list = research_field_service.get_by_ids(research_id_list)

        # User ResearchField List
        research_field_list = [
            {
                "id": research_field.id,
                "name": research_field.name,
                "label_map": research_field.label_map,
                "metadata_map": research_field.metadata_map,
                "grid_size": research_field.protocols["auto_grid_size"],
            }
            for research_field in research_field_obj_list
        ]

        # Checking if the session research field is already set or not.
        if session["research_field"] is not None:
            current_research_field = session["research_field"]
        else:
            # Setting current research field to first entry in list.
            current_research_field: ResearchField = research_field_list[0]

            # Retrieves that database object and sets the session research field to that.
            session["research_field"] = current_research_field

        # Returning to front end
        return {
            "status": 200,
            "current_research_field": current_research_field,
            "research_fields": research_field_list,
        }

    except Exception as error:
        # Incase of error returns an empty list.
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return {"status": 400, "research_fields": {}}
