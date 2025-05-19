"""Module for generating the segmented images table"""

# Python Third Party Imports
from sqlalchemy import (Table, Column,
                        Integer, String,
                        ForeignKey,MetaData,
                        Text, Float,
                        DateTime)

__all__ = ['create_segment_image_table']

def create_segment_image_table(metadata:MetaData):
    """Generates the sqlachemy table structure
    for the `segment_images` table.

    Args:
        metadata (MetaData): Metadata object to share
        between tables.

    Returns:
        sqlalchemy.Table: The sqlalchemy table object
    """
    # NOTE There are more details on column details in the model
    # files for this table

    # Creates a table object with the specified columns
    segment_image_table = Table(
        "segment_images",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("user_id", Integer, ForeignKey("users.id"),nullable=False),
        Column("shared_by", Integer,ForeignKey("users.id"), nullable=True),
        Column("shared_from", Integer, ForeignKey("users.id"), nullable=True),
        Column("crop_image_id", Integer, ForeignKey("crop_images.id"), nullable=False),
        Column("research_id", Integer, ForeignKey("research_fields.id"), nullable = False),
        Column("name", String(50), nullable=False),
        Column("segment_path", Text(1000), nullable=False),
        Column("marked_image_path", Text(1000), nullable=False),
        Column("param1", Float, default=0,nullable = False),
        Column("param2", Float, default=0,nullable = False),
        Column("param3", Float, default=0,nullable = False),
        Column("last_modified_date",DateTime),
        Column("segment_method", Integer, default=1,nullable = False),
        Column("region_merge_method", Integer, default=0,nullable = False),
        Column("region_merge_threshold", Float, default=0,nullable = False),
        Column("small_rem_method", Integer, default=0, nullable = False),
        Column("small_rem_threshold", Float, default=0, nullable = False),
        Column("light_method", Integer, nullable = False),
        Column("contrast_method", Integer, nullable = False),
        Column("color_method", Integer, nullable = False),
        Column("color_clusters", Integer, nullable = False),
        Column("crop_size", Integer, nullable=False)
        )
    return segment_image_table


