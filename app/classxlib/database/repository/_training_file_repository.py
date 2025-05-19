"""Database module for defining the TrainingFileRepository Class"""

# Python Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..model import TrainingFile
from ._base_repository import BaseRepository

__all__ = ['TrainingFileRepository']

class TrainingFileRepository(BaseRepository):
    """The class for interacting/querying the `training_files` sql table.
        Args:
            session(sqlalchemy.orm.Session): The database session object
            to use for querying and commiting changes.
    """

    def __init__(self, session:Session):
        # Initializes the base repository class
        super().__init__(session=session,
                         model=TrainingFile,
                         table_name="training_files")

    def update_label_count_by_id(self,
                                 training_file_id:int,
                                 new_label_count:dict):
        """Updates the label count of a given training file

        Args:
            training_file_id (int): The ID of the training file to update
            new_label_count (dict): The new label count.

        Returns:
            TrainingFile: The training file database object with the updated
            label count. Returns None if there is an error.
        """

        # Filtering the user level by id
        training_file_obj = self.session.query(TrainingFile).\
            filter(TrainingFile.id == training_file_id).first()

        # Overwriting the current permissions configuration
        training_file_obj.label_count = new_label_count

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return None

        return training_file_obj
