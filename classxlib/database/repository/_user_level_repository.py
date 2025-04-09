"""Database module for defining the UserLevelRepository Class"""

# Python Standard Library Imports
from typing import Any, Dict, Optional

# Python Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..model import UserLevel
from ._base_repository import BaseRepository

__all__ = ["UserLevelRepository"]


class UserLevelRepository(BaseRepository):
    """The class for interacting/querying the `user_levels` SQL table.

    Args:
        session (Session): The database session object
            to use for querying and committing changes.
    """

    def __init__(self, session: Session):
        # Initializes the base repository class
        super().__init__(session=session, model=UserLevel, table_name="user_levels")

    def get_by_name(self, user_level_name: str) -> Optional[UserLevel]:
        """Gets a user level by its name.

        Args:
            user_level_name (str): The name of the user level.

        Returns:
            Optional[UserLevel]: The user level database object, or None if not found.
        """
        return self.get_first_by_args(name=user_level_name)

    def update_permission_by_id(
        self, user_level_id: int, new_permissions: Dict[str, Any]
    ) -> Optional[UserLevel]:
        """Updates the permissions of a given user level.

        Args:
            user_level_id (int): The ID of the user level to update.
            new_permissions (Dict[str, Any]): The new permissions configuration.

        Returns:
            Optional[UserLevel]: The user level database object with the updated
                configurations. Returns None if there is an error.
        """
        user_level_obj = self.get_by_id(user_level_id)
        if not user_level_obj:
            return None

        user_level_obj.permissions = new_permissions
        if not self.commit_changes():
            return None

        return user_level_obj

    def create_user_level(
        self, name: str, permissions: Dict[str, Any]
    ) -> Optional[UserLevel]:
        """Creates a new user level.

        Args:
            name (str): The name of the user level.
            permissions (Dict[str, Any]): The permissions configuration.

        Returns:
            Optional[UserLevel]: The created user level object or None if creation failed.
        """
        new_user_level = UserLevel(name=name, permissions=permissions)
        return self.add_row(new_user_level)

    def delete_user_level(self, user_level_id: int) -> bool:
        """Deletes a user level by its ID.

        Args:
            user_level_id (int): The ID of the user level to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        return self.delete_row_by_id(user_level_id)
