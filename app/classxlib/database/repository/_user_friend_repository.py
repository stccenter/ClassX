"""Database module for defining the UserFriendRepository Class"""

# Python Third Party Imports
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session, aliased

from classxlib.database.model._user import User

# Local Library Imports
from ..model import UserFriend
from ._base_repository import BaseRepository

__all__ = ['UserFriendRepository']
class UserFriendRepository(BaseRepository):
    """The class for interacting/querying the `user_friends` sql table.
        Args:
            session(sqlalchemy.orm.Session): The database session object
            to use for querying and commiting changes.
    """

    def __init__(self, session:Session):
        # Initializes the base repository class
        super().__init__(session=session,
                         model=UserFriend,
                         table_name="user_friends")

    def get_friend_row(self, sender_id: int, receiver_id: int):
        """Gets a a friend request status based off sender and reciver's user IDs

        Args:
            sender_id (int): user id of the first user to check against
            reciver_id (int): user id of the second user to check against

        Returns:
            UserFriend: The user friend database object, Returns None if not found.
        """

        # Filtering by the user ids we were given as they can be a sender or reciveer
        user_friend_obj = self.session.query(UserFriend).\
            filter(or_(
                and_(UserFriend.sender_id == sender_id, UserFriend.receiver_id == receiver_id),
                and_(UserFriend.sender_id == receiver_id, UserFriend.receiver_id == sender_id)
            )).first()

        
        return user_friend_obj
    

    def get_requests_by_status(self, sender_id: int, status: int, sender_only = False):
        """Get all pending friend requests

        Args:
            sender_id (int): user id who sent the requests

        Returns:
            List[UserFriend, User]: Pending requests
        """
        sender_alias = aliased(User)
        receiver_alias = aliased(User)
        
        if sender_only:
            return self.session.query(UserFriend, sender_alias, receiver_alias).\
                join(sender_alias, UserFriend.sender_id == sender_alias.id).\
                join(receiver_alias, UserFriend.receiver_id == receiver_alias.id).\
                filter(and_(
                    UserFriend.sender_id == sender_id,
                    UserFriend.status == status
                )).all()
        return self.session.query(UserFriend, sender_alias, receiver_alias).\
            join(sender_alias, UserFriend.sender_id == sender_alias.id).\
            join(receiver_alias, UserFriend.receiver_id == receiver_alias.id).\
            filter(and_(
                UserFriend.status == status,
                or_(
                    UserFriend.sender_id == sender_id,
                    UserFriend.receiver_id == sender_id
                )
                )).all()

    def update_status(self, sender_id: int, receiver_id: int, new_status: int, sender_only = False):
        """Updates a friend status of two users

        Args:
            sender_id (int): user id of the first user to check against
            reciver_id (int): user id of the second user to check against

        Returns:
            UserFriend: Updated User Friend Row, or None if not found
        """

        # Filtering by the user ids we were given as they can be a sender or reciveer
        if sender_only:
            user_friend_obj = self.session.query(UserFriend).\
                filter(and_(
                    UserFriend.sender_id == sender_id,
                    UserFriend.receiver_id == receiver_id
                )).first()
        else:
            user_friend_obj = self.session.query(UserFriend).\
                filter(or_(
                    and_(UserFriend.sender_id == sender_id, UserFriend.receiver_id == receiver_id),
                    and_(UserFriend.sender_id == receiver_id, UserFriend.receiver_id == sender_id)
                )).first()
                
        if user_friend_obj is None:
            return None

        # Overwriting the current permissions configuration
        user_friend_obj.status = new_status

        # Commiting the changes to the database
        if self.commit_changes() is False:
            return None

        return user_friend_obj

    def remove_request(self, sender_id, receiver_id):
        """Deletes a frind request between two users

        Args:
            sender_id (int): user id of the first user to check against
            reciver_id (int): user id of the second user to check against

        Returns:
            sucess (boolean): True if successful otherwise False;
        """
        self.session.query(UserFriend).\
        filter(or_(
            and_(UserFriend.sender_id == sender_id, UserFriend.receiver_id == receiver_id),
            and_(UserFriend.sender_id == receiver_id, UserFriend.receiver_id == sender_id)
        )).delete()
            
        
        # Commiting the changes to the database
        if self.commit_changes() is False:
            return False
        
        return True