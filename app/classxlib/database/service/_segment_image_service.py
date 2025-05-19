"""Database module for SegmentImageService class that interacts
with the `segment_images` table"""

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import SegmentImageRepository
from ._base_service import BaseService
from ..model import SegmentImage

__all__ = ['SegmentImageService']

class SegmentImageService(BaseService):
    """The Segment Image Service class for interacting with
    the repository classes.
    """
    def __init__(self, session:Session):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, SegmentImageRepository)
        self.repo : SegmentImageRepository

    def add_image(self,segment_image_obj:SegmentImage) -> SegmentImage:
        """Service function for adding a segment image to the
        database

        Args:
            segment_image_obj (SegmentImage): The SegmentImage class object to add

        Returns:
            SegmentImage: The newly added SegmentImage. Will be None if it
            fails.
        """

        # Adding the segment image to database
        return self.add(segment_image_obj)

    def get_user_image(self,
                       segment_image_id:int,
                       user_id:int,
                       default_id:int=None) -> SegmentImage:
        """Retrieves a user segment image object by matching the user id
        and image id. Optionally the default id can be passed for the default user.

        Args:
            segment_image_id (int): The id of the segment image
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            SegmentImage: The segment image database object. Will be None if the image
            is not found.
        """

        # Filtering the the database by the user id and id of the image
        return self.repo.get_first_by_user_id_args(user_id=user_id,
                                                   default_id=default_id,
                                                   id=segment_image_id)

    def get_user_images_from_parent(self,
                                    crop_image_id:int,
                                    user_id:int,
                                    default_id:int=None) -> SegmentImage:
        """Retrieves all user segment image objects associated with a crop image and a user
        by matching the user id & crop image id. Optionally the default id can be passed
        for the default user.

        Args:
            crop_image_id (int): The id of the crop image to find crop images of
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            list(SegmentImage): List of segment image objects found. Will be empty if None
            found.
        """

        # Filtering the the database by the user id and id of the image
        return self.repo.get_all_by_user_id_args(user_id=user_id,
                                                 default_id=default_id,
                                                 crop_image_id=crop_image_id)

    def get_image(self,segment_image_id:int)-> SegmentImage:
        """Retrieves a segment image object by matching image id.

        Args:
            segment_image_id (int): The id of the segment image

        Returns:
            SegmentImage: The segment image database object. Will be None if the image
            is not found.
        """

        # Filtering the database by id of the image
        return self.repo.get_by_id(object_id=segment_image_id)

    def get_images(self,segment_image_id_list:list[int])-> list[SegmentImage]:
        """Retrieves a list of segment image objects by matching image ids.

        Args:
            segment_image_id (list[int]): The ids of the segment images

        Returns:
            list(SegmentImage): List of segment image objects found. Will be empty if None
            found.
        """

        # Filtering the database by ids of the images
        return self.repo.get_by_ids(object_id_list=segment_image_id_list)

    def get_images_from_parent_image(self,crop_image_id:int) -> SegmentImage:
        """Retrieves all segment image objects associated with a crop image
        by matching the crop image id.

        Args:
            crop_image_id (int): The id of the crop image to find segment images of

        Returns:
            list(SegmentImage): List of segment image objects found. Will be empty if None
            found.
        """

        # Filtering the the database by the crop image id
        return self.repo.get_all_by_args(crop_image_id=crop_image_id)

    def remove_image(self, segment_image_obj:SegmentImage) -> bool:
        """Removes a segment image from the database by passing the
        database object.

        Args:
            segment_image_obj (SegmentImage): The segment image object
            to reference for deletion

        Returns:
            bool: Returns True if successful and False if there
            are errors or the segment image is not found.
        """
        # Verifying the object
        segment_image_obj = self.repo.get_by_id(segment_image_obj.id)

        # Verifying the crop image was found
        if segment_image_obj is None:
            return False

        
        # Deleting the crop image by it's id
        return self.repo.delete_row_by_id(segment_image_obj.id)