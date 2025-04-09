"""Database module for defining the TrainingFileRepository Class"""

# Python Third Party Imports
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update

# Local Library Imports
from ..model import TrainingFile
from ._base_repository import BaseRepository

__all__ = ["TrainingFileRepository"]


class TrainingFileRepository(BaseRepository):
    """The class for interacting/querying the `training_files` sql table.
    Args:
        session(sqlalchemy.orm.Session): The database session object
        to use for querying and committing changes.
    """

    def __init__(self, session: Session):
        # Initializes the base repository class
        super().__init__(
            session=session, model=TrainingFile, table_name="training_files"
        )

    def update_label_count_by_id(
        self, training_file_id: int, new_label_count: dict
    ) -> Optional[TrainingFile]:
        """Updates the label count of a given training file

        Args:
            training_file_id (int): The ID of the training file to update
            new_label_count (dict): The new label count.

        Returns:
            TrainingFile: The training file database object with the updated
            label count. Returns None if there is an error.
        """
        stmt = (
            update(TrainingFile)
            .where(TrainingFile.id == training_file_id)
            .values(label_count=new_label_count)
            .returning(TrainingFile)
        )

        try:
            result = self.session.execute(stmt).scalar_one_or_none()
            self.commit_changes()
            return result
        except Exception as e:
            print(
                f"Error updating label count for training file with id {training_file_id}"
            )
            print(e)
            return None
