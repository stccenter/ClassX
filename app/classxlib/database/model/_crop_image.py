"""The pythonic dataclass for the crop_images table"""
# Python Standard Library Imports
from dataclasses import dataclass
from datetime import datetime

# Local Library Imports
from ._base import BaseModel

__all__ = ['CropImage']

@dataclass(unsafe_hash=True)
class CropImage(BaseModel): # pylint: disable=too-many-instance-attributes
    """The dataclass that is the pythonic representation of
    a single row in the `cropped_images` sql database table.
    Each attribute of the class is a column in the sql table.

    Attributes:
        id (`int`, `primary-key`, `auto-increment`):
        The id associated with the crop image.
        user_id (`int`,`foreign-key`): The id of the user that
        owns the crop image.
        shared_by (`int`): The id of the user who shared the image,
        will be None if no one shared it. Defaults to None.
        shared_from (`int`): The id of the original crop image it was shared from.
        Will be none if this is the original row. Defaults to None.
        original_image_id (`int`,`foreign-key`): The id of the original image this
        crop image was cropped from.
        research_id (`int`,`foreign-key`): The id of the research domain this
        image belongs to.
        name (`str`): The file name of the crop image data.
        visualization_path (`str`): The file path to the visualization image used for viewing.
        h5_path (`str`): The file path to the HDF5 original crop image data, after
        adjustments are made to make it compatiable with the system. This is what is used
        for most processing tasks.
        last_modified_date (`datetime`): The last time the image was used/edited.
        width (`int`): The width point of the original image at the bottom right corner of the
        crop image.
        height (`int`): The height point of the original image at the bottom right corner of the
        crop image.
        crop_size (`int`): The size of the crop image in pixels.
        crop_type (`str`): The type of crop image either manual or auto.
    """
    # NOTE for descriptions on the class attributes refer
    # to the docstring
    id : int
    user_id : int
    shared_by : int
    shared_from : int
    original_image_id : int
    research_id : int
    name : str
    visualization_path : str
    h5_path : str
    last_modified_date : datetime
    width : int
    height : int
    crop_size : int
    crop_type : str

    # Initialize the attributes
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, user_id,
                 shared_by, shared_from,
                 original_image_id, research_id,
                 name, visualization_path,
                 h5_path, last_modified_date,
                 width, height,
                 crop_size, crop_type):
        self.user_id = user_id
        self.shared_by = shared_by
        self.shared_from = shared_from
        self.original_image_id = original_image_id
        self.research_id = research_id
        self.name = name
        self.visualization_path = visualization_path
        self.h5_path = h5_path
        self.last_modified_date = last_modified_date
        self.width = width
        self.height = height
        self.crop_size = crop_size
        self.crop_type = crop_type
