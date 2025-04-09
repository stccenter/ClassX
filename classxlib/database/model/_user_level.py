"""The pythonic dataclass for the user_levels table"""

# Python Standard Library Imports
from dataclasses import dataclass

# Local Library Imports
from ._base import BaseModel

__all__ = ["UserLevel"]


@dataclass(unsafe_hash=True)
class UserLevel(BaseModel):  # pylint: disable=too-many-instance-attributes
    """The dataclass that is the pythonic representation of
    a single row in the `users` sql database table.
    Each attribute of the class is a column in the sql table.
    Attributes:
        id (`int`, `primary-key`, `auto-increment`):
        The id associated with the user_level.
        name (`str`): The name of the authorization
        level. e.g. (Member, Moderator, Admin)
        permissions (`dict`): A dictionary containing
        the configurations for a given authorization level.
    """

    # NOTE for descriptions on the class attributes refer
    # to the docstring
    id: int
    name: str
    permissions: dict

    # Initialize the attributes
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions
