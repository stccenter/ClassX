"""
Keycloak OAuth Manager
"""

# pylint: disable=invalid-name,missing-timeout
# Python Imports
import datetime
from os import environ

# Third party imports
from secrets import token_urlsafe

import jwt
import requests
from flask import Response, session
from authlib.integrations.flask_client import OAuth


__all__ = ["oAuthManager"]


class oAuthManager:
    """
    OAuth Manager for Keycloak
    """

    __session = None
    __oAtuh = None

    def __init__(self, client_id, client_secret) -> None:
        """
        Creates a new instance of a UserManager class.
        This class is used to update users via keycloaks admin API
        """
        if oAuthManager.__session is None:
            oAuthManager.__session = requests.session()
        self.__CLIENT_ID = client_id
        self.__CLIENT_SECRET = client_secret
        self.__BASE_URL = environ.get("KC_SOURCE_URL")
        self.__REALM = environ.get("KC_REALM")

        neg_time = datetime.datetime.now() - datetime.timedelta(0, 1)
        self.__token = {"token": None, "expires": neg_time}
        self.__certificate = {"cert": None, "expires": neg_time}

        # make sure we have envoriment variables
        if not self.__BASE_URL or not self.__REALM:
            raise EnvironmentError(
                "Could not find envoriment variables for keycloak's base url & the realm to manage."
            )
        # Ensure we have a trailing slash to make life easier
        if not self.__BASE_URL.endswith("/"):
            self.__BASE_URL += "/"

        # Call this method after we make sure the base url has the ending slash
        self.__get_keycloak_cert()

    def __get_auth_token(self):
        """
        Private method to get the auth token to be used in other methods caches until expired

        :returns: None
        """
        try:
            res = requests.post(
                f"{self.__BASE_URL}realms/{self.__REALM}/protocol/openid-connect/token",
                data={
                    "client_id": self.__CLIENT_ID,
                    "grant_type": "client_credentials",
                    "client_secret": self.__CLIENT_SECRET,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("REQUEST URL")
            print(
                f"{self.__BASE_URL}realms/{self.__REALM}/protocol/openid-connect/token"
            )
            print("DATA")
            data = {
                "client_id": self.__CLIENT_ID,
                "grant_type": "client_credentials",
                "client_secret": self.__CLIENT_SECRET,
            }
            print(data)
            raise SystemExit(err)
        data = res.json()
        self.__token = {
            "token": data["access_token"],
            "expires": datetime.datetime.now()
            + datetime.timedelta(0, data["expires_in"]),
        }

    def __get_keycloak_cert(self):
        """
        Private method to get the public key to decode user tokens caches for 12 hours

        :returns: None
        """
        self.__validate_current_auth_token()
        res = self.__session.get(
            f"{self.__BASE_URL}realms/{self.__REALM}",
            headers={"Authorization": "Bearer " + self.__token["token"]},
        )

        self.__certificate = {
            "cert": "-----BEGIN PUBLIC KEY-----\n"
            + res.json()["public_key"]
            + "\n-----END PUBLIC KEY-----",
            "expires": datetime.datetime.now() + datetime.timedelta(0.5),
        }

    def __validate_current_auth_token(self):
        """
        Private method to get a new auth token
        if our current one is expired private to not clog intelisense

        :returns: None
        """
        if datetime.datetime.now() > self.__token["expires"]:
            self.__get_auth_token()

    def __validate_current_cert(self):
        """
        Private method to get a new cert if our
        current one is expired private to not clog intelisense

        :returns: None
        """
        if datetime.datetime.now() > self.__certificate["expires"]:
            self.__get_keycloak_cert()

    def refresh_session_token(self, decoded_token: dict) -> None:
        """
        Refresh the user's session token

        :session: the flask session to refresh the token for

        :returns: None
        """
        client_id = decoded_token.get("azp", None)
        if not client_id:
            print("client id invalid")
            client_id = self.__CLIENT_ID
            client_secret = self.__CLIENT_SECRET
        else:
            client_secret = environ.get("OAUTH_SECRET")
        refresh_token = session.get("user", {}).get("refresh_token", None)
        if not refresh_token:
            print("No refresh token found in session :(")
            return

        res = requests.post(
            f"{self.__BASE_URL}realms/{self.__REALM}/protocol/openid-connect/token",
            data={
                "client_id": client_id,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_secret": client_secret,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        res.raise_for_status()

        data = res.json()

        session["user"]["access_token"] = data["access_token"]
        session["user"]["refresh_token"] = data["refresh_token"]

    def validate_user_session(self) -> bool:
        """
        Validate a user's current session against
        keycloak this method just simplifies getting the access token

        :session: the flask session of the user we want to check the auth against

        :return: Boolean if the user's session is valid false if the token is invalid
        """
        token = session.get("user", {}).get("access_token", None)
        if token is None:
            print("could not find token in session")
            return False

        data = self.decode_token(token)
        if not data:
            print("could not decode token")
            return False

        expires = data.get("exp", 0)
        now = datetime.datetime.now().timestamp()
        time_until_expires = expires - now
        try:
            if (
                0 < time_until_expires < 120
            ):  # Refresh the token if <2min remaining but not expired
                # print("Refreshing token")
                self.refresh_session_token(data)
        except Exception:
            username = None
            if "user" in session:
                username = session["user"]["userinfo"]["preferred_username"]
            print("There was an error refreshing token for:", username)
            return False

        # self.refresh_session_token(session, data)
        # print(expires, now, time_until_expires)
        print(f"{expires} > {now}")
        return expires > now

    def decode_token(self, token: str) -> dict:
        """
        decode an auth token

        :token: user's token to decode

        :return: dict decoded token
        """
        self.__validate_current_cert()
        try:
            decoded: dict = jwt.decode(
                token, self.__certificate["cert"], ["RS256"], audience="account"
            )
        except jwt.InvalidTokenError as err:
            return {}
        return decoded

    def get_user_id_by_uuid(self, uuid: str) -> dict:
        """
        Get a keycloak user by the user ID.

        :uuid: the uuid to get

        :return: dict of the user data in keycloak
        """
        self.__validate_current_auth_token()
        res = self.__session.get(
            f"{self.__BASE_URL}admin/realms/{self.__REALM}/users/{uuid}",
            headers={"Authorization": "Bearer " + self.__token["token"]},
        )
        res.raise_for_status()
        return res.json()

    def update_user(self, uuid: str, data: dict) -> dict:
        """
        Updates a user in keycloak based on data given.
        Since keycloak does not support patical updates
        we have to get the current user object add our data then update.

        :uuid: the uuid to update
        :data: the dict data to update in keycloak I.E {"email": "example@example.com"}

        :returns: dict[str, Any] dict with the new user
        """
        self.__validate_current_auth_token()

        # KEY CLOAK DOES NOT SUPPORT PARTIAL UPDATES SINCE 24.0.2
        user = self.get_user_id_by_uuid(uuid)
        for key, new_value in data.items():
            if key in user:
                user[key] = new_value

        res = self.__session.put(
            f"{self.__BASE_URL}admin/realms/{self.__REALM}/users/{uuid}",
            headers={
                "Authorization": "Bearer " + self.__token["token"],
                "Content-Type": "application/json",
            },
            json=user,
        )
        res.raise_for_status()

        # Return the updated/new user
        return user

    def setup_oath(self, app, replace=False) -> None:
        """
        Create flask oAuth manager

        :app: flask app to setup the oAuth for
        :replace: if we should replace the current oAuth object

        """
        if replace or oAuthManager.__oAtuh is None:
            oauth = OAuth(app)
            oAuthManager.__oAtuh = oauth.register(
                name="keycloak",
                client_id=app.config["OAUTH2_CLIENT_ID"],
                client_secret=app.config["OAUTH2_CLIENT_SECRET"],
                server_metadata_url=app.config["OAUTH2_META_URL"],
                auth_url=app.config["OAUTH2_AUTH_URL"],
                token_url=app.config["OAUTH2_TOKEN_URL"],
                client_kwargs={
                    "scope": "openid profile",
                    # "code_challenge_method": 'S256' # Enable PKCE
                },
            )

    def authorize_redirect(self, redirect_uri, *args, **kargs) -> Response:
        """
        Wrapper for the poorly typed "oauth.register()" method to authorize
        a redirect we set the nonce here when we're given the session also redirect uri

        :session: flask session we're mutating
        :redirect_uri: auth url to redirect to
        :args: any args that we may need one day
        :kargs: even more args

        :returns: flask Response (must be final line if
        being used as it will redirect the user out of the current function)

        """
        if self.__oAtuh is None:
            raise EnvironmentError(
                "oAuthManger.setup_oauth was not called yet cant use this."
            )

        nonce = token_urlsafe(16)
        session["nonce"] = nonce

        return oAuthManager.__oAtuh.authorize_redirect(
            redirect_uri=redirect_uri, nonce=nonce, *args, **kargs
        )

    def authorize_access_token(self) -> dict:
        """
        Wrapper for the poorly typed "oauth.authorize_access_token()"
        to get the user's login session after calling oAuthManager.authorize_redirect()

        :returns: user session if authorized

        """
        if self.__oAtuh is None:
            raise EnvironmentError(
                "oAuthManger.setup_oauth was not called yet cant use this."
            )

        return oAuthManager.__oAtuh.authorize_access_token()
