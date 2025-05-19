"""The pythonic dataclass for the labeled_images table"""
# Python Standard Library Imports
from dataclasses import dataclass
from datetime import datetime

# Local Library Imports
from ._base import BaseModel

__all__ = ['LabelImage']

@dataclass(unsafe_hash=True)
class LabelImage(BaseModel):  # pylint: disable=too-many-instance-attributes
    """The dataclass that is the pythonic representation of
    a single row in the `labeled_images` sql database table.
    Each attribute of the class is a column in the sql table.

    Attributes:
    id (`int`, `primary-key`, `auto-increment`):
    The id associated with the label image.
    user_id (`int`,`foreign-key`): The id of the user that
    created the label image. The user id in this case does not denote
    ownership, ownership falls to the owner of the training file it was
    appended to.
    training_file_id (`int`,`foreign-key`): The id of the training file
    the labeled image belongs to.
    segment_image_id (`int`,`foreign-key`): The id of the segment image
    the label image was created from.
    color_image_path (`str`): Path to the marked image with the segments
    colored with their appropriate labels.
    last_modified (`datetime`): The time the label image was created or modified.
    """

    # NOTE for descriptions on the class attributes refer
    # to the docstring
    id : int
    user_id : int
    training_file_id : int
    segment_image_id : int
    color_image_path : str
    last_modified: datetime

    # Initialize the attributes
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self,
                 user_id, training_file_id,
                 segment_image_id, color_image_path,
                 last_modified):
        self.user_id = user_id
        self.training_file_id = training_file_id
        self.segment_image_id = segment_image_id
        self.color_image_path = color_image_path
        self.last_modified = last_modified
