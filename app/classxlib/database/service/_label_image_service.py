"""Database module for LabelImageService class that interacts
with the `label_images` table"""

# Python Standard Library Imports
from datetime import datetime

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import LabelImageRepository
from ._base_service import BaseService
from ..model import LabelImage

__all__ = ['LabelImageService']

class LabelImageService(BaseService):
    """The Label Image Service class for interacting with
    the repository classes.
    """

    def __init__(self, session:Session):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, LabelImageRepository)
        self.repo : LabelImageRepository

    def add_image(self,label_image_obj:LabelImage) -> LabelImage:
        """Service function for adding a label image to the
        database

        Args:
            label_image_obj (LabelImage): The LabelImage class object to add

        Returns:
            LabelImage: The newly added LabelImage. Will be None if it
            fails.
        """

        # Adding the label image to database
        return self.add(label_image_obj)

    def remove_image(self, label_image_obj:LabelImage) -> bool:
        """Removes a label image from the database by passing the
        database object.

        Args:
            label_image_obj (LabelImage): The label image object
            to reference for deletion

        Returns:
            bool: Returns True if successful and False if there
            are errors or the crop image is not found.
        """
        # Verifying the object
        label_image_obj = self.repo.get_by_id(label_image_obj.id)

        # Verifying the label image was found
        if label_image_obj is None:
            return False

        # Deleting the label image by it's id
        return self.repo.delete_row_by_id(label_image_obj.id)


    def get_images_from_parent_file(self,training_file_id:int) -> LabelImage:
        """Retrieves all label image objects associated with a training file
        by matching the training file id.

        Args:
            training_file_id (int): The id of the training file to find label images of

        Returns:
            list(LabelImage): List of label image objects found. Will be empty if None
            found.
        """

        # Filtering the the database by the training file id
        return self.repo.get_all_by_args(training_file_id=training_file_id)

    def get_images_from_parent_image(self,segment_image_id:int) -> list[LabelImage]:
        """Retrieves all label image objects associated with a segment image
        by matching the segment image id.

        Args:
            segment_image_id (int): The id of the segment image to find label images of

        Returns:
            list(LabelImage): List of label image objects found. Will be empty if None
            found.
        """

        # Filtering the the database by the segment image id
        return self.repo.get_all_by_args(segment_image_id=segment_image_id)

    def get_image_from_parents(self,
                               segment_image_id:int,
                               training_file_id:int) -> LabelImage:
        """Gets a label image object by matching both the segment image id and
        training file id

        Args:
            segment_image_id (int): The id of the segment image
            training_file_id (int): The id of the training file

        Returns:
            LabelImage: The label image database object. Will be None if it
            fails or None found.
        """

        # Filtering the the database by the segment image id and training file id
        return self.repo.get_first_by_args(segment_image_id=segment_image_id,
                                           training_file_id=training_file_id)

    def update_last_modified(self,
                             segment_image_id:int,
                             training_file_id:int,
                             new_date:datetime) -> LabelImage:
        """Updates the last_modifed date of a given label image

        Args:
            segment_image_id (int): The id of the segment image
            training_file_id (int): The id of the training file
            new_date (datetime): The new modified date

        Returns:
            LabelImage: The label image database object with the updated
            date. Returns None if there is an error.
        """
        # Updating the last modifed and returning the new object
        return self.repo.update_last_modifed_by_training_id_segment_id(\
            training_file_id=training_file_id,
            segment_image_id=segment_image_id,
            new_date=new_date)

    def get_last_modified_from_parent_file(self, training_file_id:int):
        """Retrieves the latest modified label image from a training file.

        Args:
            training_file_id (int): The id of the training file to find label images

        Returns:
            LabelImage: The label image database object. Will be None if it
            fails or None found.
        """

        # Filtering the the database by the training file id
        return self.repo.get_by_training_id_latest(training_file_id=training_file_id)
