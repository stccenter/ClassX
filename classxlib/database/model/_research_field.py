"""The pythonic dataclass for the research_fields table"""

# Python Standard Library Imports
from dataclasses import dataclass
from datetime import datetime

# Local Library Imports
from ._base import BaseModel

__all__ = ["ResearchField"]


@dataclass(unsafe_hash=True)
class ResearchField(BaseModel):  # pylint: disable=too-many-instance-attributes
    """The dataclass that is the pythonic representation of
    a single row in the `research_fields` sql database table.
    Each attribute of the class is a column in the sql table.
    Attributes:
        id (`int`, `primary-key`, `auto-increment`):
        The id associated with the research field.
        user_id (`int`,`foreign-key`): The id of the user that
        created/owns the research field.
        name (`str`): The name of the research field.
        visibility (`int`): The id which refers to the privacy settings
        of the research field. e.g. 1 is default, 2 is public, 3 is private.
        label_map (`dict`): dictionary list of all the labels in this field.
        Contains their label ids, colors, and names.
        metadata_map (`dict`): Dictionary list of all the metadata extracted from
        in this research field from images.
        protocols (`dict`): Contains the upload & processing protocols for images in
        this field.
        field_data (`dict`): Contains all extra info about this research field such
        as users assigned, descriptions, and permission settings.
    """

    # NOTE for descriptions on the class attributes refer
    # to the docstring
    id: int
    user_id: int
    name: str
    visibility: int
    last_modified_date: datetime
    label_map: dict
    metadata_map: dict
    protocols: dict
    field_data: dict

    # Initialize the attributes
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(
        self,
        name,
        user_id,
        visibility,
        last_modified_date,
        label_map,
        metadata_map,
        protocols,
        field_data,
    ):
        self.name = name
        self.user_id = user_id
        self.visibility = visibility
        self.last_modified_date = last_modified_date
        self.label_map = label_map
        self.metadata_map = metadata_map
        self.protocols = protocols
        self.field_data = field_data
