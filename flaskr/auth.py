"""The blueprint API route for all authorization endpoints"""

# Python Standard Library Imports
from urllib.parse import urlencode, quote_plus

# Python Third Party Imports
from flask import (
    request,
    session,
    redirect,
    url_for,
    Blueprint,
    current_app,
    render_template,
    make_response,
)

# Local Library Imports
from classxlib.database import is_default_user
from classxlib.file import create_user_directories
from .oauth import get_oauth
from .database import get_db
from .globals import IMAGE_FOLDER, USER_UPLOAD_FOLDER
from classxlib.database.model import User, UserResearchField

# Creating the blueprint for AUTH endpoints
AUTH = Blueprint("auth", __name__)


@AUTH.route("/login")
def login():
    """The main login endpoint for
    keycloak login services

    Returns:
        redirect: A keycloak authorized redirect to the
        callback.
    """

    # Retrieving OAuth App
    oauth = get_oauth()
    print(url_for("auth.callback", _external=True))

    next_url = request.args.get("next", "/dashboard")
    next_url = next_url if next_url.startswith("/") else "/" + next_url

    session["url"] = next_url

    return oauth.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True)
    )


@AUTH.route("/callback", methods=["GET", "POST"])
def callback():
    """Callback API for keycloak to authorize
    the access token and login information. Additionally
    sets up the user session.

    Returns:
        redirect: Redirects to logInUser to login in the
        user and set up the session before going to the
        dashboard
    """

    # Retrieving OAuth App
    oauth = get_oauth()

    # The retrieved authorization object token
    token_obj = oauth.authorize_access_token()

    # Setting the object in session for later retrieval
    session["user"] = token_obj

    # Redirects to kc_index
    # Retrieving Database
    db = get_db()

    # Setting up services
    user_service = db.user_service
    research_field_service = db.research_field_service
    user_level_service = db.user_level_service

    # Checking if the user is in the session
    if "user" in session:
        # Retrieving the authorization object token
        token_obj = session["user"]

        # Checking to see if the user is already in the ClassX Database
        user_obj = user_service.get_by_uuid(token_obj["userinfo"]["sub"])

        # If not set up the user and use their keycloak token as a primary key
        if user_obj is None:
            user_obj = user_service.get_by_username(
                token_obj["userinfo"]["preferred_username"]
            )
            if (
                user_obj is not None
                and token_obj["userinfo"]["sub"] != user_obj.kc_uuid
            ):
                user_obj = user_service.update_uuid(
                    user_id=user_obj.id, new_uuid=token_obj["userinfo"]["sub"]
                )
            else:
                if token_obj["userinfo"]["preferred_username"] == "default":
                    # Getting the default user object
                    default_user_obj = user_service.get_by_username("default")

                    # If the default user token is temp that means
                    # it was never updated and updating it now.
                    if default_user_obj.kc_uuid == "temp":
                        user_obj = user_service.update_uuid(
                            user_id=default_user_obj.id,
                            new_auth_token=token_obj["userinfo"]["sub"],
                        )
                else:
                    # Getting a list of all the default research field ids
                    research_field_id_list = [
                        research_field_obj.id
                        for research_field_obj in research_field_service.get_default_fields()
                    ]

                    # The newly created user object
                    new_user_obj = User(
                        username=token_obj["userinfo"]["preferred_username"],
                        kc_uuid=token_obj["userinfo"]["sub"],
                        user_level=user_level_service.get_by_name("Member").id,
                    )

                    # Adding new user to database
                    user_obj = user_service.add_user(new_user_obj)

                    # Bluk insert new user research objects (hopefully the only one).
                    user_research_objs = [
                        UserResearchField(user_obj.id, _id, 0)
                        for _id in research_field_id_list
                    ]
                    db.session.add_all(user_research_objs)
                    db.session.commit()
        user_research_fields_service = db.user_research_fields_service

        # Retrieving the user's associated research fields
        associated = user_research_fields_service.get_user_research_fields(user_obj.id)

        if associated is None:
            research_ids = research_field_service.get_default_fields()
            for field in research_ids:
                user_research_fields_service.add_research_field(user_obj.id, field.id)

            # Just get the first one from our list
            research_field_obj = research_field_service.get_by_id(research_ids[0].id)
        else:
            research_field_obj = research_field_service.get_by_id(
                associated[0].research_id
            )

        # Formatting the return dict for front end
        current_research_field = {
            "id": research_field_obj.id,
            "name": research_field_obj.name,
            "label_map": research_field_obj.label_map,
            "metadata_map": research_field_obj.metadata_map,
            "grid_size": research_field_obj.protocols["auto_grid_size"],
        }

        # Checking which environment mode were in.
        if current_app.config["FLASK_ENV"] == "production":
            session["username"] = user_obj.username
            session["user_level"] = user_obj.user_level
            session["uuid"] = user_obj.kc_uuid
            session["research_field"] = current_research_field
            session["image"] = {}
            session["label_opacity"] = 0.7
        elif current_app.config["FLASK_ENV"] == "development":
            session["username"] = user_obj.username
            session["user_level"] = user_obj.user_level
            session["uuid"] = user_obj.kc_uuid
            session["research_field"] = current_research_field
            session["image"] = {}
            session["label_opacity"] = 0.7

        # Verifying all User Directories on Login
        if is_default_user(user_obj):
            create_user_directories(IMAGE_FOLDER, user_obj.username)
        else:
            create_user_directories(USER_UPLOAD_FOLDER, user_obj.username)

        # Redirects to the dashboard
        route = session.pop("url", "/dashboard")

        next_url = current_app.config["FRONTEND_URL"] + route
        return redirect(next_url)

    # If the user isn't in session then redirects back to login.
    return redirect(url_for("auth.login"))


@AUTH.route("/logout")
def logout():
    """API for logging a user out of keycloak and the flask app

    Returns:
        redirect: Redirects to the homepage
    """
    print("hello")
    homepage_url = current_app.config["FRONTEND_URL"]
    print(homepage_url)
    if "user" in session:
        # ID token to pass to keycloak for authorizing the logout
        id_token = session["user"]["id_token"]

        # Clearing the user session
        session.clear()

        # Creating the logout url to ping keycloak's API
        logout_url = current_app.config["OAUTH2_REVOKE_URL"] + urlencode(
            {
                "id_token_hint": id_token,
                "post_logout_redirect_uri": homepage_url,
                "client_id": current_app.config["OAUTH2_CLIENT_ID"],
            },
            quote_via=quote_plus,
        )

        # Redirecting to the keycloak API endpoint
        print("yes 1")
        #return redirect(logout_url)
        
        return redirect(logout_url)

    # Clearing the session even if user isn't found
    session.clear()

    # Redirecting to homepage
    print("yes 2")
    return redirect(homepage_url)


@AUTH.route("/loggedOut", endpoint="loggedOut")
def logged_out():
    """Redirect API for keycloak after logging out
    a user. It just redirects to the homepage.

    Returns:
        redirect: Redirects to the homepage.
    """
    return redirect(url_for("public.homepage"))


@AUTH.route("/redirectPrevious", endpoint="redirectPrevious")
def redirect_previous():
    """Redirect API for keycloak reverifying session for
    a user. It just redirects to the previous page.

    Returns:
        redirect: Redirects to the last page.
    """
    print("redirect called")
    return make_response(render_template("redirect.html"), 200)
