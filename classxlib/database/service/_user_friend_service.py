"""Database module for UserFriendService class that interacts
with the `user_friend_services` table"""

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import UserFriendRepository
from ._base_service import BaseService
from ..model import UserFriend

__all__ = ["UserFriendService"]


class UserFriendService(BaseService):
    """The Crop Image Service class for interacting with
    the repository classes.
    """

    def __init__(self, session: Session):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, UserFriendRepository)
        self.repo: UserFriendRepository

    def create_friend_request(self, row: UserFriend):
        """Service function for adding a row  to the
        user_friends table
        Args:
            row (UserFriend): The UserFriend class object to add
        Returns:
            user_friend_obj: The newly added UserFriend. Will be None if it
            fails.
        """
        # Adding the user level to database
        return self.add(row)

    def get_sent_requests(self, user_id: int):
        """Service function for adding a user level to the
        database
        Args:
            user_id (int): user id to get requests for
        Returns:
            user_friend_objs List(UserFriend): Requests that are pending
        """
        return self.repo.get_requests_by_status(user_id, 0)

    def deny_friend_request(self, user_id: int, sender_id: int):
        """Service function denying a friend request
        Args:
            user_id (int): user Id who is denying the request
            sender_id (int): user id who sent the request
        Returns:
            user_friend_obj: The newly added UserLevel. Will be None if it
            fails.
        """
        return self.repo.update_status(sender_id, user_id, 2)

    def block_user(self, sender_id: int, reciver_id: int):
        """Service function for blocking a user
        database
        Args:
            sender_id (int): user who is sending the block
            reciver_id (int): user who is being blocked
        Returns:
            user_friend_obj: The newly added UserFriend. Will be None if it
            fails.
        """
        if self.repo.update_status(sender_id, reciver_id, 3) is not None:
            return

        request = UserFriend(sender_id, reciver_id, 3)

        return self.create_friend_request(request)

    def get_block_list(self, user_id: int):
        """Service function for gettlist list of blocked users
        Args:
            user_id (int): user to check their list for
        Returns:
            List(user_friend_obj): List of blocked people requests
        """
        return self.repo.get_requests_by_status(user_id, 3)

    def remove_request(self, sender_id, reciver_id):
        """Service function to remove a friend request (if the sender cancels it)
        Args:
            user_id (int): user to check their list for
        Returns:
            success (boolean): if it was successful
        """
        return self.repo.remove_request(sender_id, reciver_id)

    def accept_friend_request(self, sender_id: int, reciver_id: int):
        """Service function for accepting a friend request
        Args:
            sender_id (int): user id of the first user to check against
            reciver_id (int): user id of the second user to check against
        Returns:
            user_friend_obj: The newly added UserFriend. Will be None if it
            fails.
        """
        return self.repo.update_status(sender_id, reciver_id, 1, True)

    def get_friends(self, user_id: int):
        """Service to get accepted friends
        Args:
            user_id (int): user to check their list for
        Returns:
            List(user_friend_obj): List of blocked people requests
        """
        return self.repo.get_requests_by_status(user_id, 1)

    def get_pending(self, sender_id: int):
        """Service function for gettlist list of pending requests
        Args:
            user_id (int): user to check their list for
        Returns:
            List(user_friend_obj): List of blocked people requests
        """
        return self.repo.get_requests_by_status(sender_id, 0)

    def get_status(self, sender_id: int, receiver_id: int):
        """Service function to get a row between two users no matter if they sent or recivved
        Args:
            sender_id (int): user id of the first user to check against
            reciver_id (int): user id of the second user to check against
        Returns:
            user_friend_obj (UserFriend): List of blocked people requests
        """
        return self.repo.get_friend_row(sender_id, receiver_id)
