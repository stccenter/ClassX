"""Database module for OriginalImageService class that interacts
with the `original_images` table"""

# Python Standard Library Imports
from datetime import datetime, timezone
import traceback

# Python Third Party Imports
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, select
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, DatabaseError

# Local Library Imports
from ..repository import OriginalImageRepository
from ._base_service import BaseService
from ..model import OriginalImage

__all__ = ["OriginalImageService"]


class OriginalImageService(BaseService):
    """The Original Image Service class for interacting with
    the repository classes.
    """

    def __init__(self, session: Session):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, OriginalImageRepository)
        self.repo: OriginalImageRepository

    def add_image(self, original_image_obj: OriginalImage) -> OriginalImage:
        """Service function for adding a original image to the
        database

        Args:
            original_image_obj (OriginalImage): The OriginalImage class object to add

        Returns:
            OriginalImage: The newly added OriginalImage. Will be None if it
            fails.
        """

        # Adding the original image to database
        return self.add(original_image_obj)

    def get_user_image(
        self, original_image_id: int, user_id: int, default_id: int = None
    ) -> OriginalImage:
        """Retrieves a user original image object by matching the user id
        and image id. Optionally the default id can be passed for the default user.

        Args:
            original_image_id (int): The id of the original image
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            OriginalImage: The original image database object. Will be None if the image
            is not found.
        """

        # Filtering the the database by the user id and id of the image
        return self.repo.get_first_by_user_id_args(
            user_id=user_id, default_id=default_id, id=original_image_id
        )

    def get_user_images(self, user_id: int, default_id: int = None) -> OriginalImage:
        """Retrieves all user original image objects associated with a user
        by matching the user id. Optionally the default id can be passed
        for the default user.

        Args:
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            list(OriginalImage): List of original image objects found. Will be empty if None
            found.
        """

        # Filtering the the database by the user id and id of the image
        return self.repo.get_all_by_user_id_args(user_id=user_id, default_id=default_id)

    def get_user_research_images(
        self, research_field_id: int, user_id: int, default_id: int = None
    ) -> OriginalImage:
        """Retrieves all user original image objects associated with a user & research field
        by matching the user id and research id. Optionally the default id can be passed
        for the default user.

        Args:
            research_field_id (int): The id of the research field to filter by.
            user_id (int): The id of the user retrieving. This is for verification
            purposes.
            default_id (int, optional): The id of the default user to also filter by.
            Defaults to None.

        Returns:
            list(OriginalImage): List of original image objects found. Will be empty if None
            found.
        """

        # Filtering the the database by the user id and the research field id
        return self.repo.get_all_by_user_id_args(
            user_id=user_id, default_id=default_id, research_id=research_field_id
        )

    def check_duplicate_user_image(
        self, user_id: int, original_image_name: str
    ) -> bool:
        """Checks for a duplicate entry under a user image. This is because the names
        will conflict and overwrite eachother.

        Args:
            user_id (int): The id of the associated user.
            original_image_name (str): The original image name to verify.

        Returns:
            bool: Returns True if a duplicate found and False if nothing is found.
        """

        # Retrieving the possible image object.
        original_image_obj = self.repo.get_first_by_user_id_args(
            user_id=user_id, name=original_image_name
        )

        # If nothing is found then there is no duplicate
        if original_image_obj is None:
            return False

        return True

    def update_alias(self, original_image_id: int, new_alias: str) -> OriginalImage:
        """Updates the alias of a given original image.

        Args:
            original_image_id (int): The ID of the original image to update
            new_alias (str): The new metadata map configuration

        Returns:
            OriginalImage: The original image database object with the updated
            alias. Returns None if there is an error.
        """
        # Updating the alias and returning the result
        return self.repo.update_alias_by_id(
            original_image_id=original_image_id, new_alias=new_alias
        )

    # pylint: disable=too-many-arguments

    def search_images(
        self,
        query: str,
        research_field_id: int,
        user_id: int,
        default_id: int = None,
        search_filters: dict = None,
    ):
        """A service function to filter user original images by a name search
        query and metadata filters.

        Args:
            query (str): The filename search query
            research_field_id (int): ID of the research field to filter by
            user_id (int): The ID of the user to filter by.
            default_id (int, optional): Optionally the ID of default user to filter by.
            search_filters (dict): The metadata search filters.

        Returns:
            list(OriginalImage): A list of original image objects after filters
            have been applied.
        """
        # Constructing the base query
        user_ids = [user_id]
        if default_id:
            user_ids.append(default_id)

        stmt = select(OriginalImage).where(
            and_(
                OriginalImage.user_id.in_(user_ids),
                or_(
                    OriginalImage.name.contains(query),
                    OriginalImage.alias.contains(query),
                ),
                OriginalImage.research_id == research_field_id,
            )
        )

        if search_filters:
            for filter_name, filter_value in search_filters.items():
                try:
                    if filter_value["type"] == "minmax":
                        min_value = float(filter_value["data"]["min"])
                        max_value = float(filter_value["data"]["max"])
                        stmt = stmt.where(
                            and_(
                                OriginalImage.metadata[filter_name].astext.cast(float)
                                >= min_value,
                                OriginalImage.metadata[filter_name].astext.cast(float)
                                <= max_value,
                            )
                        )
                    elif filter_value["type"] == "checkbox":
                        check_list = filter_value["data"]
                        if check_list:
                            stmt = stmt.where(
                                OriginalImage.metadata[filter_name].has_any(check_list)
                            )
                    elif filter_value["type"] == "date":
                        start_date = filter_value["data"].get("startDate", "1000-01-01")
                        end_date = filter_value["data"].get(
                            "endDate", datetime.now(timezone.utc).strftime("%Y-%m-%d")
                        )

                        start_date = datetime.strptime(start_date, "%Y-%m-%d")
                        end_date = datetime.strptime(end_date, "%Y-%m-%d")

                        stmt = stmt.where(
                            and_(
                                getattr(OriginalImage, filter_name) >= start_date,
                                getattr(OriginalImage, filter_name) <= end_date,
                            )
                        )
                except (
                    SQLAlchemyError,
                    DatabaseError,
                    DBAPIError,
                    RuntimeError,
                    KeyError,
                    RuntimeWarning,
                ) as error:
                    print(f"Error filtering {filter_name}")
                    traceback.print_tb(error.__traceback__)
                    continue

        try:
            result = self.session.scalars(stmt).all()
            return result
        except Exception as e:
            print(f"Error executing search_images query: {e}")
            return []

    def get_image(self, original_image_id: int) -> OriginalImage:
        """Retrieves a original image object by matching image id.

        Args:
            original_image_id (int): The id of the original image

        Returns:
            OriginalImage: The original image database object. Will be None if the image
            is not found.
        """

        # Filtering the database by id of the image
        return self.repo.get_by_id(object_id=original_image_id)

    def get_images(self, original_image_id_list: list[int]) -> list[OriginalImage]:
        """Retrieves a list of original image objects by matching image ids.

        Args:
            original_image_id_list (list[int]): The ids of the original images

        Returns:
            list(OriginalImage): List of original image objects found. Will be empty if None
            found.
        """

        # Filtering the database by ids of the images
        return self.repo.get_by_ids(object_id_list=original_image_id_list)
