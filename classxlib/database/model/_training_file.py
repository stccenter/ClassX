"""The pythonic dataclass for the training_files table"""

# Python Standard Library Imports
from dataclasses import dataclass

# Local Library Imports
from ._base import BaseModel


@dataclass(unsafe_hash=True)
class TrainingFile(BaseModel):  # pylint: disable=too-many-instance-attributes
    """The dataclass that is the pythonic representation of
    a single row in the `training_files` sql database table.
    Each attribute of the class is a column in the sql table.
    Attributes:
        id (`int`, `primary-key`, `auto-increment`):
        The id associated with the segment image.
        user_id (`int`,`foreign-key`): The id of the user that
        owns the training file.
        research_id (`int`,`foreign-key`): The id of the research domain this
        image belongs to.
        shared_by (`int`): The id of the user who shared the image,
        will be None if no one shared it. Defaults to None.
        shared_from (`int`): The id of the original training file it was shared from.
        Will be none if this is the original row. Defaults to None.
        file_name (`str`): The name of the training file.
        file_path (`str`): The file directory to the location of the training file
        model_path (`str`): The file directory to the location of any trained models for
        this training file.
        label_counts (`dict`): A dictionary containing the label counts for each label type
        in this file.
    """

    # NOTE for descriptions on the class attributes refer
    # to the docstring
    id: int
    user_id: int
    research_id: int
    shared_by: int
    shared_from: int
    file_name: str
    file_path: str
    model_path: str
    label_count: dict

    # Initialize the attributes
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(
        self,
        user_id,
        research_id,
        shared_by,
        shared_from,
        file_name,
        file_path,
        model_path,
        label_count,
    ):
        self.user_id = user_id
        self.research_id = research_id
        self.file_name = file_name
        self.file_path = file_path
        self.model_path = model_path
        self.shared_by = shared_by
        self.shared_from = shared_from
        self.label_count = label_count
