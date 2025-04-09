"""Security Module for verifying a user session"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
from flask import session

# Local Library Imports
from ..database.model import User
from ..database.service import UserService

__all__ = ["verify_session"]


def verify_session(user_service: UserService) -> User:
    """Verifies the user session by checking the session token against the database

    Args:
        user_service (UserService): User Service to access database User table

    Raises:
        TypeError: If the Secret Key is not a string.

    Returns:
        User: Returns User database object if token and session are verified
        otherwise returns None if verification fails.
    """

    try:
        # Verifying the token exists within the session
        if "token" not in session:
            return None

        # Checking the token against the database to verify integrity
        user_obj = user_service.get_by_uuid(session["token"])

        # Checking if the User was found
        if user_obj is None:
            return None

        # Return the user object if no issues are found
        return user_obj
    except (RuntimeError, TypeError) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return None
