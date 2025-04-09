"""The pythonic dataclass for the original_images table"""

# Python Standard Library Imports
from dataclasses import dataclass
from datetime import datetime

# Local Library Imports
from ._base import BaseModel

__all__ = ["OriginalImage"]


@dataclass(unsafe_hash=True)
class OriginalImage(BaseModel):  # pylint: disable=too-many-instance-attributes
    """The dataclass that is the pythonic representation of
    a single row in the `original_images` sql database table.
    Each attribute of the class is a column in the sql table.

    Attributes:
        id (`int`, `primary-key`, `auto-increment`):
        The id associated with the original image.
        user_id (`int`,`foreign-key`): The id of the user that
        owns the image.
        shared_by (`int`): The id of the user who shared the image,
        will be None if no one shared it. Defaults to None.
        shared_from (`int`): The id of the original image it was shared from.
        Will be none if this is the original row. Defaults to None.
        research_id (`int`,`foreign-key`): The id of the research domain this
        image belongs to.
        name (`str`): The file name of the unaltered original image data.
        alias (`str`): The changeable name of the original file, by default
        it will be the same as the name column
        path (`str`): The file path to the unaltered original image data.
        visualization_path (`str`): The file path to the visualization image used for viewing.
        h5_path (`str`): The file path to the HDF5 original image data, after
        adjustments are made to make it compatiable with the system. This is what is used
        for most processing tasks.
        thumbnail_path (`str`): The file path to the thumbnail image of the original image.
        crop_grid_path (`str`): The file path to the grid line image used for the automatic
        cropping.
        upload_time (`datetime`): The time & date the image was uploaded.
        creation_date (`datetime`): If available the time & date the original image was
        taken, rendered, etc.. Defaults to None.
        last_modified_date (`datetime`): The last time the image was used/edited.
        width (`int`): The width of the image
        height (`int`):The height of the image
        size (`float`): The file size in megabytes of the unaltered original image data
        file_type (`str`): The file type of the unaltered original image data.
        (.png,.tif,.fits,etc...)
        mode (`str`): The data format of the original image data.
        (RGB, Grayscale, Multi-Spectural, etc...)
        metadata (`dict`): The dictionary for the extracted image metadata.
    """

    # NOTE for descriptions on the class attributes refer
    # to the docstring
    id: int
    user_id: int
    shared_by: int
    shared_from: int
    research_id: int
    name: str
    alias: str
    path: str
    h5_path: str
    visualization_path: str
    thumbnail_path: str
    crop_grid_path: str
    upload_time: datetime
    creation_date: datetime
    last_modified_date: datetime
    width: int
    height: int
    size: float
    file_type: str
    mode: str
    metadata: dict

    # Initialize the attributes
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(
        self,
        user_id,
        shared_by,
        shared_from,
        research_id,
        name,
        alias,
        path,
        h5_path,
        visualization_path,
        thumbnail_path,
        crop_grid_path,
        upload_time,
        creation_date,
        last_modified_date,
        width,
        height,
        size,
        file_type,
        mode,
        metadata,
    ):
        self.user_id = user_id
        self.shared_by = shared_by
        self.shared_from = shared_from
        self.research_id = research_id
        self.name = name
        self.alias = alias
        self.path = path
        self.h5_path = h5_path
        self.visualization_path = visualization_path
        self.thumbnail_path = thumbnail_path
        self.crop_grid_path = crop_grid_path
        self.upload_time = upload_time
        self.creation_date = creation_date
        self.last_modified_date = last_modified_date
        self.width = width
        self.height = height
        self.size = size
        self.file_type = file_type
        self.mode = mode
        self.metadata = metadata
