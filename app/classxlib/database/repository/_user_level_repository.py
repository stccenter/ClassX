"""Database module for defining the UserLevelRepository Class"""

# Python Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..model import UserLevel
from ._base_repository import BaseRepository

__all__ = ['UserLevelRepository']
class UserLevelRepository(BaseRepository):
    """The class for interacting/querying the `user_levels` sql table.
        Args:
            session(sqlalchemy.orm.Session): The database session object
            to use for querying and commiting changes.
    """

    def __init__(self, session:Session):
        # Initializes the base repository class
        super().__init__(session=session,
                         model=UserLevel,
                         table_name="user_levels")

    def get_by_name(self, user_level_name:str):
        """Gets a user_level by their name

        Args:
            user_level_name (int): The name of the user level

        Returns:
            UserLevel: The user level database object, Returns None if not found.
        """

        # Filtering by the user level name
        user_level_obj = self.session.query(UserLevel).\
            filter(UserLevel.name == user_level_name).first()

        return user_level_obj

    def update_permission_by_id(self, user_level_id:int,
                                new_permissions:dict):
        """Updates the permissions of a given user level

        Args:
            user_level_id (int): The ID of the user level to update
            new_permissions (dict): The new permissions configuration

        Returns:
            UserLevel: The user level database object with the updated
            configurations. Returns None if there is an error.
        """

        # Filtering the user level by id
        user_level_obj = self.session.query(UserLevel).\
            filter(UserLevel.id == user_level_id).first()

        # Overwriting the current permissions configuration
        user_level_obj.permissions = new_permissions

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return None

        return user_level_obj
