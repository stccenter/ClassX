"""
This file contains the user blueprint for the flask application. This blueprint is user management
"""

# Python Third Party Imports

from celery.result import AsyncResult

from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    render_template,
    request,
    send_from_directory,
    Response,
)

# Local Library Imports
from classxlib.database.model import UserFriend
from flaskr import celery
from .oauth import get_oauth
from .database import get_db

USER = Blueprint("user", __name__, template_folder="/templates")


@USER.route("/settings/profile", methods=["GET", "POST"], endpoint="settings/profile")
def user_profile():
    """User setting profile/update end points

    Request Args:
        uuid(str): The user's uuid to check if it if their session is valid

    Returns:
        render_template: user profile page
    """
    oauth = get_oauth()
    valid_session = oauth.validate_user_session()

    if not valid_session:
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        user = oauth.get_user_id_by_uuid(session["uuid"])
        username = user["username"]
        first_name = user["firstName"]
        last_name = user["lastName"]
        email = user["email"]
        organization = user["attributes"]["organization"][0]
        title = user["attributes"]["title"][0]

        return render_template(
            "user/profile.html",
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            organization=organization,
            title=title,
        )
    if request.method == "POST":
        current_user = oauth.get_user_id_by_uuid(session["uuid"])

        first_name = request.form.get("first-name", type=str)
        last_name = request.form.get("last-name", type=str)
        email = request.form.get("email", type=str)
        organization = request.form.get("organization", type=str)
        title = request.form.get("title", type=str)

        # check if any of the fields are empty? TODO: are any allowed to be empty?
        print(first_name, last_name, email, organization, title)
        if any([not first_name, not last_name, not email, not organization, not title]):
            return redirect(url_for("user.settings/profile"))

        atterbuttes = {"organization": organization, "title": title}
        new_user = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "attributes": atterbuttes,
        }

        oauth.update_user(current_user["id"], new_user)
        return redirect(url_for("user.settings/profile"))

    return redirect(url_for("user.settings/profile"))


@USER.route("/settings/friends", methods=["GET"], endpoint="settings/")
def user_friends():
    """renders the user friends page or redirects to reauth

    Returns:
        render_template: friend list page
    """
    oauth = get_oauth()
    valid_session = oauth.validate_user_session()

    if not valid_session:
        return redirect(url_for("auth.login"))

    return render_template("user/friends.html")


