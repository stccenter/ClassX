"""The pythonic dataclass for the segmented_images table"""

# Python Standard Library Imports
from dataclasses import dataclass
from datetime import datetime

# Local Library Imports
from ._base import BaseModel

__all__ = ["SegmentImage"]


@dataclass(unsafe_hash=True)
class SegmentImage(BaseModel):  # pylint: disable=too-many-instance-attributes
    """The dataclass that is the pythonic representation of
    a single row in the `segmented_images` sql database table.
    Each attribute of the class is a column in the sql table.

    Attributes:
        id (`int`, `primary-key`, `auto-increment`):
        The id associated with the segment image.
        user_id (`int`,`foreign-key`): The id of the user that
        owns the segment image.
        shared_by (`int`): The id of the user who shared the image,
        will be None if no one shared it. Defaults to None.
        shared_from (`int`): The id of the original segment image it was shared from.
        Will be none if this is the original row. Defaults to None.
        crop_image_id (`int`,`foreign-key`): The id of the crop image this
        segment image was segmented from.
        research_id (`int`,`foreign-key`): The id of the research domain this
        image belongs to.
        name (`str`): The file name of the segment image data.
        segment_path (`str`): The file path to the segment image mask
        data.
        marked_image_path (`str`): The file path to the crop_image with the
        segment boundaries marked.
        last_modified_date (`datetime`): The last time the image was used/edited.
        segment_method (`int`): The id of the segmentation algorithm used.
        param1 (`float`): The numeric value of the first parameter for the segment
        method used.
        param2 (`float`): The numeric value of the second parameter for the segment
        method used.
        param3 (`float`): The numeric value of the third parameter for the segment
        method used.
        region_merge_method (`int`): The id of the region merging algorithm used.
        Will be set to 0 if unused/disabled.
        region_merge_threshold (`float`): The numeric value of the similarity threshold
        used for merging segments.
        small_rem_method (`int`): The id of the small object/segment removal algorithm
        used. Will be set to 0 if unused/disabled.
        small_rem_threshold (`float`): The numeric value of the size threshold used
        for removing objects/segments.
        light_method (`int`): The id of the light adjustment algorithm used on the image.
        Will be set to 0 if unused/disabled.
        contrast_method (`int`): The id of the contrast stretch algorithm used on the image.
        Will be set to 0 if unused/disabled.
        color_method (`int`): The id of the color clustering/quantization algorithm used
        on the image. Will be set to 0 if unused/disabled.
        color_clusters (`int`): The amount of colors the image was reduced/quantized to.
        crop_size (`int`): The size of the crop_image that was segmented.
    """

    # NOTE for descriptions on the class attributes refer
    # to the docstring
    id: int
    user_id: int
    shared_by: int
    shared_from: int
    crop_image_id: int
    research_id: int
    name: str
    segment_path: str
    marked_image_path: str
    last_modified_date: datetime
    segment_method: int
    param1: float
    param2: float
    param3: float
    region_merge_method: int
    region_merge_threshold: float
    small_rem_method: int
    small_rem_threshold: float
    light_method: int
    contrast_method: int
    color_method: int
    color_clusters: int
    crop_size: int

    # Initialize the attributes
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(
        self,
        user_id,
        shared_by,
        shared_from,
        crop_image_id,
        research_id,
        name,
        segment_path,
        marked_image_path,
        last_modified_date,
        param1,
        param2,
        param3,
        segment_method,
        region_merge_method,
        region_merge_threshold,
        small_rem_method,
        small_rem_threshold,
        light_method,
        contrast_method,
        color_method,
        color_clusters,
        crop_size,
    ):
        self.user_id = user_id
        self.shared_by = shared_by
        self.shared_from = shared_from
        self.crop_image_id = crop_image_id
        self.research_id = research_id
        self.name = name
        self.segment_path = segment_path
        self.last_modified_date = last_modified_date
        self.marked_image_path = marked_image_path
        self.segment_method = segment_method
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.region_merge_method = region_merge_method
        self.region_merge_threshold = region_merge_threshold
        self.small_rem_method = small_rem_method
        self.small_rem_threshold = small_rem_threshold
        self.light_method = light_method
        self.contrast_method = contrast_method
        self.color_method = color_method
        self.color_clusters = color_clusters
        self.crop_size = crop_size
