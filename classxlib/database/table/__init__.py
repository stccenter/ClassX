"""ClassX Database Tables"""

# classxlib/database/tables/__init__.py

from ._user import create_user_table
from ._user_level import create_user_level_table
from ._user_friend import create_user_friends_table
from ._user_research_id import create_user_research_fields_table
from ._original_image import create_original_image_table
from ._crop_image import create_crop_image_table
from ._segment_image import create_segment_image_table
from ._label_image import create_label_image_table
from ._research_field import create_research_field_table
from ._training_file import create_training_file_table

__all__ = [
    "create_user_table",
    "create_user_level_table",
    "create_user_friends_table",
    "create_user_research_fields_table",
    "create_original_image_table",
    "create_crop_image_table",
    "create_segment_image_table",
    "create_label_image_table",
    "create_research_field_table",
    "create_training_file_table",
]
