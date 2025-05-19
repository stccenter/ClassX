"""Database module for defining the UserRepository Class"""

# Python Third Party Imports
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from sqlalchemy.orm.attributes import flag_modified

# Local Library Imports
from ..model import User
from ._base_repository import BaseRepository

__all__ = ['UserRepository']

class UserRepository(BaseRepository):
    """The class for interacting/querying the `users` sql table.
        Args:
            session(sqlalchemy.orm.Session): The database session object
            to use for querying and commiting changes.
    """

    def __init__(self, session:Session):
        # Initializes the base repository class
        super().__init__(session=session,
                         model=User,
                         table_name="users")

    def get_by_uuid(self, uuid:str) -> User | None:
        """Gets a user by their keycloak uuid

        Args:
            uuid (str): The encoded token to find the user
            by.

        Returns:
            User: The user database object, Returns None if not found.
        """
        # Filtering by the authtication token
        user_obj = self.session.query(User).filter(User.kc_uuid == uuid).first()

        return user_obj

    def get_by_username(self, username:str):
        """Gets a user by their username

        Args:
            username (str): The username of the associated user.

        Returns:
            User: The user database object, Returns None if not found.
        """
        # Filtering by the username
        user_obj = self.session.query(User).\
            filter(User.username == username).first()

        return user_obj

    def get_all_except_username(self,
                                username:str,
                                get_default_user:False):
        """Get all users not equal to the current username

        Args:
            username (str): The username of the user to filter by.
            get_default_user (False): Check to see if the default user should be returned.

        Returns:
            list(User): The list of user database objects, Returns an empty list if
            none found.
        """
        # Checking if we should return the default user or not.
        # Filtering by everything not equal to the username
        # NOTE This will be changed to user the friend code system in the future instead.
        if get_default_user is True:
            user_obj_list = self.session.query(User).\
                filter(User.username != username).all()
        else:
            user_obj_list = self.session.query(User).\
                filter(and_(User.username != username,
                            User.username != 'default')).all()
        return user_obj_list

    def update_uuid_by_id(self, user_id:int, new_uuid:str,) -> User:
        """Updates the keycloak uuid of a user by matching it's ID.

        Args:
            user_id (int): The ID of the user to update
            new_uuid (str): The new auth token to input for the user.

        Returns:
            User: The updated User object. Will be None if the update failed.
        """
        # Getting user by their ID
        user_obj = self.get_by_id(object_id=user_id)

        # Overwriting old token
        user_obj.kc_uuid = new_uuid

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return None

        return user_obj
