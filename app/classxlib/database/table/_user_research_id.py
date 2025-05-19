"""Module for generating the user levels table"""

# Python Third Party Imports
from sqlalchemy import (Table, Column,
                        Integer, MetaData,
                        ForeignKey)

__all__ = ['create_user_research_fields_table']

def create_user_research_fields_table(metadata:MetaData):
    """Generates the sqlachemy table structure
    for the `user_research_fields` table.

    Args:
        metadata (MetaData): Metadata object to share
        between tables.

    Returns:
        sqlalchemy.Table: The sqlalchemy table object
    """
    # NOTE There are more details on column details in the model
    # files for this table

    # Creates a table object with the specified columns
    user_research_fields_table = Table(
        "user_research_fields",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
        Column("research_id", Integer, ForeignKey("research_fields.id"), nullable=False),
        Column("role_id", Integer, nullable=False, default=0)
        )
    return user_research_fields_table


