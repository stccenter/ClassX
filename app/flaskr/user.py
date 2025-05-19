# Python Third Party Imports
from flask import (current_app as app, Blueprint,
                   session, redirect,
                   url_for, render_template, request)

# Local Library Imports
from classxlib.database import DatabaseService
from classxlib.database.model import UserFriend
from classxlib.database.service import UserService
from classxlib.security.keycloak import oAuthManager
from .oauth import get_oauth
from classxlib.security.keycloak import oAuthManager
from .oauth import get_oauth
from .database import get_db

# OAuth App
oauth : oAuthManager

# OAuth App
oauth : oAuthManager

# DATABASE SERVICES IN USE
db : DatabaseService
user_service : UserService

USER = Blueprint('user', __name__, template_folder="/templates")

@USER.route('/settings/profile', methods=['GET'], endpoint='settings/profile')
def user_profile():
    oauth = get_oauth()
    valid_session = oauth.validate_user_session()

    if not valid_session:
        return redirect(url_for('auth.login'))

    return render_template('user/profile.html')

@USER.route('/settings/friends', methods=['GET'], endpoint='settings/')
def user_friends():
    oauth = get_oauth()
    valid_session = oauth.validate_user_session()

    if not valid_session:
        return redirect(url_for('auth.login'))

    return render_template('user/friends.html')

@USER.route('/friends', methods=["GET", "DELETE", "POST", "PATCH"], endpoint='friends')
def friends():
    oauth = get_oauth()
    valid_session = oauth.validate_user_session()
    
    if not valid_session:
        return redirect(url_for('auth.login'))
    db = get_db()

    user_obj = db.user_service.get_by_uuid(session['uuid'])
    user_id = user_obj.id
    
    if request.method == "GET":
     # get friends list and pending requests
        current_friends = db.user_friend_service.get_friends(user_id)
        pending = db.user_friend_service.get_pending(user_id)
        ret = []

        for friend in (pending + current_friends):
            status, sender, reciver = friend[0].status, friend[1], friend[2]
            sent = sender.id == user_id

            print(status, sender, reciver)
            if status == 0: # pending friend request logic
                ret.append({
                    'pending': True,
                    'sent': sent,
                    'username': reciver.username if sent else sender.username,
                    'uuid': reciver.kc_uuid if sent else sender.kc_uuid
                })

            elif status == 1: # accepted friend request logic
                ret.append({
                    'pending': False,
                    'username': reciver.username if sent else sender.username,
                    'uuid': reciver.kc_uuid if sent else sender.kc_uuid,
                })
                continue

        return ret
    elif request.method == "DELETE":
        uuid = request.args.get('uuid', None)
        if not uuid:
            return {'status': 400}
        
        other_user = db.user_service.get_by_uuid(uuid)

        if not other_user:
            return {'status': 400}
        
        
        success = db.user_friend_service.remove_request(user_id, other_user.id)
        if not success:
            return {'status': 400}
        
        return {'status': 200}

    
    elif request.method == "POST":
        data = request.get_json(cache=False, force=True, silent=True)
        if not data:
            return {'status': 400}
        
        username = data.get('username', None)
        if not username:
            return {'status': 400}
        elif username == user_obj.username or username == user_obj.kc_uuid:
            return {'status': 400}
        
        # they can get via username or uuid
        other_user = db.user_service.get_by_username(username)
        if not other_user:
            other_user = db.user_service.get_by_uuid(username)
            if not other_user:
                return {'status': 400}
        
        # check if there is already an out going friend request
        current_request = db.user_friend_service.get_status(user_id, other_user.id)
        if current_request:
            if current_request.status == 0:
                if current_request.receiver_id == user_id:
                    db.user_friend_service.accept_friend_request(other_user.id, user_id)
                    return {'status': 200, 'message': "User had a pending request from"}

                return {'status': 400, 'error': "request already sent"}
            elif current_request.status == 1:
                return {'status': 400, 'error': "already friends"}
            # Going here shouldnt happen since blocking doesnt exist yet
        
        friend_request = UserFriend(user_id, other_user.id, 0)
        
        db.user_friend_service.create_friend_request(friend_request)

        return {'status': 200, 'message': "Friend request sent"}
    
    elif request.method == "PATCH":
        # accept the friend request
        data = request.get_json(cache=False, force=True, silent=True)
        if not data: 
            return {'status': 400}
        
        uuid = data.get('uuid', None)
        if not uuid:
            return {'status': 400}
        elif uuid == user_obj.kc_uuid:
            return {'status': 400}
        
        other_user = db.user_service.get_by_uuid(uuid)

        if not other_user:
            return {'status': 400}
        
        current = db.user_friend_service.get_status(other_user.id, user_id)
        if not current:
            return {'status': 400}
        
        if current.status != 0:
            return {'status': 400}
        
        if current.sender_id != other_user.id:
            return {'status': 400}
        
        success = db.user_friend_service.accept_friend_request(other_user.id, user_id)
        if not success:
            return {'status': 400}
        
        return {'status': 200}


@USER.route('/getUserShareList/', methods=['GET'], endpoint="getUserShareList")
def get_user_share_list():
    # Retrieving Database
    db = get_db()
    oauth = get_oauth()

    # Setting up services
    user_service = db.user_service

    # Verifying the session is valid and retrieving user object
    valid_session = oauth.validate_user_session()

    # If user is none then session is invalid
    if not valid_session:
        session['url'] = 'go-back'
        return redirect(url_for('auth.login'))

    user_obj = user_service.get_by_uuid(session['uuid'])
    user_id = user_obj.id

    user_friends = db.user_friend_service.get_friends(user_id)

    if len(user_friends) == 0:
        return {'status': 404, 'error': "no users found"}
    
    user_obj_list = [friend[1] if friend[1].id != user_id else friend[2] for friend in user_friends]
    username_list = [user_obj.username for user_obj in user_obj_list]
    return {'status': 200, 'username_list': username_list}

