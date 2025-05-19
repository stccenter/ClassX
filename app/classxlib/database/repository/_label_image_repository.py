"""Database module for defining the LabelImageRepository Class"""
# Python Standard Library Imports
from datetime import datetime

# Python Third Party Imports
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

# Local Library Imports
from ..model import LabelImage
from ._base_repository import BaseRepository

__all__ = ['LabelImageRepository']


class LabelImageRepository(BaseRepository):
    """The class for interacting/querying the `label_images` sql table.
        Args:
            session(sqlalchemy.orm.Session): The database session object
            to use for querying and commiting changes.
    """
    def __init__(self, session:Session):
        # Initializes the base repository class
        super().__init__(session=session,
                         model=LabelImage,
                         table_name="label_images")

    def delete_by_training_id_segment_id(self,
                                         training_file_id:int,
                                         segment_image_id:int):
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

        # Filtering by the crop image id then deleting
        self.session.query(LabelImage).\
            filter(and_(LabelImage.training_file_id == training_file_id,
                        LabelImage.segment_image_id == segment_image_id)).delete()

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return False

        return True

    def update_last_modifed_by_training_id_segment_id(self,
                                                      training_file_id:int,
                                                      segment_image_id:int,
                                                      new_date:datetime):
        """Updates the label image save_time from the database by matching the
        segment image id and the training file id.

        Args:
            training_file_id (int): The ID of the training file this label
            image belongs to.
            segment_image_id (int): The ID of the segment image the label image
            was created from.
            new_date (datetime): The new datetime to input.

        Returns:
            LabelImage : The label image database object with the updated
            save time. Returns None if there is an error.
        """

        label_image_obj = self.session.query(LabelImage).\
            filter(and_(LabelImage.training_file_id == training_file_id,
                        LabelImage.segment_image_id == segment_image_id)).\
                            update({'last_modified': new_date})

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return None

        return label_image_obj

    def get_by_training_id_latest(self, training_file_id:int):
        """Gets the latest label image of a training file.

        Args:
            training_file_id (int): The ID of the training file
            this label image belongs to.

        Returns:
            DatabaseModel: The database row represented as a
            python dataclass
        """
        # Filtering by the original image id
        label_image_obj = self.session.query(self.model).\
            filter(LabelImage.training_file_id == training_file_id).\
                order_by(LabelImage.last_modified.desc()).first()

        return label_image_obj
