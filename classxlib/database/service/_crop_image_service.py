"""Database module for CropImageService class that interacts
with the `crop_images` table"""

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import CropImageRepository
from ._base_service import BaseService
from ..model import CropImage

__all__ = ["CropImageService"]


class CropImageService(BaseService):
    """The Crop Image Service class for interacting with
    the repository classes.
    """

    def __init__(self, session: Session):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, CropImageRepository)
        self.repo: CropImageRepository

    def add_image(self, crop_image_obj: CropImage) -> CropImage:
        """Service function for adding a crop image to the
        database

        Args:
            crop_image_obj (CropImage): The CropImage class object to add

        Returns:
            CropImage: The newly added CropImage. Will be None if it
            fails.
        """

        # Adding the crop image to database
        return self.add(crop_image_obj)

    def get_user_image(
        self, crop_image_id: int, user_id: int, default_id: int = None
    ) -> CropImage:
        """Retrieves a user crop image object by matching the user id
        and image id. Optionally the default id can be passed for the default user.

        Args:
            crop_image_id (int): The id of the crop image
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            CropImage: The crop image database object. Will be None if the image
            is not found.
        """

        # Filtering the the database by the user id and id of the image
        return self.repo.get_first_by_user_id_args(
            user_id=user_id, default_id=default_id, id=crop_image_id
        )

    def get_user_images(
        self, user_id: int, crop_type: str = None, default_id: int = None
    ) -> CropImage:
        """Retrieves all user crop image objects associated with a user
        by matching the user id. Optionally the default id can be passed
        for the default user.

        Args:
            crop_type (str, optional): The crop type of the image to filter by. Can be
            `'man'` or `'auto'`. If None will ignore the argument.
            Defaults to None.
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            list(CropImage): List of crop image objects found. Will be empty if None
            found.
        """
        if crop_type is None:
            # Filtering the the database by the user id and id of the image
            return self.repo.get_all_by_user_id_args(
                user_id=user_id, default_id=default_id
            )
        return self.repo.get_all_by_user_id_args(
            user_id=user_id, default_id=default_id, crop_type=crop_type
        )

    def get_user_research_images(
        self,
        research_field_id: int,
        user_id: int,
        crop_type: str = None,
        default_id: int = None,
    ) -> CropImage:
        """Retrieves all user crop image objects associated with a user & research field
        by matching the user id and research id. Optionally the default id can be passed
        for the default user.

        Args:
            research_field_id (int): The id of the research field to filter by.
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            crop_type (str, optional): The crop type of the image to filter by. Can be
            `'man'` or `'auto'`. If None will ignore the argument.
            Defaults to None.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            list(CropImage): List of crop image objects found. Will be empty if None
            found.
        """
        if crop_type is None:
            # Filtering the the database by the user id and id of the image
            return self.repo.get_all_by_user_id_args(
                user_id=user_id, default_id=default_id, research_id=research_field_id
            )
        return self.repo.get_all_by_user_id_args(
            user_id=user_id,
            default_id=default_id,
            research_id=research_field_id,
            crop_type=crop_type,
        )

    def get_user_image_from_grid(
        self,
        original_image_id: int,
        grid_point: tuple,
        user_id: int,
        default_id: int = None,
    ) -> CropImage:
        """Retrieves a user crop image object that was auto-cropped by matching
        the user id, grid position and original image id. Optionally the default id
        can be passed for the default user.

        Args:
            original_image_id (int): The id of the parent original image.
            grid_point (tuple): The x-y coordinate position the image was cropped at.
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            CropImage: The crop image database object. Will be None if the image
            is not found.
        """

        # Filtering the the database by the user id and id of the image
        return self.repo.get_first_by_user_id_args(
            user_id=user_id,
            default_id=default_id,
            original_image_id=original_image_id,
            width=grid_point[0],
            height=grid_point[1],
            crop_type="auto",
        )

    def get_user_images_from_parent(
        self,
        original_image_id: int,
        user_id: int,
        crop_type: str = None,
        default_id: int = None,
    ) -> CropImage:
        """Retrieves all user crop image objects associated with a original image and a user
        by matching the user id & original image id. Optionally the default id can be passed
        for the default user.

        Args:
            original_image_id (int): The id of the original image to find crop images of
            crop_type (str, optional): The crop type of the image to filter by. Can be
            `'man'` or `'auto'`. If None will ignore the argument.
            Defaults to None.
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            list(CropImage): List of crop image objects found. Will be empty if None
            found.
        """
        if crop_type is None:
            # Filtering the the database by the user id and id of the image
            return self.repo.get_all_by_user_id_args(
                user_id=user_id,
                default_id=default_id,
                original_image_id=original_image_id,
            )
        return self.repo.get_all_by_user_id_args(
            user_id=user_id,
            default_id=default_id,
            original_image_id=original_image_id,
            crop_type=crop_type,
        )

    def remove_image(self, crop_image_obj: CropImage) -> bool:
        """Removes a crop image from the database by passing the
        database object.

        Args:
            crop_image_obj (CropImage): The crop image object
            to reference for deletion

        Returns:
            bool: Returns True if successful and False if there
            are errors or the crop image is not found.
        """
        # Verifying the object
        crop_image_obj = self.repo.get_by_id(crop_image_obj.id)

        # Verifying the crop image was found
        if crop_image_obj is None:
            return False

        # Deleting the crop image by it's id
        return self.repo.delete_row_by_id(crop_image_obj.id)

    def get_image(self, crop_image_id: int) -> CropImage:
        """Retrieves a crop image object by matching image id.

        Args:
            crop_image_id (int): The id of the crop image

        Returns:
            CropImage: The crop image database object. Will be None if the image
            is not found.
        """

        # Filtering the database by id of the image
        return self.repo.get_by_id(object_id=crop_image_id)

    def get_images(self, crop_image_id_list: list[int]) -> list[CropImage]:
        """Retrieves a list of crop image objects by matching image ids.

        Args:
            crop_image_id (list[int]): The ids of the crop images

        Returns:
            list(CropImage): List of crop image objects found. Will be empty if None
            found.
        """

        # Filtering the database by ids of the images
        return self.repo.get_by_ids(object_id_list=crop_image_id_list)
