"""Module for generating the training files table"""

# Python Third Party Imports
from sqlalchemy import Table, Column, Integer, String, JSON, ForeignKey, MetaData, Text

__all__ = ["create_training_file_table"]


def create_training_file_table(metadata: MetaData):
    """Generates the sqlachemy table structure
    for the `training_files` table.

    Args:
        metadata (MetaData): Metadata object to share
        between tables.

    Returns:
        sqlalchemy.Table: The sqlalchemy table object
    """
    # NOTE There are more details on column details in the model
    # files for this table

    # Creates a table object with the specified columns
    training_files_table = Table(
        "training_files",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
        Column(
            "research_id", Integer, ForeignKey("research_fields.id"), nullable=False
        ),
        Column("shared_by", Integer, nullable=True),
        Column("shared_from", Integer, nullable=True),
        Column("file_name", String(length=100), nullable=False),
        Column("file_path", Text(1000), nullable=False),
        Column("model_path", Text(1000), nullable=False),
        Column("label_count", JSON, nullable=False),
    )
    return training_files_table
