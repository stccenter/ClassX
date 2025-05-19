"""Module for generating the research fields table"""

# Python Third Party Imports
from sqlalchemy import (Table, Column,
                        Integer, JSON,
                        ForeignKey, MetaData,
                        DateTime, String)

__all__ = ['create_research_field_table']

def create_research_field_table(metadata:MetaData):
    """Generates the sqlachemy table structure
    for the `research_fields` table.

    Args:
        metadata (MetaData): Metadata object to share
        between tables.

    Returns:
        sqlalchemy.Table: The sqlalchemy table object
    """
    # NOTE There are more details on column details in the model
    # files for this table

    # Creates a table object with the specified columns
    research_field_table = Table(
        "research_fields",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String(50), nullable=False),
        Column("user_id", Integer,ForeignKey("users.id"), nullable=True),
        Column("visibility", Integer, nullable=False),
        Column("last_modified_date",DateTime),
        Column("label_map", JSON, nullable=False),
        Column("metadata_map", JSON, nullable=False),
        Column("protocols", JSON, nullable=False),
        Column("field_data", JSON, nullable=False),
        )
    return research_field_table


