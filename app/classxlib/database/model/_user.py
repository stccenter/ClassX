"""The pythonic dataclass for the user table"""
# Python Standard Library Imports
from dataclasses import dataclass

# Local Library Imports
from ._base import BaseModel

__all__ = ['User']

@dataclass(unsafe_hash=True)
class User(BaseModel):  # pylint: disable=too-many-instance-attributes
    """The dataclass that is the pythonic representation of
    a single row in the `users` sql database table.
    Each attribute of the class is a column in the sql table.
    Attributes:
        id (`int`, `primary-key`, `auto-increment`):
        The id associated with the user.
        user_level (`int`,`foreign-key`): The id for the user
        authorization level
        kc_uuid (`str`): keycloak given uid also known as "sub" in their api
        username (`str`): The username of the user account, used as a login method.
    """
    # NOTE for descriptions on the class attributes refer
    # to the docstring
    id : int
    username : str
    user_level : int
    kc_uuid : str

    # Initialize the attributes
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, username,
                 kc_uuid, user_level):
        self.username = username
        self.user_level = user_level
        self.kc_uuid = kc_uuid
