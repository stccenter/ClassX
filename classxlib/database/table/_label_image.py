"""Module for generating the labeled_images table"""

# Python Third Party Imports
from sqlalchemy import Table, Column, Integer, ForeignKey, MetaData, DateTime, String

__all__ = ["create_label_image_table"]


def create_label_image_table(metadata: MetaData):
    """Generates the sqlachemy table structure
    for the `labeled_images` table.

    Args:
        metadata (MetaData): Metadata object to share
        between tables.

    Returns:
        sqlalchemy.Table: The sqlalchemy table object
    """
    # NOTE There are more details on column details in the model
    # files for this table

    # Creates a table object with the specified columns
    labeled_images_table = Table(
        "label_images",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
        Column(
            "training_file_id", Integer, ForeignKey("training_files.id"), nullable=False
        ),
        Column(
            "segment_image_id", Integer, ForeignKey("segment_images.id"), nullable=False
        ),
        Column("color_image_path", String(length=100), nullable=False),
        Column("last_modified", DateTime, nullable=False),
    )
    return labeled_images_table
