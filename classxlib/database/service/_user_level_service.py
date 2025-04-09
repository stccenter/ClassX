"""Database module for UserService class that interacts
with the `user_levels` table"""

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import UserLevelRepository
from ._base_service import BaseService
from ..model import UserLevel


class UserLevelService(BaseService):
    """The User Service class for interacting with
    the repository classes.
    """

    def __init__(self, session: Session):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, UserLevelRepository)
        self.repo: UserLevelRepository

    def add_level(self, user_level_obj: UserLevel) -> UserLevel:
        """Service function for adding a user level to the
        database

        Args:
            user_level_obj (UserLevel): The UserLevel class object to add

        Returns:
            user_level_obj: The newly added UserLevel. Will be None if it
            fails.
        """
        # Adding the user level to database
        return self.add(user_level_obj)

    def get_by_id(self, level_id: int) -> UserLevel:
        """Retrieves a user level from the database
        by matching it's level id

        Args:
            level_id (int): The ID of the associated user level.

        Returns:
            UserLevel: The database user level object. Returns None if not
            found.
        """
        # Retrieving the user level and returning it
        return self.repo.get_by_id(object_id=level_id)

    def get_by_name(self, level_name: str) -> UserLevel:
        """Retrieves a user level from the database
        by matching it's level name

        Args:
            level_name (str): The name of the associated user level.

        Returns:
            UserLevel: The database user level object. Returns None if not
            found.
        """

        # Retrieving the user level and returning it
        return self.repo.get_by_name(user_level_name=level_name)

    def update_level_permissions(
        self, user_level_id: int, new_permissions: dict
    ) -> UserLevel:
        """Updates the permissions of a given user level

        Args:
            user_level_id (int): The ID of the user level to update
            new_permissions (dict): The new permissions configuration

        Returns:
            UserLevel: The user level database object with the updated
            configurations. Returns None if there is an error.
        """
        return self.repo.update_permission_by_id(
            user_level_id=user_level_id, new_permissions=new_permissions
        )

    def remove_level(self, user_level_obj: UserLevel) -> bool:
        """Removes a user level by passing the object and removing it

        Args:
            user_level_obj (UserLevel): The user level object to reference
            for removal.

        Returns:
            bool: Returns True if successful and False if there
            are errors or the user is not found.
        """

        # Deleting the user level from the database
        return self.repo.delete_row_by_id(user_level_obj.id)
