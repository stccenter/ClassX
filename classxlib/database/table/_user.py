"""Module for generating the user table"""

# Python Third Party Imports
from sqlalchemy import Table, Column, Integer, String, JSON, ForeignKey, MetaData

__all__ = ["create_user_table"]


def create_user_table(metadata: MetaData):
    """Generates the sqlachemy table structure
    for the `users` table.

    Args:
        metadata (MetaData): Metadata object to share
        between tables.

    Returns:
        sqlalchemy.Table: The sqlalchemy table object
    """
    # NOTE There are more details on column details in the model
    # files for this table

    # Creates a table object with the specified columns
    user_table = Table(
        "users",
        metadata,
        Column(
            "id", Integer, primary_key=True, autoincrement=True
        ),  # TODO This will be swapped out for a uuid
        Column("username", String(length=100), nullable=False, unique=True),
        Column("user_level", Integer, ForeignKey("user_levels.id"), nullable=False),
        Column("kc_uuid", String(length=255), nullable=False, unique=True),
    )
    return user_table
