"""Database module for TrainingFileService class that interacts
with the `training_files` table"""

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import TrainingFileRepository
from ._base_service import BaseService
from ..model import TrainingFile

__all__ = ['TrainingFileService']

class TrainingFileService(BaseService):
    """The Training File Service class for interacting with
    the repository classes.
    """
    def __init__(self, session:Session):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, TrainingFileRepository)
        self.repo : TrainingFileRepository

    def add_file(self,training_file_obj:TrainingFile) -> TrainingFile:
        """Service function for adding a training file to the
        database

        Args:
            training_file_obj (TrainingFile): The TrainingFile class
            object to add

        Returns:
            TrainingFile: The newly added TrainingFile. Will be None
            if it fails.
        """
        # Adding the training file to database
        return self.add(training_file_obj)

    def get_file(self,training_file_id:int)-> TrainingFile:
        """Retrieves a training file object by matching file id.

        Args:
            training_file_id (int): The id of the training file

        Returns:
            TrainingFile: The training file database object. Will be None if the file
            is not found.
        """

        # Filtering the database by id of the training file
        return self.repo.get_by_id(object_id=training_file_id)

    def get_user_file(self,training_file_id:int,
                      user_id:int,
                      default_id:int=None)-> TrainingFile:
        """Retrieves a training file object by matching file id, user id, and
        optionally the default id.

        Args:
            training_file_id (int): The id of the training file
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            TrainingFile: The training file database object. Will be None if the file
            is not found.
        """

        # Filtering the database by id & user id of the training file
        return self.repo.get_first_by_user_id_args(user_id=user_id,
                                                   default_id=default_id,
                                                   id=training_file_id)

    def get_user_research_files(self,
                                research_field_id:int,
                                user_id:int,
                                default_id:int=None) -> TrainingFile:
        """Retrieves all user training file objects associated with a user & research field
        by matching the user id and research id. Optionally the default id can be passed
        for the default user.

        Args:
            research_field_id (int): The id of the research field to filter by.
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            list(TrainingFile): List of training file objects found. Will be empty if None
            found.
        """

        # Filtering the the database by the user id and the research field id
        return self.repo.get_all_by_user_id_args(user_id=user_id,
                                                 default_id=default_id,
                                                 research_id=research_field_id)

    def get_user_file_by_name(self,
                              training_file_name:str,
                              user_id:int,
                              default_id:int=None) -> TrainingFile:
        """Retrieves a user training file object by matching the user id
        and file name. Optionally the default id can be passed for the default user.

        Args:
            training_file_name (str): The name of the training file
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            TrainingFile: The training file database object. Will be None if the image
            is not found.
        """

        # Filtering the the database by the user id and name of the file
        return self.repo.get_first_by_user_id_args(user_id=user_id,
                                                   default_id=default_id,
                                                   file_name=training_file_name)

    def update_label_count(self,
                           training_file_id:int,
                           new_label_count:dict) -> TrainingFile:
        """Updates the label count of a given training file

        Args:
            training_file_id (int): The ID of the training file to update
            new_label_count (dict): The new label count

        Returns:
            TrainingFile: The training file database object with the updated
            label count. Returns None if there is an error.
        """

        # Updating the label count of the training file and returning the new object
        return self.repo.update_label_count_by_id(training_file_id=training_file_id,
                                                  new_label_count=new_label_count)
