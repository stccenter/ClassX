"""Module for generating the crop image table"""

# Python Third Party Imports
from sqlalchemy import (Table, Column,
                        Integer, String,
                        ForeignKey,MetaData,
                        Text, DateTime)

__all__ = ['create_crop_image_table']

def create_crop_image_table(metadata:MetaData):
    """Generates the sqlachemy table structure
    for the `crop_image` table.

    Args:
        metadata (MetaData): Metadata object to share
        between tables.

    Returns:
        sqlalchemy.Table: The sqlalchemy table object
    """
    # NOTE There are more details on column details in the model
    # files for this table

    # Creates a table object with the specified columns
    crop_images_table = Table(
        "crop_images",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("user_id", Integer, ForeignKey("users.id"),nullable=False),
        Column("shared_by", Integer,ForeignKey("users.id"), nullable=True),
        Column("shared_from", Integer, ForeignKey("users.id"), nullable=True),
        Column("original_image_id", Integer, ForeignKey("original_images.id"), nullable=False),
        Column("research_id", Integer, ForeignKey("research_fields.id"), nullable = False),
        Column("name", String(50), nullable=False),
        Column("h5_path", Text(1000), nullable=False),
        Column("last_modified_date",DateTime),
        Column("width", Integer, nullable=False),
        Column("height", Integer, nullable=False),
        Column("visualization_path", Text(1000), nullable=False),
        Column("crop_size", Integer),
        Column("crop_type",String(50))
        )
    return crop_images_table


