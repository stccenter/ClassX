"""Validation function for checking default user"""
# Python Standard Library Imports
import traceback

# Local Library Imports
from .model import User

__all__ = ['is_default_user']

def is_default_user(user_obj:User) -> bool:
    """Checks if a user is the default admin user

    Args:
        user_obj (User): User Class Object from database

    Raises:
        TypeError: If the argument given is not a User Class Object

    Returns:
        bool: True if the user is verified as default admin
    """
    # Verifying arguments
    if not isinstance(user_obj, User):
        raise TypeError("TypeError: user_obj argument must be User Class Object")

    try:
        # Checking if the username and level match correctly for the user
        if(user_obj.username == "default" and user_obj.user_level == 3):
            return True

        # f not return false
        return False
    except (TypeError, RuntimeError,
            ValueError, RuntimeWarning) as error:
        print("Error:", error)
        traceback.print_tb(error.__traceback__)
        return False
