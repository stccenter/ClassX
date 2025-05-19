"""Database module for defining the ResearchFieldRepository Class"""

# Python Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..model import ResearchField
from ._base_repository import BaseRepository

__all__ = ['ResearchFieldRepository']

class ResearchFieldRepository(BaseRepository):
    """The class for interacting/querying the `research_fields` sql table.
        Args:
            session(sqlalchemy.orm.Session): The database session object
            to use for querying and commiting changes.
    """
    def __init__(self, session:Session):
        # Initializes the base repository class
        super().__init__(session=session,
                         model=ResearchField,
                         table_name="research_fields")

    def get_by_visibility(self, research_field_visibility:int):
        """Gets a list of research fields by their visibility level

        Args:
            research_field_visibility (int): The visibility ID associated with a
            research field

        Returns:
            list(ResearchField): The list of research field database objects, Returns
            an empty list if none found.
        """

        # Filtering by the research field id
        research_field_obj_list = self.session.query(ResearchField).\
            filter(ResearchField.visibility == research_field_visibility).all()

        return research_field_obj_list

    def get_by_name(self, research_field_name:str):
        """Gets a research field by their name

        Args:
            research_field_name (str): The name associated with a research field

        Returns:
            ResearchField: The research field database object, Returns None if not found.
        """

        # Filtering by the research field name
        research_field_obj = self.session.query(ResearchField).\
            filter(ResearchField.name == research_field_name).first()

        return research_field_obj

    def update_label_map_by_id(self, research_field_id:int,
                                new_label_map:dict):
        """Updates the label map of a research_field

        Args:
            research_field_id (int): The ID of the research field to update.
            new_label_map (dict): The new label map configurations.

        Returns:
            ResearchField: The research field database object with the updated
            configurations. Returns None if there is an error.
        """

        # Filtering by the research field id
        research_field_obj = self.session.query(ResearchField).\
            filter(ResearchField.id == research_field_id).first()

        # Updating the label_map
        research_field_id.label_map = new_label_map

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return None

        return research_field_obj

    def update_metadata_map_by_id(self, research_field_id:int,
                                new_metadata_map:dict):
        """Updates the metadata map of a research_field

        Args:
            research_field_id (int): The ID of the research field to update.
            new_metadata_map (dict): The new metadata map configurations.

        Returns:
            ResearchField: The research field database object with the updated
            configurations. Returns None if there is an error.
        """

        # Filtering by the research field id
        research_field_obj = self.session.query(ResearchField).\
            filter(ResearchField.id == research_field_id).first()

        # Updating the metadata_map
        research_field_id.metadata_map = new_metadata_map

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return None

        return research_field_obj

    def update_protocols_by_id(self, research_field_id:int,
                                new_protocols:dict):
        """Updates the protocols of a research_field

        Args:
            research_field_id (int): The ID of the research field to update.
            new_protocols (dict): The new protocols configurations.

        Returns:
            ResearchField: The research field database object with the updated
            configurations. Returns None if there is an error.
        """

        # Filtering by the research field id
        research_field_obj = self.session.query(ResearchField).\
            filter(ResearchField.id == research_field_id).first()

        # Updating the metadata_map
        research_field_obj.protocols = new_protocols

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return None

        return research_field_obj

    def update_field_data_by_id(self, research_field_id:int,
                                new_field_data:dict):
        """Updates the field data of a research_field

        Args:
            research_field_id (int): The ID of the research field to update.
            new_field_data (dict): The new field data configurations.

        Returns:
            ResearchField: The research field database object with the updated
            configurations. Returns None if there is an error.
        """

        # Filtering by the research field id
        research_field_obj = self.session.query(ResearchField).\
            filter(ResearchField.id == research_field_id).first()

        # Updating the field data
        research_field_id.field_data = new_field_data

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return None

        return research_field_obj
