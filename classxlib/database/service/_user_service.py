"""Database module for UserService class that interacts
with the `users` table"""

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import UserRepository
from ._base_service import BaseService
from ..model import User


class UserService(BaseService):
    """The User Service class for interacting with
    the repository classes.
    """

    def __init__(self, session: Session):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, UserRepository)
        self.repo: UserRepository

    def add_user(self, user_obj: User) -> User:
        """Service function for adding a user to the
        database

        Args:
            user_obj (User): The User class object to add

        Returns:
            User: The newly added User. Will be None if it
            fails.
        """
        # Adding the user to database
        return self.add(user_obj)

    def login_user(self, username: str, uuid: str) -> User:
        """Service function for logging in and verifying the user.
        Locates a user by their authentication token and verifies the
        username of them.

        Args:
            username (str): The username of the user.
            uuid (str): The uuid of the user provided
            by keycloak.

        Returns:
            User: The database user object. Returns None if there is an
            error in authtication
        """
        # Locating the user by their token
        user_obj = self.repo.get_by_uuid(auth_token=uuid)

        # Verifying the user is not None
        if user_obj is None:
            return None

        # Verifying the username matches
        if user_obj.username != username:
            return None
        return user_obj

    def get_by_uuid(self, uuid: str) -> User | None:
        """Retrieves a user from the database
        by matching it's authtication token

        Args:
            uuid (str): the keycloak uuid of the user.

        Returns:
            User: The database user object. Returns None if not
            found.
        """
        # Retrieving the user and returning it.
        return self.repo.get_by_uuid(uuid)

    def update_uuid(self, user_id: int, new_uuid: str) -> User:
        """Updates the keycloak uuid for a user in
        the database.

        Args:
            user_id (int): The ID of the user to update
            new_uuid (str): the new keycloak uuid this should only be used to update the default user..

        Returns:
            User: The user database object with the updated
            authorization token
        """
        # Updating and returning the user object in database
        return self.repo.update_uuid_by_id(user_id, new_uuid)

    def get_by_username(self, username: str):
        """Retrieves a user from the database
        by matching it's username

        Args:
            username (str): The username of the user.

        Returns:
            User: The database user object. Returns None if not
            found.
        """
        # Retrieving the user and returning it.
        return self.repo.get_by_username(username)

    def get_by_id(self, user_id: int) -> User:
        """Retrieves a user from the database
        by matching it's user id

        Args:
            user_id (int): The ID of the associated user.

        Returns:
            User: The database user object. Returns None if not
            found.
        """
        # Retrieving the user and returning it
        return self.repo.get_by_id(object_id=user_id)

    def remove_user_by_uuid(self, uuid: str) -> bool:
        """Removes a user from the database by matching it's
        authtication token then removing them

        Args:
            uuid (str): The uuid token
            provided and assigned by keycloak.

        Returns:
            bool: Returns True if successful and False if there
            are errors or the user is not found.
        """
        # Retrieving the user by it's token.
        user_obj = self.repo.get_by_uuid(uuid)

        # Verifying the user was found
        if user_obj is None:
            return False

        # Deleting the user by it's id
        return self.repo.delete_row_by_id(user_obj.id)

    def update_research_fields(
        self, user_id: int, research_field_id_list: list[int], append: bool = True
    ):
        """Updates the research field JSON attribute in the user data column

        Args:
            user_id (int): The ID of the user to update
            research_field_id_list (list[int]): List of new research field IDs
            append (bool, optional): Check to either append the IDs or replace them
            with the new list. Defaults to True.

        Returns:
            User: The user database object with the updated research field IDs
        """
        return self.repo.update_research_fields_by_id(
            user_id=user_id,
            research_field_id_list=research_field_id_list,
            append=append,
        )

    def get_all_user_except(self, username: str) -> list[User]:
        """Retrieves a list of users from the database
        by matching everything not equal to the username

        Args:
            username (str): The username of the user.

        Returns:
            list[User]: The list of database user objects. List will
            be empty if None found.
        """

        # Filtering by everything not equal
        return self.repo.get_all_except_username(
            username=username, get_default_user=False
        )
