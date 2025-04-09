"""Database module for defining the UserRepository Class"""

# Python Third Party Imports
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError

# Local Library Imports
from ..model import User
from ._base_repository import BaseRepository

__all__ = ["UserRepository"]


class UserRepository(BaseRepository):
    """The class for interacting/querying the `users` SQL table.

    Args:
        session (Session): The database session object
            to use for querying and committing changes.
    """

    def __init__(self, session: Session):
        # Initializes the base repository class
        super().__init__(session=session, model=User, table_name="users")

    def get_by_uuid(self, uuid: str) -> Optional[User]:
        """Gets a user by their Keycloak UUID.

        Args:
            uuid (str): The Keycloak UUID to find the user by.

        Returns:
            Optional[User]: The user database object, or None if not found.
        """
        stmt = select(User).where(User.kc_uuid == uuid)
        try:
            result = self.session.scalars(stmt).first()
            return result
        except SQLAlchemyError as e:
            return None

    def get_by_username(self, username: str) -> Optional[User]:
        """Gets a user by their username.

        Args:
            username (str): The username of the associated user.

        Returns:
            Optional[User]: The user database object, or None if not found.
        """
        stmt = select(User).where(User.username == username)
        try:
            result = self.session.scalars(stmt).first()
            return result
        except SQLAlchemyError as e:
            return None

    def get_all_except_username(
        self, username: str, get_default_user: bool = False
    ) -> List[User]:
        """Get all users except the one with the specified username.

        Args:
            username (str): The username of the user to exclude.
            get_default_user (bool, optional): Whether to include the default user. Defaults to False.

        Returns:
            List[User]: The list of user database objects, empty if none found.
        """
        try:
            if get_default_user:
                stmt = select(User).where(User.username != username)
            else:
                stmt = select(User).where(
                    and_(User.username != username, User.username != "default")
                )
            results = self.session.scalars(stmt).all()
            return results
        except SQLAlchemyError as e:
            return []

    def update_uuid_by_id(self, user_id: int, new_uuid: str) -> Optional[User]:
        """Updates the Keycloak UUID of a user by matching its ID.

        Args:
            user_id (int): The ID of the user to update.
            new_uuid (str): The new UUID to assign to the user.

        Returns:
            Optional[User]: The updated User object, or None if the update failed.
        """
        try:
            # Retrieve the user by ID using the BaseRepository method
            user_obj = self.get_by_id(object_id=user_id)
            if not user_obj:
                return None

            # Update the UUID
            user_obj.kc_uuid = new_uuid

            # Flag the 'kc_uuid' attribute as modified if using mutable types
            # Not strictly necessary for simple types like strings
            # flag_modified(user_obj, "kc_uuid")

            # Commit the changes
            if not self.commit_changes():
                return None

            return user_obj
        except SQLAlchemyError as e:
            self.session.rollback()
            return None
