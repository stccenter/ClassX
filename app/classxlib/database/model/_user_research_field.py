"""The pythonic dataclass for the user_levels table"""
# Python Standard Library Imports
from dataclasses import dataclass

# Local Library Imports
from ._base import BaseModel

__all__ = ['UserResearchField']

@dataclass(unsafe_hash=True)
class UserResearchField(BaseModel): # pylint: disable=too-many-instance-attributes
    """The dataclass that is the pythonic representation of
    a single row in the `user_research_fields` sql database table.
    Each attribute of the class is a column in the sql table.
    Attributes:
        id (`int`, `primary-key`, `auto-increment`):
        The id associated with the user_level.
        user_id (`int`): The user this row applies to
        research_field_id (`int`): Research field that this applies
        the configurations for a given authorization level.
    """
    # NOTE for descriptions on the class attributes refer
    # to the docstring
    id : int
    user_id : int
    research_id : int
    role_id : int

    # Initialize the attributes
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, user_id,
                 research_id,
                 role_id):
        self.user_id = user_id
        self.research_id = research_id
        self.role_id = role_id
