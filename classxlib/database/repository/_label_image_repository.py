"""Database module for defining the LabelImageRepository Class"""

# Python Standard Library Imports
from typing import Optional
from datetime import datetime

# Python Third Party Imports
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from sqlalchemy.sql import and_

# Local Library Imports
from ..model import LabelImage
from ._base_repository import BaseRepository

__all__ = ["LabelImageRepository"]


class LabelImageRepository(BaseRepository):
    """The class for interacting/querying the `label_images` sql table.
    Args:
        session(sqlalchemy.orm.Session): The database session object
        to use for querying and commiting changes.
    """

    def __init__(self, session: Session):
        # Initializes the base repository class
        super().__init__(session=session, model=LabelImage, table_name="label_images")

    def delete_by_training_id_segment_id(
        self, training_file_id: int, segment_image_id: int
    ) -> bool:
        """Deletes a label image from the database by matching the
        segment image id and the training file id.

        Args:
            training_file_id (int): The ID of the training file this label
            image belongs to.
            segment_image_id (int): The ID of the segment image the label image
            was created from.

        Returns:
            bool : Returns True or False indicating whether the operation was
            successful
        """
        stmt = delete(LabelImage).where(
            and_(
                LabelImage.training_file_id == training_file_id,
                LabelImage.segment_image_id == segment_image_id,
            )
        )

        try:
            self.session.execute(stmt)
            return self.commit_changes()
        except Exception as e:
            print(
                f"Error deleting label image with training_file_id {training_file_id} and segment_image_id {segment_image_id}"
            )
            print(e)
            return False

    def update_last_modified_by_training_id_segment_id(
        self, training_file_id: int, segment_image_id: int, new_date: datetime
    ) -> Optional[LabelImage]:
        """Updates the label image save_time from the database by matching the
        segment image id and the training file id.

        Args:
            training_file_id (int): The ID of the training file this label
            image belongs to.
            segment_image_id (int): The ID of the segment image the label image
            was created from.
            new_date (datetime): The new datetime to input.

        Returns:
            Optional[LabelImage]: The label image database object with the updated
            save time. Returns None if there is an error.
        """
        stmt = (
            update(LabelImage)
            .where(
                and_(
                    LabelImage.training_file_id == training_file_id,
                    LabelImage.segment_image_id == segment_image_id,
                )
            )
            .values(last_modified=new_date)
            .returning(LabelImage)
        )

        try:
            result = self.session.scalars(stmt).first()
            self.commit_changes()
            return result
        except Exception as e:
            print(
                f"Error updating last_modified for training_file_id {training_file_id} and segment_image_id {segment_image_id}"
            )
            print(e)
            return None

    def get_by_training_id_latest(self, training_file_id: int) -> Optional[LabelImage]:
        """Gets the latest label image of a training file.

        Args:
            training_file_id (int): The ID of the training file
            this label image belongs to.

        Returns:
            Optional[LabelImage]: The database row represented as a
            python dataclass or None if not found.
        """
        stmt = (
            select(LabelImage)
            .where(LabelImage.training_file_id == training_file_id)
            .order_by(LabelImage.last_modified.desc())
            .limit(1)
        )

        try:
            result = self.session.scalars(stmt).first()
            return result
        except Exception as e:
            print(
                f"Error fetching latest label image for training_file_id {training_file_id}"
            )
            print(e)
            return None
