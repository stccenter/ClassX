"""Module for generating the original image table"""

# Python Third Party Imports
from sqlalchemy import (Table, Column,
                        Integer, String,
                        JSON, ForeignKey,
                        MetaData, Text,
                        DateTime, Numeric)

__all__ = ['create_segment_image_table']

def create_original_image_table(metadata:MetaData):
    """Generates the sqlachemy table structure
    for the `original_images` table.

    Args:
        metadata (MetaData): Metadata object to share
        between tables.

    Returns:
        sqlalchemy.Table: The sqlalchemy table object
    """
    # NOTE There are more details on column details in the model
    # files for this table

    # Creates a table object with the specified columns
    original_image_table = Table(
        "original_images",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("user_id", Integer, ForeignKey("users.id"),nullable=False),
        Column("shared_by", Integer,ForeignKey("users.id"), nullable=True),
        Column("shared_from", Integer, ForeignKey("users.id"), nullable=True),
        Column("research_id", Integer, ForeignKey("research_fields.id"), nullable = False),
        Column("name", String(100), nullable=False),
        Column("alias", String(100)),
        Column("path", Text(1000), nullable=False),
        Column("thumbnail_path", Text(1000)),
        Column("crop_grid_path", Text(1000)),
        Column("upload_time", DateTime, nullable = False),
        Column("creation_date",DateTime),
        Column("last_modified_date",DateTime),
        Column("width", Integer),
        Column("height", Integer),
        Column("size", Numeric(precision=10, scale=2), nullable = False),
        Column("h5_path", Text(1000), nullable=False),
        Column("visualization_path", Text(1000), nullable=False),
        Column("file_type", String(50), nullable=False),
        Column("mode", String(50), nullable=False),
        Column("metadata", JSON, nullable = False),
        )
    return original_image_table