@USER.route("/friends", methods=["GET", "DELETE", "POST", "PATCH"], endpoint="friends")
def friends():
    """API ENDPOINT for friend management

    Request Args:
        uuid(str): The user's uuid to check if it if their session is valid
        other_uuid(str): The other user's uuid for the friend request (all but get)

    Methods:
        GET: get the friends list
        DELETE: remove a friend request
        POST: send a friend request
        PATCH: accept a friend request

    Returns:
        dict: depends on the method
    """
    oauth = get_oauth()
    valid_session = oauth.validate_user_session()

    if not valid_session:
        return redirect(url_for("auth.login"))
    db = get_db()

    user_obj = db.user_service.get_by_uuid(session["uuid"])
    user_id = user_obj.id

    if request.method == "GET":
        # get friends list and pending requests
        current_friends = db.user_friend_service.get_friends(user_id)
        pending = db.user_friend_service.get_pending(user_id)
        ret = []

        for friend in pending + current_friends:
            status, sender, reciver = friend[0].status, friend[1], friend[2]
            sent = sender.id == user_id

            print(status, sender, reciver)
            if status == 0:  # pending friend request logic
                ret.append(
                    {
                        "pending": True,
                        "sent": sent,
                        "username": reciver.username if sent else sender.username,
                        "uuid": reciver.kc_uuid if sent else sender.kc_uuid,
                    }
                )

            elif status == 1:  # accepted friend request logic
                ret.append(
                    {
                        "pending": False,
                        "username": reciver.username if sent else sender.username,
                        "uuid": reciver.kc_uuid if sent else sender.kc_uuid,
                    }
                )
                continue

        return ret
    if request.method == "DELETE":
        uuid = request.args.get("uuid", None)
        if not uuid:
            return {"status": 400}

        other_user = db.user_service.get_by_uuid(uuid)

        if not other_user:
            return {"status": 400}

        success = db.user_friend_service.remove_request(user_id, other_user.id)
        if not success:
            return {"status": 400}

    elif request.method == "POST":
        data = request.args.get("username", type=str)
        if not data:
            return {"status": 400, "notes": "no data"}

        username = data
        if not username:
            return {"status": 400, "notes": "no username"}
        elif username == user_obj.username or username == user_obj.kc_uuid:
            return {"status": 400, "notes": "username is yourself"}

        # they can get via username or uuid
        other_user = db.user_service.get_by_username(username)
        if not other_user:
            other_user = db.user_service.get_by_uuid(username)
            if not other_user:
                return {"status": 400, "notes": "user not exist"}

        # check if there is already an out going friend request
        current_request = db.user_friend_service.get_status(user_id, other_user.id)
        if current_request:
            if current_request.status == 0:
                if current_request.receiver_id == user_id:
                    db.user_friend_service.accept_friend_request(other_user.id, user_id)
                    return {"status": 200, "message": "User had a pending request from"}

                return {"status": 400, "error": "request already sent"}
            if current_request.status == 1:
                return {"status": 400, "error": "already friends"}
            # Going here shouldnt happen since blocking doesnt exist yet

        friend_request = UserFriend(user_id, other_user.id, 0)

        db.user_friend_service.create_friend_request(friend_request)

        return {"status": 200, "message": "Friend request sent"}

    if request.method == "PATCH":
        # accept the friend request
        data = request.get_json(cache=False, force=True, silent=True)
        if not data:
            return {"status": 400}

        uuid = data.get("uuid", None)
        if not uuid or uuid == user_obj.kc_uuid:
            return {"status": 400}

        other_user = db.user_service.get_by_uuid(uuid)

        if not other_user:
            return {"status": 400}

        current = db.user_friend_service.get_status(other_user.id, user_id)
        if not current:
            return {"status": 400}

        if current.status != 0:
            return {"status": 400}

        if current.sender_id != other_user.id:
            return {"status": 400}

        success = db.user_friend_service.accept_friend_request(other_user.id, user_id)
        if not success:
            return {"status": 400}

        return {"status": 200}
    return {"status": 400}


@USER.route("/getUserShareList/", methods=["GET"], endpoint="getUserShareList")
def get_user_share_list():
    """Get the list of users that the user can share to

    Returns:
        List: List of friends they can share w
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))

    user_obj = user_service.get_by_uuid(session["uuid"])
    user_id = user_obj.id

    friend_list = db.user_friend_service.get_friends(user_id)

    if len(friend_list) == 0:
        return {"status": 404, "error": "no users found"}

    username_list = [
        friend[1].username if friend[1].id != user_id else friend[2].username
        for friend in friend_list
    ]
    return {"status": 200, "username_list": username_list}


@USER.route("/serve/<path:path>")
def send_user_file(path: str):
    """
    This function is used to serve user files to the user. This function will check if the user is allowed to access the file
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()
    user_obj = user_service.get_by_uuid(session["uuid"])
    # If user is none then session is invalid
    if not valid_session:
        session["url"] = "go-back"
        return redirect(url_for("auth.login"))
    path_split = path.split("/")
    if "user_images" not in path_split[1] or "default" not in path_split[1]:
        return send_from_directory(directory="../static", path=path)
    if user_obj.name in path_split[2] or "default" in path_split[1]:
        return send_from_directory(directory="../static", path=path)
    return Response("Error user can not access these files", status=400)


@USER.route("/me")
def me():
    """
    This function is used to get the user object of the user that is currently logged in
    """
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        print("invalid session")
        return {"status": 400, "error": "invalid session"}, 401  # Unauthorized

    pending_alerts = session.get("pending_alerts", [])
    notifications = []

    for alert in pending_alerts:
        res = AsyncResult(alert)
        if res.ready():
            result = res.get(timeout=0.2)
            if not result:
                continue  # skip if no result from celery yet
            notifications.append(result)
            pending_alerts.remove(alert)

    session["pending_alerts"] = pending_alerts

    user_obj = user_service.get_by_uuid(session["uuid"])

    return {
        "status": 200,
        "uuid": user_obj.kc_uuid,
        "username": user_obj.username,
        "notifications": notifications,
    }, 200
