"""Module for generating the user levels table"""

# Python Third Party Imports
from sqlalchemy import Table, Column, Integer, String, MetaData, JSON

__all__ = ["create_user_level_table"]


def create_user_level_table(metadata: MetaData):
    """Generates the sqlachemy table structure
    for the `user_levels` table.

    Args:
        metadata (MetaData): Metadata object to share
        between tables.

    Returns:
        sqlalchemy.Table: The sqlalchemy table object
    """
    # NOTE There are more details on column details in the model
    # files for this table

    # Creates a table object with the specified columns
    user_levels_table = Table(
        "user_levels",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String(50), nullable=False),
        Column("permissions", JSON, nullable=False),
    )
    return user_levels_table
