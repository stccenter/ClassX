"""Database module for ResearchFieldService class that interacts
with the `research_fields` table"""

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import ResearchFieldRepository
from ._base_service import BaseService
from ..model import ResearchField

__all__ = ["ResearchFieldService"]


class ResearchFieldService(BaseService):
    """The Research Field Service class for interacting with
    the repository classes.
    """

    def __init__(self, session: Session):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, ResearchFieldRepository)
        self.repo: ResearchFieldRepository

    def add_field(self, research_field_obj: ResearchField) -> ResearchField:
        """Service function for adding a research field to the
        database

        Args:
            research_field_obj (ResearchField): The ResearchField class object to add

        Returns:
            ResearchField: The newly added ResearchField. Will be None if it
            fails.
        """

        # Adding the original image to database
        return self.add(research_field_obj)

    def get_default_fields(self) -> list:
        """Gets all the default Research Fields stored in the database

        Returns:
            list(ResearchFields): List of ResearchField objects that are
            all listed as default in the database
        """
        # Getting all the default research fields
        # Visibility 1 means it's a default domain.
        return self.repo.get_all_by_args(visibility=1)

    def get_default_field_by_name(self, research_field_name: str) -> ResearchField:
        """Gets a default research field by name.

        Args:
            research_field_name (str): The name to filter by.
        Returns:
            ResearchField: The database research field object.
            Returns None if not found.
        """
        # Getting all the default research fields
        # Visibility 1 means it's a default domain.
        return self.repo.get_first_by_args(visibility=1, name=research_field_name)

    def get_by_id(self, research_id: int) -> ResearchField:
        """Retrieves a research field from the database
        by matching it's research id

        Args:
            research_id (int): The ID of the associated research field.

        Returns:
            ResearchField: The database research field object.
            Returns None if not found.
        """
        # Retrieving the research field and returning it
        return self.repo.get_by_id(object_id=research_id)

    def get_by_ids(self, research_id_list: list) -> list:
        """Retrieves a list of research fields from the database
        by matching their research ids

        Args:
            research_id_list (list(int)): The IDs of the associated
            research fields.

        Returns:
            list(ResearchField): List of ResearchField objects that are
            are found will be empty if none found.
        """

        # Retrieving the research field and returning it
        return self.repo.get_by_ids(object_id_list=research_id_list)

    def update_label_map(self, research_id: int, new_label_map: dict) -> ResearchField:
        """Updates the label map of a given research field.

        Args:
            research_id (int): The ID of the research field to update
            new_label_map (dict): The new label map configuration

        Returns:
            ResearchField: The research field database object with the updated
            configurations. Returns None if there is an error.
        """
        # Updating the label map and returning the result
        return self.repo.update_label_map_by_id(
            research_field_id=research_id, new_label_map=new_label_map
        )

    def update_field_data(
        self, research_id: int, new_field_data: dict
    ) -> ResearchField:
        """Updates the field data of a given research field.

        Args:
            research_id (int): The ID of the research field to update
            new_field_data (dict): The new field data configuration

        Returns:
            ResearchField: The research field database object with the updated
            configurations. Returns None if there is an error.
        """
        # Updating the field data and returning the result
        return self.repo.update_field_data_by_id(
            research_field_id=research_id, new_field_data=new_field_data
        )

    def update_metadata_map(
        self, research_id: int, new_metadata_map: dict
    ) -> ResearchField:
        """Updates the metadata map of a given research field.

        Args:
            research_id (int): The ID of the research field to update
            new_metadata_map (dict): The new metadata map configuration

        Returns:
            ResearchField: The research field database object with the updated
            configurations. Returns None if there is an error.
        """
        # Updating the metadata map and returning the result
        return self.repo.update_metadata_map_by_id(
            research_field_id=research_id, new_metadata_map=new_metadata_map
        )

    def update_protocols(self, research_id: int, new_protocols: dict) -> ResearchField:
        """Updates the upload protocols of a given research field.

        Args:
            research_id (int): The ID of the research field to update
            new_protocols (dict): The new upload protocols configuration

        Returns:
            ResearchField: The research field database object with the updated
            configurations. Returns None if there is an error.
        """
        # Updating the protocols and returning the result
        return self.repo.update_protocols_by_id(
            research_field_id=research_id, new_protocols=new_protocols
        )
